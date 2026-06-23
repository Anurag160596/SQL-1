#!/usr/bin/env python3
"""
Agentic AI Daily Digest agent.

Flow:
  1. Load config.yaml (topics, competitor watchlist, recipients, model).
  2. Ask Gemini (with Google Search grounding) to research the last ~24h and
     write a deep-dive markdown digest.
  3. Save the digest to digests/YYYY-MM-DD.md.
  4. Email it via Resend (markdown rendered to HTML).

Required environment variables:
  GEMINI_API_KEY   - Google AI Studio key (Gemini).
  RESEND_API_KEY   - Resend API key for sending email.

Optional environment variables:
  GEMINI_MODEL     - overrides model.name from config.yaml.
  DIGEST_DRY_RUN   - if "1"/"true", generate + save but do NOT send email.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
import yaml

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.yaml"
DIGESTS_DIR = ROOT / "digests"
ALERT_STATE_PATH = ROOT / "alerts_state.json"
ALERT_STATE_RETENTION_DAYS = 7
KB_DIR = ROOT / "knowledge_base"
KB_CHAR_BUDGET = 48000  # cap KB text injected into the prompt


def fail(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        fail(f"config.yaml not found at {CONFIG_PATH}")
    with CONFIG_PATH.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def local_now(tz_name: str) -> datetime:
    try:
        return datetime.now(ZoneInfo(tz_name))
    except Exception:
        return datetime.now(timezone.utc)


def load_knowledge_base() -> str:
    """Concatenate every markdown file in knowledge_base/ as grounding context."""
    if not KB_DIR.is_dir():
        return ""
    parts: list[str] = []
    for md_file in sorted(KB_DIR.glob("*.md")):
        try:
            parts.append(md_file.read_text(encoding="utf-8").strip())
        except Exception:
            continue
    kb = "\n\n".join(parts)
    if len(kb) > KB_CHAR_BUDGET:
        kb = kb[:KB_CHAR_BUDGET] + "\n\n[...knowledge base truncated...]"
    return kb


NEWS_RSS_BASE = "https://news.google.com/rss/search"


def _fetch_rss(query: str, days: int) -> bytes:
    params = {"q": f"{query} when:{days}d", "hl": "en-US", "gl": "US", "ceid": "US:en"}
    url = NEWS_RSS_BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (digest-agent)"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read()


def fetch_news(config: dict, now_local: datetime, lookback_hours: int | None = None) -> list[dict]:
    """Pull fresh, dated competitor news from Google News RSS (free, no key).

    Returns items within the lookback window: {competitor, title, url, date, source}.
    On any failure it returns whatever it gathered (possibly empty), letting the
    caller fall back to model-side web search.
    """
    news_cfg = config.get("news", {})
    if not news_cfg.get("enabled", True):
        return []
    lookback = int(lookback_hours or config.get("lookback_hours", 72))
    days = max(1, math.ceil(lookback / 24))
    cutoff = datetime.now(timezone.utc) - timedelta(hours=lookback)
    per_company = int(news_cfg.get("max_per_company", 5))
    total_cap = int(news_cfg.get("max_total", 40))

    items: list[dict] = []
    seen: set[str] = set()
    for w in config.get("watchlist", []):
        name = w.get("name", "")
        query = w.get("query") or f'"{name}"'
        try:
            root = ET.fromstring(_fetch_rss(query, days))
        except Exception as exc:
            print(f"  news fetch failed for {name}: {str(exc)[:80]}")
            continue
        count = 0
        for item in root.iter("item"):
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            pub = item.findtext("pubDate")
            src_el = item.find("source")
            source = (src_el.text or "").strip() if src_el is not None else ""
            if not title or not pub:
                continue
            try:
                dt = parsedate_to_datetime(pub)
            except Exception:
                continue
            if dt is None:
                continue
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            if dt < cutoff:
                continue
            key = re.sub(r"\W+", "", title.lower())[:80]
            if key in seen:
                continue
            seen.add(key)
            items.append({
                "competitor": name,
                "title": title,
                "url": link,
                "date": dt.strftime("%Y-%m-%d"),
                "source": source,
            })
            count += 1
            if count >= per_company:
                break
    items.sort(key=lambda x: x["date"], reverse=True)
    if len(items) > total_cap:
        items = items[:total_cap]
    print(f"Fetched {len(items)} fresh news item(s) from Google News RSS.")
    return items


def format_news_block(items: list[dict]) -> str:
    by_company: dict[str, list[dict]] = {}
    for it in items:
        by_company.setdefault(it["competitor"], []).append(it)
    lines: list[str] = []
    for comp, lst in by_company.items():
        lines.append(f"### {comp}")
        for it in lst:
            src = f" — {it['source']}" if it.get("source") else ""
            lines.append(f"- ({it['date']}) {it['title']}{src} — {it['url']}")
    return "\n".join(lines)


def build_prompt(
    config: dict,
    now_local: datetime,
    knowledge_base: str = "",
    news_items: "list[dict] | None" = None,
) -> str:
    lookback = int(config.get("lookback_hours", 24))
    since = now_local - timedelta(hours=lookback)
    topics = config.get("topics", [])
    watchlist = config.get("watchlist", [])

    topic_lines = "\n".join(f"  - {t}" for t in topics) or "  - (none specified)"

    if watchlist:
        watch_lines = "\n".join(
            f"  - {w.get('name', '?')} — focus: {w.get('focus', 'anything notable')}"
            for w in watchlist
        )
    else:
        watch_lines = "  - (none specified)"

    undercut = config.get("undercut", {})
    levers = undercut.get("levers", [])
    lever_lines = "\n".join(f"  - {l}" for l in levers) or "  - (none specified)"

    today = now_local.strftime("%A, %d %B %Y")
    month_year = now_local.strftime("%B %Y")
    window = (
        f"{since.strftime('%Y-%m-%d %H:%M %Z')} to "
        f"{now_local.strftime('%Y-%m-%d %H:%M %Z')}"
    )

    if news_items:
        # Fresh-news mode: items were pre-fetched (e.g. Google News RSS), already
        # filtered to the window and dated. The model must NOT search or invent —
        # it builds the digest strictly from these real items.
        sourcing_rules = f"""## ⛔ SOURCING RULES (read first)
