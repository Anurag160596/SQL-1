# SQL-1

A **dashboard creation agent**: describe the dashboard you want in plain English,
and an AI agent explores a SQL database, writes the queries, and assembles an
interactive HTML dashboard.

The agent is powered by Claude (via the official `anthropic` SDK) and drives
itself with a small set of tools. Every chart is rendered from the SQL the agent
writes, so the numbers are real query results — not anything the model made up.

## How it works

```
request ──▶  Claude agent  ──▶  dashboard.html
                  │
                  ├─ list_tables      discover tables
                  ├─ describe_table   inspect columns + sample rows
                  ├─ run_query        explore data (read-only SELECT)
                  └─ add_panel        add a chart, backed by a SQL query
```

The agent loops: it explores the schema, validates queries with `run_query`,
then calls `add_panel` once per visualization. Panels are rendered to a
self-contained `dashboard.html` using [Plotly](https://plotly.com/javascript/)
(loaded from a CDN — no build step). Supported panel types: `bar`, `line`,
`pie`, `scatter`, and `table`.

Database access is **read-only** (SQLite opened in `mode=ro`, and only
`SELECT` / `WITH` statements are accepted), so the agent can't modify your data.

## Files

| File                 | Purpose                                                      |
| -------------------- | ----------------------------------------------------------- |
| `dashboard_agent.py` | The agent + tools + HTML renderer (entry point).            |
| `sample_data.py`     | Builds `sales.db`, a sample e-commerce database to explore. |
| `requirements.txt`   | Python dependencies (`anthropic`).                          |

## Quick start

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...

# 1. Create the sample database (customers, products, orders, order_items)
python sample_data.py

# 2. Build a dashboard from a natural-language request
python dashboard_agent.py "Show revenue over time, sales by region, and top products"

# 3. Open the result
open dashboard.html   # or just open it in your browser
```

Running with no request uses a sensible default sales-overview prompt.

### Options

```bash
python dashboard_agent.py "your request" \
    --db   sales.db        # path to a SQLite database (default: sales.db)
    --out  dashboard.html  # output file (default: dashboard.html)
```

## Using your own database

Point `--db` at any SQLite file. The agent discovers the schema on its own, so
no configuration is needed — just describe the dashboard you want. (To connect a
different engine such as Postgres or MySQL, swap the `Database` class in
`dashboard_agent.py` for the corresponding driver; the rest is unchanged.)

## Model

Uses `claude-opus-4-8` with adaptive thinking. Set `ANTHROPIC_API_KEY` in your
environment before running.
