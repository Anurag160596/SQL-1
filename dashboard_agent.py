"""Dashboard creation agent.

Give it a natural-language request and a SQLite database; it explores the
schema, writes read-only SQL queries, and assembles an interactive HTML
dashboard. The agent is powered by Claude through the official Anthropic SDK
and drives itself with a small set of tools:

    list_tables       discover the tables in the database
    describe_table    inspect a table's columns and a few sample rows
    run_query         run a read-only SELECT to explore the data
    add_panel         add a chart (or table) to the dashboard, backed by SQL

Every panel is rendered from the SQL the agent supplies, so the numbers in the
dashboard are real query results rather than anything the model invented.

Usage:
    export ANTHROPIC_API_KEY=...
    python sample_data.py                 # one-time: build sales.db
    python dashboard_agent.py "Show sales trends and the top products"

Then open dashboard.html in a browser.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

import anthropic

MODEL = "claude-opus-4-8"

SYSTEM_PROMPT = """\
You are a data-dashboard building agent. The user gives you a request in plain \
English and you have read-only access to a SQLite database through tools.

Work in this order:
1. Call list_tables to see what exists, then describe_table on the relevant \
tables to learn the columns.
2. Use run_query to explore and validate the SQL you intend to chart (check \
that columns, groupings, and row counts look right).
3. Call add_panel once per visualization to build the dashboard. Prefer 3-6 \
focused panels that together answer the request. Each panel runs its own SQL, \
so write a query whose result columns map cleanly to the chart you want.

Guidelines for add_panel:
- bar / line: x_column is the category or time axis; y_columns are one or more \
numeric series.
- pie: x_column holds the labels, the first y_column holds the values.
- scatter: x_column and one y_column, both numeric.
- table: omit x_column/y_columns; every selected column is shown.
- Order time series chronologically and limit "top N" queries so charts stay \
readable. Give every panel a clear title and a one-line description.