1. A set of PRE-FETCHED, real, dated news items from the last {lookback} hours is \
provided below in <fresh_news>. Build the entire digest STRICTLY from these items.
2. Do NOT invent items, do NOT add anything not in <fresh_news>, and do NOT pull \
"news" from the knowledge base or memory. Every item you report MUST correspond to \
one in <fresh_news>, keeping its **(YYYY-MM-DD)** date and its source link.
3. ATTRIBUTION CHECK (critical): attribute an item to a competitor ONLY if the \
article is genuinely ABOUT that competitor. DROP the item if the competitor is just \
mentioned in passing (as an example, comparison, or customer), if the story is \
actually about a different company, or if it's a different organisation that merely \
shares the name (e.g. a manufacturer, foundry, or nonprofit). NEVER restate another \
company's funding/news under a competitor's name. When in doubt, drop it.
4. Relevance: keep only items relevant to enterprise CX / contact-center / agentic \
AI. Drop unrelated items (sports sponsorships, manufacturing, generic stock blurbs).
5. Judgement is yours: pick the most important items, group/synthesise them, and \
frame the undercut angle using the knowledge base. You may drop trivial items.
6. Honesty over volume: if <fresh_news> is thin or has nothing material, say \
"Nothing material in the window" rather than padding.

<fresh_news>
{format_news_block(news_items)}
</fresh_news>"""
    else:
        # Fallback mode: no pre-fetched news, so the model must search the web itself.
        sourcing_rules = f"""## ⛔ CRITICAL RECENCY RULES (read first)
1. You MUST use Google Search. For EACH watchlist company run explicit recent-news \
queries (e.g. "<company> news", "<company> announcement {month_year}", \
"<company> funding/pricing/outage"). Do not answer from memory.
2. Report ONLY items you found via search that were **published within the window \
{window}** (last {lookback} hours). Every item MUST cite its **publication date as \
(YYYY-MM-DD)** inline. If you cannot establish a publication date within the window, \
DROP the item.
3. The knowledge base below is BACKGROUND ONLY. NEVER present a knowledge-base fact \
(e.g. an already-known funding round, the Genesys outage, the NICE–Cognigy deal) as \
today's news. Use it only to interpret and frame genuinely new search results.
4. Honesty over volume: if a section or the whole digest has nothing new in the \
window, say "Nothing new in the window" — do NOT backfill with older or KB items."""

    kb_block = ""
    if knowledge_base:
        kb_block = f"""
## Internal knowledge base (background — use for framing, not as today's news)
The following is our standing context on Kore.ai and each tracked competitor. Use it
to interpret today's developments, frame "Why it matters" vs. Kore.ai, and know each
company's documented strengths/gaps. Treat "battlecard framing" as our positioning,
not neutral fact. Do NOT repeat it as news — only report genuinely NEW developments
found via search, informed by this context.

<knowledge_base>
{knowledge_base}
</knowledge_base>
"""

    return f"""You are a senior competitive-intelligence analyst at Kore.ai, an \
enterprise conversational-AI and agentic-platform vendor. You track the \
**enterprise agentic AI / contact-center AI (CCAI) / customer-experience** \
market for a product-marketing audience. Today is {today}. Produce a DEEP-DIVE \
daily competitive-intelligence digest.

Your job is not just to report news — it is to find **openings to undercut these \
competitors** and hand our teams (Sales, Product Marketing, Analyst Relations, \
Product) something they can act on today.

{sourcing_rules}
{kb_block}
## What to cover (sweep all of these)
{topic_lines}

## Competitor watchlist (give this its own prominent section)
Prioritize and specifically search for news about each of these companies:
{watch_lines}

## Undercut levers — actively hunt for these openings across every competitor
These are the weaknesses to look for. Any new evidence of one is an opening:
{lever_lines}

## Output format (Markdown only — no preamble, no "here is your digest")
Every news item, in every section, MUST begin with its publication date as \
**(YYYY-MM-DD)** and carry a working source link. Items without a verifiable \
in-window date do not belong in the digest. Start directly with an H1 title line. \
Structure:

# Agentic AI Daily Digest — {today}

**TL;DR** — 3-5 bullet points capturing the single most important things today, \
leading with the sharpest undercut opportunity.

## ⚔️ Undercut Opportunities (the hero section — lead with this)
For each genuinely new competitor development that creates an opening, write an entry. \
Only include real openings backed by a source — never manufacture one. If nothing is \
actionable today, say so in one line. Format each entry as:

- **[Competitor] — <one-line event>** — [Source](url)
  - **Lever:** which weakness this exposes (Pricing/TCO · Proof/validation gap · \
Channel/coverage gap · Reliability/governance · or other — name it)
  - **Angle:** the attack narrative — how to frame this against the competitor
  - **Kore.ai counter:** the specific proof point/capability to deploy (ABL determinism, \
true omnichannel, multi-model routing, 6x analyst Leader status, etc. — cite the KB)
  - **Plays:** concrete, team-tagged actions —
    🟦 **Sales** (battlecard line or trap discovery question) ·
    🟩 **PMM** (campaign/content/comparison angle) ·
    🟪 **AR** (what to feed Gartner/Forrester/Everest/IDC) ·
    🟧 **Product** (gap to close to neutralize them)

## 🏆 Top Stories
The 2-4 biggest developments. For EACH: a bold headline, 2-4 sentences of \
substance, an explicit **Why it matters** line, and a Markdown source link \
[Source](url). Connect related items where relevant.

## 🎯 Competitor Watch
One subsection per watchlist company that has real news. Bold the company name, \
summarize what happened, give **Why it matters** (especially vs. Kore.ai's \
enterprise CX / agentic platform positioning), and link the source. \
If a company has nothing new, omit it (don't invent news).

## 🏗️ Platform & Big-Tech Moves
Enterprise agentic-platform and CCAI moves from the big players (Salesforce \
Agentforce, ServiceNow, Microsoft, Google CCAI, AWS, IBM) and notable \
foundation-model releases relevant to CX agents. Bullets with links.

## 📊 Analysts & Rankings
New analyst reports, Magic Quadrant / Wave / Everest / IDC placements, awards, \
and benchmark or ranking news. For each: one-line takeaway + link. \
Omit if nothing new.

## 💰 Funding, M&A & Industry
Funding rounds, acquisitions, earnings, launches, enterprise adoption, and \
partnerships across CX / customer-service / agentic AI. Bullets with links.