Only issue SELECT (or WITH ... SELECT) statements. When the dashboard fully \
answers the request, stop and briefly summarize what you built.\
"""

TOOLS = [
    {
        "name": "list_tables",
        "description": "List the names of all tables in the database.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "describe_table",
        "description": "Show a table's column names/types and up to 5 sample rows.",
        "input_schema": {
            "type": "object",
            "properties": {
                "table": {"type": "string", "description": "Table name"}
            },
            "required": ["table"],
        },
    },
    {
        "name": "run_query",
        "description": (
            "Run a read-only SELECT query and return up to 50 rows as JSON. "
            "Use this to explore and validate data before charting it."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "sql": {"type": "string", "description": "A single SELECT statement"}
            },
            "required": ["sql"],
        },
    },
    {
        "name": "add_panel",
        "description": (
            "Add one visualization to the dashboard. The SQL is executed and its "
            "results are charted, so it must return exactly the columns the chart "
            "needs."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {
                    "type": "string",
                    "description": "One line explaining what the panel shows.",
                },
                "chart_type": {
                    "type": "string",
                    "enum": ["bar", "line", "pie", "scatter", "table"],
                },
                "sql": {
                    "type": "string",
                    "description": "SELECT statement producing the panel's data.",
                },
                "x_column": {
                    "type": "string",
                    "description": "Column for the x-axis / pie labels (not for table).",
                },
                "y_columns": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Numeric column(s) to plot (not for table).",
                },
            },
            "required": ["title", "description", "chart_type", "sql"],
        },
    },
]


class Database:
    """Read-only access to a SQLite database."""

    def __init__(self, path: Path):
        if not path.exists():
            raise FileNotFoundError(
                f"Database not found: {path}. Run `python sample_data.py` first."
            )
        # Open in read-only mode so the agent cannot mutate the data.
        uri = f"file:{path}?mode=ro"
        self.conn = sqlite3.connect(uri, uri=True)
        self.conn.row_factory = sqlite3.Row

    def list_tables(self) -> list[str]:
        rows = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
        return [r["name"] for r in rows]

    def describe_table(self, table: str) -> dict:
        if table not in self.list_tables():
            raise ValueError(f"Unknown table: {table}")
        cols = self.conn.execute(f"PRAGMA table_info({table})").fetchall()
        sample = self.conn.execute(f"SELECT * FROM {table} LIMIT 5").fetchall()
        return {
            "columns": [{"name": c["name"], "type": c["type"]} for c in cols],
            "sample_rows": [dict(r) for r in sample],
        }

    def query(self, sql: str, limit: int | None = None) -> tuple[list[str], list[list]]:
        stripped = sql.lstrip().lower()
        if not (stripped.startswith("select") or stripped.startswith("with")):
            raise ValueError("Only SELECT / WITH queries are allowed.")
        cur = self.conn.execute(sql)
        rows = cur.fetchmany(limit) if limit else cur.fetchall()
        columns = [d[0] for d in cur.description] if cur.description else []
        return columns, [list(r) for r in rows]


def dispatch(db: Database, panels: list[dict], name: str, args: dict) -> str:
    """Execute a tool call and return a JSON string result for the model."""
    try:
        if name == "list_tables":
            return json.dumps({"tables": db.list_tables()})

        if name == "describe_table":
            return json.dumps(db.describe_table(args["table"]), default=str)

        if name == "run_query":
            columns, rows = db.query(args["sql"], limit=50)
            return json.dumps(
                {"columns": columns, "rows": rows, "row_count": len(rows)},
                default=str,
            )

        if name == "add_panel":
            columns, rows = db.query(args["sql"])
            panel = {
                "title": args["title"],
                "description": args["description"],
                "chart_type": args["chart_type"],
                "columns": columns,
                "rows": rows,
                "x_column": args.get("x_column"),
                "y_columns": args.get("y_columns", []),
            }
            panels.append(panel)
            print(f"  + panel: {panel['title']} ({panel['chart_type']}, {len(rows)} rows)")
            return json.dumps(
                {"status": "added", "panel_number": len(panels), "row_count": len(rows)}
            )

        return json.dumps({"error": f"Unknown tool: {name}"})
    except Exception as exc:  # surface errors back to the model so it can adapt
        return json.dumps({"error": str(exc)})


def run_agent(request: str, db: Database, max_turns: int = 25) -> list[dict]:
    client = anthropic.Anthropic()
    panels: list[dict] = []
    messages = [{"role": "user", "content": request}]

    for _ in range(max_turns):
        response = client.messages.create(
            model=MODEL,
            max_tokens=16000,
            thinking={"type": "adaptive"},
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        for block in response.content:
            if block.type == "text" and block.text.strip():
                print(f"\n{block.text.strip()}\n")

        if response.stop_reason != "tool_use":
            break

        messages.append({"role": "assistant", "content": response.content})
        results = []
        for block in response.content:
            if block.type == "tool_use":
                output = dispatch(db, panels, block.name, block.input)
                results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": output,
                    }
                )
        messages.append({"role": "user", "content": results})

    return panels


def render_dashboard(title: str, panels: list[dict], out_path: Path) -> None:
    """Render panels into a self-contained HTML dashboard using Plotly (CDN)."""
    data_json = json.dumps(panels)
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
  body { font-family: system-ui, sans-serif; margin: 0; background: #f5f6f8; color: #1d2330; }
  header { background: #1d2330; color: #fff; padding: 24px 32px; }
  header h1 { margin: 0; font-size: 22px; }
  header p { margin: 6px 0 0; color: #aeb6c4; font-size: 14px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(420px, 1fr)); gap: 20px; padding: 24px 32px; }
  .panel { background: #fff; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,.1); padding: 16px; }
  .panel h2 { margin: 0 0 2px; font-size: 16px; }
  .panel .desc { margin: 0 0 12px; color: #66718a; font-size: 13px; }
  .chart { width: 100%; height: 340px; }
  table { border-collapse: collapse; width: 100%; font-size: 13px; }
  th, td { border-bottom: 1px solid #eceef2; padding: 6px 8px; text-align: left; }
  th { background: #f0f2f5; }
  footer { padding: 16px 32px; color: #9aa3b2; font-size: 12px; }
</style>
</head>
<body>
<header><h1>__TITLE__</h1><p>__SUBTITLE__</p></header>
<div class="grid" id="grid"></div>
<footer>Generated by the dashboard agent — every panel is backed by a live SQL query.</footer>
<script>
const PANELS = __DATA__;
const PALETTE = ["#4c78a8","#f58518","#54a24b","#e45756","#72b7b2","#ff9da6","#9d755d"];

PANELS.forEach((p, i) => {
  const panel = document.createElement("div");
  panel.className = "panel";
  panel.innerHTML = `<h2>${p.title}</h2><p class="desc">${p.description}</p>`;
  const body = document.createElement("div");
  panel.appendChild(body);
  document.getElementById("grid").appendChild(panel);

  const colIdx = name => p.columns.indexOf(name);
  const col = name => p.rows.map(r => r[colIdx(name)]);

  if (p.chart_type === "table") {
    let html = "<table><thead><tr>" +
      p.columns.map(c => `<th>${c}</th>`).join("") + "</tr></thead><tbody>";
    html += p.rows.map(r => "<tr>" + r.map(v => `<td>${v}</td>`).join("") + "</tr>").join("");
    html += "</tbody></table>";
    body.innerHTML = html;
    return;
  }

  const div = document.createElement("div");
  div.className = "chart";
  body.appendChild(div);

  let traces = [];
  if (p.chart_type === "bar" || p.chart_type === "line") {
    (p.y_columns || []).forEach((y, j) => traces.push({
      x: col(p.x_column), y: col(y), name: y,
      type: p.chart_type === "line" ? "scatter" : "bar",
      mode: p.chart_type === "line" ? "lines+markers" : undefined,
      marker: { color: PALETTE[j % PALETTE.length] }
    }));
  } else if (p.chart_type === "pie") {
    traces.push({
      labels: col(p.x_column), values: col((p.y_columns || [])[0]),
      type: "pie", marker: { colors: PALETTE }
    });
  } else if (p.chart_type === "scatter") {
    traces.push({
      x: col(p.x_column), y: col((p.y_columns || [])[0]),
      mode: "markers", type: "scatter",
      marker: { color: PALETTE[0] }
    });
  }

  Plotly.newPlot(div, traces, {
    margin: { t: 10, r: 10, b: 40, l: 50 },
    legend: { orientation: "h" }
  }, { responsive: true, displayModeBar: false });
});
</script>
</body>
</html>
"""
    subtitle = f"{len(panels)} panel(s)"
    html = (
        html.replace("__TITLE__", title)
        .replace("__SUBTITLE__", subtitle)
        .replace("__DATA__", data_json)
    )
    out_path.write_text(html, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a dashboard from a SQL database.")
    parser.add_argument(
        "request",
        nargs="?",
        default="Build an overview dashboard of sales performance: revenue over "
        "time, sales by region and category, and the top-selling products.",
        help="Natural-language description of the dashboard you want.",
    )
    parser.add_argument("--db", default="sales.db", help="Path to the SQLite database.")
    parser.add_argument("--out", default="dashboard.html", help="Output HTML file.")
    args = parser.parse_args()

    try:
        db = Database(Path(args.db))
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1

    print(f"Request: {args.request}\n")
    panels = run_agent(args.request, db)

    if not panels:
        print("\nThe agent did not produce any panels.", file=sys.stderr)
        return 1

    out_path = Path(args.out)
    render_dashboard("Dashboard", panels, out_path)
    print(f"\nWrote {len(panels)} panel(s) to {out_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