## ⚡ Quick Hits
A handful of smaller-but-worth-knowing items as one-liners with links.

## Rules
- Every factual claim must have a real, working source link. Never fabricate URLs.
- Be specific (numbers, names, dates). Skip hype and marketing fluff.
- Write for a technical reader who builds agents. Analytical, not breathless.
- It is fine for the digest to be long; depth is the goal."""


def generate_digest(config: dict, prompt: str, use_search: bool = True):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        fail("GEMINI_API_KEY is not set.")

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        fail("google-genai not installed. Run: pip install -r requirements.txt")

    model_cfg = config.get("model", {})
    primary = os.environ.get("GEMINI_MODEL") or model_cfg.get("name", "gemini-2.5-flash")
    fallbacks = model_cfg.get("fallbacks", ["gemini-2.5-flash-lite"])
    if use_search:
        # Search quality matters → lead with the configured (grounding) model.
        order = [primary, *fallbacks]
    else:
        # Pure synthesis of pre-fetched news → no search needed, so lead with the
        # cheap, reliable synthesis model (avoids burning retries on a throttled flash).
        synth = model_cfg.get("synthesis_model", "gemini-2.5-flash-lite")
        order = [synth, primary, *fallbacks]
    # Ordered, de-duplicated candidate list.
    candidates: list[str] = []
    for m in order:
        if m and m not in candidates:
            candidates.append(m)
    temperature = float(model_cfg.get("temperature", 0.4))
    max_retries = max(1, int(model_cfg.get("max_retries", 3)))
    backoff_base = float(model_cfg.get("retry_backoff_seconds", 5))

    client = genai.Client(api_key=api_key)
    if use_search:
        tools = [types.Tool(google_search=types.GoogleSearch())]
    else:
        # Fresh news already supplied in the prompt — no model-side search needed.
        tools = []
    gen_config = types.GenerateContentConfig(tools=tools, temperature=temperature)

    # Retryable: model overloaded (503) / quota (429) / transient 5xx. For each
    # candidate model we retry with exponential backoff, then fall through to the
    # next model — so a transient free-tier 503 doesn't kill an unattended run.
    retry_codes = {429, 500, 502, 503, 504}
    response = None
    last_err: Exception | None = None
    mode_label = "Google Search grounding" if use_search else "synthesis, no search"
    for model_name in candidates:
        for attempt in range(1, max_retries + 1):
            print(
                f"Generating digest with {model_name} "
                f"(attempt {attempt}/{max_retries}, {mode_label})..."
            )
            try:
                response = client.models.generate_content(
                    model=model_name, contents=prompt, config=gen_config
                )
                print(f"  -> succeeded with {model_name}")
                break
            except genai.errors.APIError as exc:
                code = getattr(exc, "code", None) or getattr(exc, "status_code", None)
                last_err = exc
                if code not in retry_codes:
                    raise
                if attempt < max_retries:
                    wait = backoff_base * (2 ** (attempt - 1))
                    print(f"  -> {code} on {model_name}; retrying in {wait:.0f}s...")
                    time.sleep(wait)
                else:
                    print(
                        f"  -> {code} on {model_name}; exhausted {max_retries} "
                        "attempts, trying next model..."
                    )
        if response is not None:
            break
    if response is None:
        fail(f"All candidate models failed ({', '.join(candidates)}). Last error: {last_err}")

    text = (getattr(response, "text", None) or "").strip()
    if not text:
        fail("Gemini returned an empty digest.")

    sources = extract_sources(response)
    if sources:
        text += "\n\n---\n\n### 📎 Grounding sources\n" + "\n".join(
            f"- [{title}]({url})" for title, url in sources
        )
    # Return the live-search source count so callers can gate on grounding:
    # zero sources means the model answered without web search (likely recycling
    # the knowledge base), so the digest must not be presented as fresh news.
    return text, len(sources)


def extract_sources(response) -> list[tuple[str, str]]:
    """Pull grounding citation links out of the Gemini response, best-effort."""
    seen: dict[str, str] = {}
    try:
        for cand in getattr(response, "candidates", []) or []:
            meta = getattr(cand, "grounding_metadata", None)
            for chunk in getattr(meta, "grounding_chunks", []) or []:
                web = getattr(chunk, "web", None)
                if web and getattr(web, "uri", None):
                    title = getattr(web, "title", None) or web.uri
                    seen.setdefault(web.uri, title)
    except Exception:
        pass
    return list((title, url) for url, title in seen.items())


def save_digest(markdown_text: str, now_local: datetime) -> Path:
    DIGESTS_DIR.mkdir(exist_ok=True)
    # Include the run time so multiple runs/day (e.g. the 12-hourly schedule)
    # are each archived instead of overwriting one another.
    out_path = DIGESTS_DIR / f"{now_local.strftime('%Y-%m-%d-%H%M')}.md"
    out_path.write_text(markdown_text + "\n", encoding="utf-8")
    print(f"Saved digest to {out_path}")
    return out_path


def send_email(
    config: dict, markdown_text: str, now_local: datetime, subject: str | None = None
) -> None:
    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        fail("RESEND_API_KEY is not set.")

    try:
        import markdown as md
    except ImportError:
        fail("markdown not installed. Run: pip install -r requirements.txt")

    html_body = md.markdown(
        markdown_text, extensions=["extra", "sane_lists", "nl2br"]
    )
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
  body {{ font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
         line-height: 1.55; color: #1a1a1a; max-width: 720px; margin: 0 auto; padding: 16px; }}
  h1 {{ font-size: 24px; border-bottom: 2px solid #eaeaea; padding-bottom: 8px; }}
  h2 {{ font-size: 19px; margin-top: 28px; }}
  h3 {{ font-size: 16px; margin-top: 20px; }}
  a {{ color: #2563eb; }}
  hr {{ border: none; border-top: 1px solid #eaeaea; margin: 24px 0; }}
  code {{ background: #f4f4f4; padding: 1px 4px; border-radius: 4px; }}
</style></head><body>{html_body}</body></html>"""

    email_cfg = config.get("email", {})
    if subject is None:
        subject_prefix = email_cfg.get("subject_prefix", "🤖 Agentic AI Daily —")
        subject = f"{subject_prefix} {now_local.strftime('%A, %d %b %Y')}"
    sender = email_cfg.get("from", "Agentic AI Digest <onboarding@resend.dev>")
    recipients = config.get("recipients", [])
    if not recipients:
        fail("No recipients configured in config.yaml.")

    resp = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "from": sender,
            "to": recipients,
            "subject": subject,
            "html": html,
        },
        timeout=60,
    )
    if resp.status_code >= 300:
        fail(f"Resend API error {resp.status_code}: {resp.text}")
    print(f"Email sent to {', '.join(recipients)} (Resend id: {resp.json().get('id')})")


NO_ALERTS_SENTINEL = "NO_ALERTS"


def build_alert_prompt(
    config: dict,
    now_local: datetime,
    knowledge_base: str,
    news_items: "list[dict] | None" = None,
) -> str:
    """Short-window prompt: only surface HIGH-VALUE breaking undercut events."""
    alerts_cfg = config.get("alerts", {})
    lookback = int(alerts_cfg.get("lookback_hours", 6))
    since = now_local - timedelta(hours=lookback)
    watchlist = config.get("watchlist", [])
    names = ", ".join(w.get("name", "?") for w in watchlist) or "(none)"

    triggers = config.get("undercut", {}).get("alert_triggers", [])
    trigger_lines = "\n".join(f"  - {t}" for t in triggers) or "  - (none specified)"

    window = (
        f"{since.strftime('%Y-%m-%d %H:%M %Z')} to "
        f"{now_local.strftime('%Y-%m-%d %H:%M %Z')}"
    )

    kb_block = (
        f"\n<knowledge_base>\n{knowledge_base}\n</knowledge_base>\n"
        if knowledge_base
        else ""
    )

    if news_items:
        source_instr = (
            "A set of PRE-FETCHED, dated news items from the alert window is provided "
            "below in <fresh_news>. Consider ONLY these items. Do not search or invent. "
            "Select ONLY those that are genuinely HIGH-VALUE breaking triggers.\n\n"
            f"<fresh_news>\n{format_news_block(news_items)}\n</fresh_news>\n"
        )
    else:
        source_instr = "Search the web to verify candidate events.\n"

    return f"""You are a competitive-intelligence analyst at Kore.ai running a \
RAPID ALERT sweep. Only surface HIGH-VALUE, time-sensitive, breaking events about \
our competitors that just happened in the window {window} (last {lookback} hours). \
This is NOT the daily digest — be ruthless. Routine product blog posts, minor \
updates, and anything older than the window do NOT qualify.

Competitors: {names}

An event qualifies ONLY if it is one of these high-value triggers and is genuinely \
breaking:
{trigger_lines}
{kb_block}
{source_instr}
If — and only if — you find one or more qualifying events, \
output ONLY a fenced ```json code block containing a JSON array of event objects. \
Each object MUST have these string keys:
- "competitor": the competitor name
- "headline": one-line description of the event
- "url": a real, working source URL (never fabricate)
- "trigger": which trigger category it matches
- "why_urgent": one line on why it matters now
- "play": the single sharpest action, prefixed with one of 🟦 Sales / 🟩 PMM / 🟪 AR / 🟧 Product

Output nothing outside the ```json block.

If there are NO qualifying high-value events in the window, output EXACTLY this and \
nothing else:
{NO_ALERTS_SENTINEL}

Never fabricate events or URLs. When in doubt, output {NO_ALERTS_SENTINEL}."""


UNGROUNDED_BANNER = (
    "> ⚠️ **KB-only run — no live web search succeeded.** The model returned no "
    "grounding sources this run (likely free-tier throttling falling back to a "
    "non-searching model), so the items below are drawn from the internal "
    "knowledge base, not fresh search results. **Treat dates and \"news\" as "
    "unverified / possibly stale.** Enable billing for reliable grounded search.\n\n"
    "---\n\n"
)


def run_daily(config: dict, now_local: datetime, knowledge_base: str, dry_run: bool) -> None:
    guard = config.get("grounding", {})
    news_items = fetch_news(config, now_local)

    if news_items:
        # Freshness comes from the RSS feed; the model only synthesises (no search).
        prompt = build_prompt(config, now_local, knowledge_base, news_items=news_items)
        digest, _ = generate_digest(config, prompt, use_search=False)
        grounded = len(news_items)
    else:
        # No pre-fetched news — fall back to model-side web search + grounding.
        print("No RSS news fetched; falling back to model web search.")
        prompt = build_prompt(config, now_local, knowledge_base)
        digest, grounded = generate_digest(config, prompt, use_search=True)

    if grounded == 0:
        print("WARNING: no grounding sources — this run did not perform live search.")
        digest = UNGROUNDED_BANNER + digest
        if guard.get("skip_if_ungrounded", False):
            save_digest(digest, now_local)
            print("skip_if_ungrounded is set — archiving but NOT emailing the KB-only digest.")
            return
    else:
        print(f"Grounded on {grounded} live source(s).")

    save_digest(digest, now_local)
    if dry_run:
        print("DIGEST_DRY_RUN set — skipping email.")
        return
    send_email(config, digest, now_local)
    print("Done.")


def _parse_alert_events(result: str) -> list[dict] | None:
    """Extract the JSON event array from the model output. None = unparseable."""
    match = re.search(r"```json\s*(.*?)\s*```", result, re.DOTALL)
    blob = match.group(1) if match else result
    blob = blob.strip()
    if not (blob.startswith("[") or blob.startswith("{")):
        start = blob.find("[")
        if start == -1:
            return None
        blob = blob[start:]
    try:
        data = json.loads(blob)
    except json.JSONDecodeError:
        return None
    if isinstance(data, dict):
        data = [data]
    return [e for e in data if isinstance(e, dict) and e.get("headline")]


def _fingerprint(event: dict) -> str:
    """Stable id for an event: competitor + normalized headline + url host/path."""
    comp = re.sub(r"\W+", "", str(event.get("competitor", "")).lower())
    head = re.sub(r"\W+", "", str(event.get("headline", "")).lower())[:60]
    url = re.sub(r"^https?://(www\.)?", "", str(event.get("url", "")).lower()).split("?")[0].rstrip("/")
    return hashlib.sha1(f"{comp}|{head}|{url}".encode()).hexdigest()[:16]


def _load_alert_state() -> dict:
    if not ALERT_STATE_PATH.exists():
        return {}
    try:
        return json.loads(ALERT_STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_alert_state(state: dict, now_utc: datetime) -> None:
    cutoff = now_utc - timedelta(days=ALERT_STATE_RETENTION_DAYS)
    pruned = {
        fp: ts
        for fp, ts in state.items()
        if _safe_dt(ts) is None or _safe_dt(ts) >= cutoff
    }
    ALERT_STATE_PATH.write_text(json.dumps(pruned, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _safe_dt(iso: str) -> datetime | None:
    try:
        return datetime.fromisoformat(iso)
    except Exception:
        return None


def _render_alert_markdown(events: list[dict], now_local: datetime) -> str:
    lines = [f"# 🚨 Undercut Alert — {now_local.strftime('%a %d %b %Y, %H:%M %Z')}", ""]
    for e in events:
        url = e.get("url", "")
        link = f" — [Source]({url})" if url else ""
        lines.append(f"- **{e.get('competitor', '?')} — {e.get('headline', '')}**{link}")
        if e.get("trigger"):
            lines.append(f"  - **Trigger:** {e['trigger']}")
        if e.get("why_urgent"):
            lines.append(f"  - **Why it's urgent:** {e['why_urgent']}")
        if e.get("play"):
            lines.append(f"  - **Undercut play:** {e['play']}")
    return "\n".join(lines)


def run_alerts(config: dict, now_local: datetime, knowledge_base: str, dry_run: bool) -> None:
    alerts_lookback = int(config.get("alerts", {}).get("lookback_hours", 6))
    news_items = fetch_news(config, now_local, lookback_hours=alerts_lookback)

    if news_items:
        prompt = build_alert_prompt(config, now_local, knowledge_base, news_items=news_items)
        result, _ = generate_digest(config, prompt, use_search=False)
    else:
        # No fresh RSS items in the short window → nothing to alert on. An alert
        # without live, dated sourcing can't be trusted, so suppress.
        print("No fresh RSS items in the alert window — suppressing.")
        return

    head = result.split("\n", 1)[0].strip()
    if result.strip() == NO_ALERTS_SENTINEL or head == NO_ALERTS_SENTINEL:
        print("No high-value alert events found — nothing to send.")
        return

    events = _parse_alert_events(result)
    if events is None:
        # Couldn't parse structured events; fall back to sending raw (no dedup)
        # rather than swallow a possible real alert.
        print("Could not parse structured events — sending raw alert (no dedup).")
        if dry_run:
            print("DIGEST_DRY_RUN set — skipping alert email.\n\n" + result)
            return
        _send_alert(config, result, now_local)
        return

    now_utc = datetime.now(timezone.utc)
    state = _load_alert_state()
    new_events = [e for e in events if _fingerprint(e) not in state]
    if not new_events:
        print(f"All {len(events)} alert event(s) already sent previously — nothing new.")
        return

    markdown = _render_alert_markdown(new_events, now_local)
    print(f"{len(new_events)} new alert event(s) (of {len(events)} found).")
    if dry_run:
        print("DIGEST_DRY_RUN set — skipping email + state write.\n\n" + markdown)
        return

    _send_alert(config, markdown, now_local)
    for e in new_events:
        state[_fingerprint(e)] = now_utc.isoformat()
    _save_alert_state(state, now_utc)
    print("Alert email sent; state updated.")


def _send_alert(config: dict, markdown: str, now_local: datetime) -> None:
    subject_prefix = config.get("alerts", {}).get("subject_prefix", "🚨 Undercut Alert —")
    subject = f"{subject_prefix} {now_local.strftime('%a %d %b, %H:%M')}"
    send_email(config, markdown, now_local, subject=subject)


def main() -> None:
    config = load_config()
    tz_name = config.get("timezone", "Asia/Kolkata")
    now_local = local_now(tz_name)

    knowledge_base = load_knowledge_base()
    if knowledge_base:
        print(f"Loaded knowledge base ({len(knowledge_base)} chars).")

    dry_run = os.environ.get("DIGEST_DRY_RUN", "").lower() in {"1", "true", "yes"}
    mode = os.environ.get("DIGEST_MODE", "daily").strip().lower()
    print(f"Run mode: {mode}")

    if mode == "alerts":
        run_alerts(config, now_local, knowledge_base, dry_run)
    else:
        run_daily(config, now_local, knowledge_base, dry_run)


if __name__ == "__main__":
    main()
