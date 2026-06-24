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

import base64
import concurrent.futures
import hashlib
import io
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
FONTS_DIR = ROOT / "assets" / "fonts"

# PDF palette: blue + black fonts only (per spec), Inter Tight throughout.
# A restrained, on-brand scale — every text colour is blue or black/near-black;
# greys are reserved for structural labels (eyebrows, meta, rules) as in the
# reference design. Priority dots use a blue-intensity scale (not traffic-light)
# to keep the strict blue+black palette.
PDF_BLUE = "#1d4ed8"          # primary accent (kore.ai blue)
PDF_BLUE_SOFT = "#93b4f5"     # muted blue (Med priority)
PDF_BLACK = "#0b0f19"         # near-black for headings/body
PDF_INK = "#1f2430"           # body text
PDF_GREY = "#6b7280"          # eyebrows / meta / secondary
PDF_GREY_SOFT = "#9aa3b2"     # Low priority dot
PDF_RULE = "#e2e6ee"          # hairline rules / borders (neutral grey)
PDF_CARD_BORDER = "#d7deea"   # card border (neutral grey, not blue)
PDF_CARD_BG = "#ffffff"       # signal-card fill: white, separated by borders
PDF_CALLOUT_BG = "#f4f7fd"    # bottom-line / caveat box fill (very faint)

# Strip emoji/pictographs so the PDF stays strictly blue + black (no color glyphs
# / tofu boxes). The descriptive text after each emoji is preserved.
_EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF"
    "\U00002190-\U000021FF\U00002B00-\U00002BFF\U00002300-\U000023FF️]",
    flags=re.UNICODE,
)


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


# ------------------------------------------------------------
# Accuracy governance layer
# Vets fetched items before they reach the writer: a deterministic
# source-quality + scope gate, then a model review that confirms each item is
# genuinely ABOUT the named competitor and on-topic. Misattributions
# (e.g. an Anthropic/Claude story filed under "Sierra"), look-alike companies,
# and finance/SEO filler are dropped here so they can never enter the digest.
# ------------------------------------------------------------

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def _domain(url: str) -> str:
    try:
        host = urllib.parse.urlparse(url).netloc.lower()
    except Exception:
        return ""
    return host[4:] if host.startswith("www.") else host


def _fetch_article_excerpt(url: str, timeout: int, max_chars: int = 1500) -> str:
    """Best-effort: fetch an article and return a plain-text excerpt. Returns ""
    on any failure (the reviewer then judges from the headline + source)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (digest-agent)"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read(400_000)
        html = raw.decode("utf-8", errors="ignore")
        # Drop scripts/styles, then strip tags.
        html = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", html)
        text = _WS_RE.sub(" ", _TAG_RE.sub(" ", html)).strip()
        return text[:max_chars]
    except Exception:
        return ""


def _extract_json_array(text: str) -> "list | None":
    """Pull a JSON array out of a model response (tolerant of code fences/prose)."""
    m = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    blob = m.group(1) if m else text
    start, end = blob.find("["), blob.rfind("]")
    if start == -1 or end <= start:
        return None
    try:
        data = json.loads(blob[start : end + 1])
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, list) else None


def _verify_review(config: dict, candidates: list[dict]) -> "dict[int, dict] | None":
    """Ask the model to vet each candidate. Returns {index: verdict} or None if
    the review itself could not be obtained (caller then fails safe)."""
    lines = []
    for c in candidates:
        ex = c.get("excerpt", "")
        ex = (" | excerpt: " + ex[:600]) if ex else ""
        lines.append(
            f'{{"i": {c["i"]}, "competitor": {json.dumps(c["competitor"])}, '
            f'"headline": {json.dumps(c["title"])}, "source": {json.dumps(c.get("source",""))}'
            f'}}  // {ex}'
        )
    drop_uncertain = config.get("verification", {}).get("drop_when_uncertain", True)
    uncertain_rule = ("When you are NOT confident, set keep=false."
                      if drop_uncertain else "When borderline, you may keep it.")
    prompt = f"""You are an ACCURACY-GOVERNANCE reviewer for a Kore.ai competitive- \
intelligence digest. You are given candidate news items, each tentatively tagged with a \
competitor name (from a news-search query that is often wrong). Decide which items may \
enter the digest.

KEEP an item ONLY if ALL of these hold:
1. ATTRIBUTION: the article is genuinely ABOUT the tagged competitor as a primary \
subject or direct actor — NOT a passing mention, NOT a different company, and NOT a \
different organisation that merely shares the name (e.g. a person, place, fund, or \
unrelated firm called the same thing).
2. TOPIC: it concerns enterprise conversational AI / contact-center / customer- \
experience / agentic AI.
3. SUBSTANCE: it is a real development (launch, funding, M&A, partnership, outage, exec \
move, analyst report, customer win, pricing change) — NOT a stock-price blurb, listicle, \
award roundup, generic survey, or SEO filler.
{uncertain_rule}

For EACH item return one JSON object with keys:
- "i": the item's index (integer, unchanged)
- "keep": true or false
- "subject": the actual primary company/entity the article is about (string)
- "reason": a short phrase justifying the decision

Output ONLY a JSON array of these objects — nothing else.

ITEMS:
[
{chr(10).join(lines)}
]"""
    try:
        text, _ = generate_digest(config, prompt, use_search=False)
    except SystemExit:
        return None
    except Exception as exc:
        print(f"  verification review error: {str(exc)[:120]}")
        return None
    arr = _extract_json_array(text)
    if arr is None:
        print("  verification: could not parse reviewer output.")
        return None
    verdicts: dict[int, dict] = {}
    for obj in arr:
        if isinstance(obj, dict) and isinstance(obj.get("i"), int):
            verdicts[obj["i"]] = obj
    return verdicts


def verify_news_items(config: dict, items: list[dict], now_local: datetime) -> list[dict]:
    """Governance gate between fetch and synthesis. Returns the vetted subset.

    Gate 1 (deterministic): drop blocked source domains and any item whose
    competitor is not on the watchlist.
    Gate 2 (model review): drop items the reviewer judges misattributed, off-topic,
    or insubstantial. Fails SAFE — if the review can't be obtained, keep the
    domain/scope-filtered items rather than emitting nothing.
    """
    vcfg = config.get("verification", {})
    if not vcfg.get("enabled", True) or not items:
        return items

    scfg = config.get("sources", {})
    blocked = {d.lower() for d in scfg.get("blocked_domains", [])}
    blocked_names = [s.lower() for s in scfg.get("blocked_sources", [])]
    watch = {w.get("name", "") for w in config.get("watchlist", [])}

    # --- Gate 1: source-quality + scope ---
    # Note: Google News RSS links are news.google.com redirects, so the publisher
    # is identified by the RSS <source> NAME, not the URL domain — name-match first.
    gate1: list[dict] = []
    for it in items:
        src_name = (it.get("source") or "").lower()
        hit = next((b for b in blocked_names if b and b in src_name), None)
        if hit:
            print(f"  drop (blocked source '{it.get('source')}'): {it['title'][:70]}")
            continue
        dom = _domain(it.get("url", ""))
        if dom and any(dom == b or dom.endswith("." + b) for b in blocked):
            print(f"  drop (blocked domain {dom}): {it['title'][:70]}")
            continue
        if watch and it.get("competitor") not in watch:
            print(f"  drop (off-watchlist {it.get('competitor')!r}): {it['title'][:60]}")
            continue
        gate1.append(it)
    if not gate1:
        return []

    # --- Optional: fetch article text so the reviewer judges on real content ---
    if vcfg.get("fetch_articles", True):
        timeout = int(vcfg.get("fetch_timeout_seconds", 6))
        urls = [it.get("url", "") for it in gate1]
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
                excerpts = list(ex.map(lambda u: _fetch_article_excerpt(u, timeout), urls))
            for it, exc in zip(gate1, excerpts):
                it["excerpt"] = exc
        except Exception as exc:
            print(f"  article prefetch skipped: {str(exc)[:80]}")

    # --- Gate 2: model attribution/relevance review ---
    candidates = [
        {"i": idx, "competitor": it.get("competitor", ""), "title": it.get("title", ""),
         "source": it.get("source", ""), "excerpt": it.get("excerpt", "")}
        for idx, it in enumerate(gate1)
    ]
    verdicts = _verify_review(config, candidates)
    if verdicts is None:
        # Fail safe: reviewer unavailable — keep the gate-1 set (still source/scope-clean).
        print("Verification review unavailable — keeping source/scope-filtered items.")
        for it in gate1:
            it.pop("excerpt", None)
        return gate1

    kept: list[dict] = []
    for idx, it in enumerate(gate1):
        it.pop("excerpt", None)
        v = verdicts.get(idx)
        if v is None:
            if vcfg.get("drop_when_uncertain", True):
                print(f"  drop (no verdict): {it['title'][:70]}")
                continue
            kept.append(it)
            continue
        if v.get("keep") is True:
            kept.append(it)
        else:
            subj = v.get("subject", "?")
            print(f"  drop (review: about {subj!r}; {v.get('reason','')[:60]}): "
                  f"{it.get('competitor')} — {it['title'][:60]}")
    print(f"Verification: {len(items)} fetched -> {len(gate1)} after source/scope "
          f"-> {len(kept)} verified.")
    return kept


def _norm_url(u: str) -> str:
    """Host + path, lowercased, no query/fragment/trailing slash — for matching a
    model-written URL back to a verified source item despite ?oc=5-style variation."""
    try:
        p = urllib.parse.urlparse(u.strip())
    except Exception:
        return u.strip().lower()
    return (p.netloc.lower() + p.path.rstrip("/")).lower()


def bind_links(digest_md: str, verified_items: list[dict]) -> str:
    """Deterministic link governance: keep a Markdown hyperlink ONLY if its URL
    matches one of the verified source items; otherwise drop the hyperlink and keep
    the plain text. This guarantees the digest can never show a hallucinated or
    mismatched URL (e.g. a 'Petty Products / Agentforce' citation that secretly
    points at a Decagon valuation page)."""
    if not verified_items:
        return digest_md
    allowed = {_norm_url(it.get("url", "")) for it in verified_items if it.get("url")}
    dropped = 0

    def _repl(m: "re.Match") -> str:
        nonlocal dropped
        text, url = m.group(1), m.group(2)
        if _norm_url(url) in allowed:
            return m.group(0)
        dropped += 1
        return text  # unlink: keep the publication name, drop the bad URL

    out = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", _repl, digest_md)
    if dropped:
        print(f"Link governance: unlinked {dropped} URL(s) not matching a verified source.")
    return out


def ground_digest(config: dict, digest_md: str, verified_items: list[dict]) -> str:
    """Output-grounding governance: rewrite the finished digest so every dated
    'What happened' claim and every priority-table row is supported by one of the
    VERIFIED source items — deleting any claim, row, signal, or company drawn from
    background knowledge rather than the actual news. Single best-effort model call;
    on any failure it returns the digest unchanged (the input gates already ran)."""
    if not config.get("verification", {}).get("audit_output", True) or not verified_items:
        return digest_md
    allowed = "\n".join(
        f"- {it.get('competitor','')} | {it.get('date','')} | "
        f"{it.get('source','')} | {it.get('title','')}"
        for it in verified_items
    )
    prompt = f"""You are an accuracy editor. Below is (A) the COMPLETE list of verified \
news items that are allowed to appear as "news", and (B) a competitive-intelligence \
digest in Markdown.

Rewrite the digest so that EVERY dated "What happened" sentence and EVERY row of the \
priority table is directly supported by one of the verified items in (A). Apply these \
edits and NOTHING else:
- DELETE any signal, table row, "Watch for" bullet, or Sources entry whose factual \
event is NOT in (A) — including claims clearly drawn from background knowledge (e.g. a \
"multi-month outage", "lacks analyst validation", a pricing change) that no verified \
item reports.
- If deleting leaves a company with nothing, remove that company entirely.
- Keep all SUPPORTED content verbatim. Do NOT add new facts, companies, dates, or \
links. Keep the exact same section structure and headings.
- The "What it means for Kore.ai" / "Kore.ai counter" framing may stay (it is opinion, \
not news), as long as its companion "What happened" fact is supported.
- If, after deletions, very little remains, that is correct — keep the bottom line \
honest about a thin window. Never re-pad.

Output ONLY the corrected Markdown digest — no preamble, no commentary.

(A) VERIFIED ITEMS:
{allowed}

(B) DIGEST:
{digest_md}"""
    try:
        revised, _ = generate_digest(config, prompt, use_search=False)
    except SystemExit:
        return digest_md
    except Exception as exc:
        print(f"  output-grounding skipped: {str(exc)[:100]}")
        return digest_md
    revised = (revised or "").strip()
    # Sanity: a valid rewrite still starts with the H1 and isn't suspiciously tiny.
    if not revised.startswith("#") or len(revised) < 200:
        print("  output-grounding produced an unexpected result — keeping original.")
        return digest_md
    print("Output-grounding pass complete.")
    return revised


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
3. These items were ALREADY vetted by an accuracy-governance layer for \
attribution and relevance. Still, attribute each item to a competitor ONLY if it is \
genuinely ABOUT that competitor; if anything looks mis-tagged, DROP it.
4. WATCHLIST-ONLY (critical): every competitor you name — in the signals, the priority \
table, anywhere — MUST be one of the watchlist companies listed below, spelled exactly. \
NEVER introduce, name, or create a row for any company that is not on the watchlist \
(no MoEngage, no eGain, no Zoom, no Anthropic, etc.), even if it appears inside a \
headline. If an item is really about a non-watchlist company, drop it.
5. Relevance: keep only items relevant to enterprise CX / contact-center / agentic \
AI. Drop unrelated items (sports sponsorships, manufacturing, generic stock blurbs).
6. Judgement is yours: pick the most important items, group/synthesise them, and \
frame the undercut angle using the knowledge base. You may drop trivial items.
7. Honesty over volume: if <fresh_news> is thin or has nothing material, say \
"Nothing material in the window" rather than padding. Never fabricate a date, a link, \
or a development to fill space.
8. OMIT, don't pad: if a watchlist company has NO item in <fresh_news>, give it NO \
signal and NO table row. Cover only companies that actually have a fresh item — three \
real rows beat ten invented ones.
9. GROUNDING (critical): every "What happened" sentence and every table row MUST be \
traceable to a SPECIFIC <fresh_news> item, and MUST use that item's source name and \
link. NEVER turn a knowledge-base weakness into a dated event — e.g. do NOT write \
"Genesys had a multi-month outage" or "Parloa lacks analyst validation" as today's news \
unless an actual <fresh_news> item reports exactly that. The knowledge base is for \
"What it means for Kore.ai" framing ONLY, never for the "What happened" fact.

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

## Output format — Competitive Signal Report (Markdown only; no preamble)
AUDIENCE: **Kore.ai executives.** This is a polished, board-ready competitive \
**Signal Report**, NOT a news list. Apply the **Pyramid Principle (Minto / McKinsey)**: \
lead with the answer, then support with MECE grouped arguments — synthesize, never a \
flat chronological list. Apply the **7 Cs**: clear, concise, concrete (names/numbers/ \
dates), correct (every claim sourced and in-window), coherent, complete, courteous \
(professional, board tone). Every factual claim carries an in-window **(YYYY-MM-DD)** \
date and a working source link whose text is the **publication name** (e.g. \
`[Reuters](url)`), never a raw URL. Follow the exact skeleton below — same headings, \
same order. Start directly with the H1.

# Competitive Signal Report — Enterprise AI Platform ({today})

> **Bottom line:** 1–2 sentences — the single most important strategic takeaway from \
today's competitive moves and what it means for Kore.ai. (Markdown blockquote, starting \
with `> **Bottom line:**`.)

## Three signals that matter
The **three most important** moves this run, each as its own block. For EACH signal use \
exactly this shape (the title is an H3 whose final 2–4 words are the sharp insight; the \
two bold labels MUST appear verbatim, each starting its own line):

### {{Short insight headline for signal 1}}
**What happened —** (YYYY-MM-DD) one or two concrete sentences with names/numbers, \
ending in a `[Publication](url)` link.
**What it means for Kore.ai —** one or two sentences: the threat/opening AND the \
specific Kore.ai counter or positioning move (grounded in a real proof point).

### {{Short insight headline for signal 2}}
**What happened —** …
**What it means for Kore.ai —** …

### {{Short insight headline for signal 3}}
**What happened —** …
**What it means for Kore.ai —** …

(If fewer than three material signals exist this run, output only the ones that are \
real — never pad.)

## Signal priority table
A Markdown TABLE of the run's material competitor moves — one row each, highest threat \
first. Use exactly these columns:

| Competitor | Move (dated) | Threat | Kore.ai counter |
|---|---|---|---|
| Five9 | (2026-06-23) Launched Voice AI Agents — [Business Wire](url) | High | Determinism + cost-per-outcome vs. seat model |

- **Move (dated)** starts with **(YYYY-MM-DD)** and ends with a `[Publication](url)` link.
- **Threat** = exactly one of `High` / `Med` / `Low` (Kore.ai's exposure).
- **Kore.ai counter** = one short clause, grounded in a real proof point.
- Only in-window, sourced rows. If nothing material this run, write one line saying so.

## Watch for
**2–4 short bullets** — developing situations to monitor (not yet material, but could \
become so). One line each. Omit the section entirely if there is nothing to watch.

## Recommended actions
**3–5 decision-oriented bullets** — the OVERALL actions for Kore.ai now (messaging to \
push, analyst narrative to seed, capability gap to close, deal play to arm). \
Do NOT tag actions by department/owner — keep them company-level.

## Sources
The underlying items as compact one-liners, each linked by publication name.

## Rules
- Pyramid discipline: bottom line first, then the three signals, then the table.
- Use H3 (`###`) ONLY for the three signal headlines — nowhere else.
- 7 Cs throughout; concise — short cells, specifics over adjectives.
- Every claim sourced and within the window; never fabricate. If nothing is material \
this run, say so in the Bottom line and keep it short."""


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
        # Gemini exhausted (free-tier 503/429). Fall back to OpenRouter, which has
        # separate capacity. Fine for our primary path since the model is given the
        # pre-fetched RSS news and doesn't need Google Search grounding here.
        text = _generate_openrouter(config, prompt, temperature)
        if text:
            return text, 0
        fail(f"All Gemini candidates failed ({', '.join(candidates)}) and OpenRouter "
             f"fallback unavailable/failed. Last Gemini error: {last_err}")

    text = (getattr(response, "text", None) or "").strip()
    if not text:
        fail("Gemini returned an empty digest.")

    sources = extract_sources(response)
    if sources:
        text += "\n\n---\n\n## 📎 Grounding sources\n" + "\n".join(
            f"- [{title}]({url})" for title, url in sources
        )
    # Return the live-search source count so callers can gate on grounding:
    # zero sources means the model answered without web search (likely recycling
    # the knowledge base), so the digest must not be presented as fresh news.
    return text, len(sources)


def _generate_openrouter(config: dict, prompt: str, temperature: float) -> str | None:
    """Fallback brain via OpenRouter (OpenAI-compatible). Tries each configured
    model in order. Returns the digest text, or None if unavailable/failed."""
    key = os.environ.get("OPEN_ROUTER_API_KEY")
    if not key:
        return None
    models = config.get("openrouter", {}).get(
        "models", ["openai/gpt-4o-mini", "google/gemini-2.0-flash-001"]
    )
    for model in models:
        print(f"Gemini exhausted — trying OpenRouter model {model}...")
        try:
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/Anurag160596/SQL-1",
                    "X-Title": "Agentic AI Digest",
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature,
                },
                timeout=120,
            )
        except Exception as exc:
            print(f"  OpenRouter {model} request error: {str(exc)[:120]}")
            continue
        if resp.status_code >= 300:
            print(f"  OpenRouter {model} -> {resp.status_code}: {resp.text[:160]}")
            continue
        try:
            text = (resp.json()["choices"][0]["message"]["content"] or "").strip()
        except Exception as exc:
            print(f"  OpenRouter {model} parse error: {str(exc)[:120]}")
            continue
        if text:
            print(f"  -> synthesized via OpenRouter:{model}")
            return text
    return None


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


# Small gray uppercase "eyebrow" labels injected above known sections, mirroring
# the reference report's two-tier (eyebrow + heading) section style. Matched by a
# lowercase substring of the H2 text; unmatched H2s simply render without one.
_SECTION_EYEBROWS = [
    ("three signals", "WHAT MATTERS THIS RUN"),
    ("signal priority", "AT A GLANCE"),
    ("watch for", "ON THE RADAR"),
    ("recommended actions", "SO WHAT — DO THIS NOW"),
    ("sources", "EVIDENCE TRAIL"),
    ("grounding sources", "EVIDENCE TRAIL"),
]


def _wordmark_html() -> str:
    """kore.ai text wordmark: black 'kore' + blue '.ai' (on-brand, no logo asset)."""
    return (
        f"<span style='font-weight:bold;color:{PDF_BLACK};font-size:11pt;'>kore"
        f"<span style='color:{PDF_BLUE};'>.ai</span></span>"
    )


def _build_cover_html(title_text: str, now_local: datetime, config: dict) -> str:
    """Styled cover block that replaces the model's first H1: blue eyebrow, big
    title with the final keyword in blue, and a grey meta line."""
    lookback = int((config or {}).get("lookback_hours", 72))
    # Trim any "— …" / "(…)" suffix so the big title stays short like the reference
    # (the topic/date live in the meta line and running header).
    short = re.split(r"\s+[—\-(]", title_text)[0].strip() or title_text
    # Highlight the keyword "Signal" in blue (fallback: the last word).
    if re.search(r"\bSignal\b", short):
        title_html = re.sub(r"\b(Signal)\b", rf"<span style='color:{PDF_BLUE};'>\1</span>", short, count=1)
    else:
        bits = short.rsplit(" ", 1)
        title_html = (f"{bits[0]} <span style='color:{PDF_BLUE};'>{bits[1]}</span>"
                      if len(bits) == 2 else short)
    date_str = now_local.strftime("%A, %d %B %Y · %H:%M %Z")
    return (
        "<div class='cover'>"
        "<div class='eyebrow' style='color:{blue};'>KORE.AI COMPETITIVE INTELLIGENCE</div>"
        "<div class='cover-title'>{title}</div>"
        "<div class='cover-meta'>Topic: Enterprise agentic AI &amp; contact-center AI (CCAI) &nbsp;·&nbsp; "
        "Window: last {lb}h &nbsp;·&nbsp; {date}</div>"
        "<div class='cover-meta'>Prepared by Kore.ai Competitive Intelligence</div>"
        "</div>"
    ).format(blue=PDF_BLUE, title=title_html, lb=lookback, date=date_str)


def _postprocess_html(body_html: str, now_local: datetime, config: dict) -> str:
    """Transform the plain markdown HTML into the polished report layout:
    cover block, eyebrow labels, signal cards, and priority-dot threat cells."""
    # 1) Replace the first H1 with the styled cover block.
    m = re.search(r"<h1>(.*?)</h1>", body_html, re.DOTALL)
    if m:
        cover = _build_cover_html(re.sub(r"<.*?>", "", m.group(1)).strip(), now_local, config)
        body_html = body_html[: m.start()] + cover + body_html[m.end():]

    # 2) Inject grey eyebrow labels above known H2 sections.
    def _eyebrow(match: "re.Match") -> str:
        heading = match.group(1)
        plain = re.sub(r"<.*?>", "", heading).strip().lower()
        for needle, label in _SECTION_EYEBROWS:
            if needle in plain:
                return f"<div class='eyebrow'>{label}</div><h2>{heading}</h2>"
        return f"<h2>{heading}</h2>"

    body_html = re.sub(r"<h2>(.*?)</h2>", _eyebrow, body_html, flags=re.DOTALL)

    # 3) Wrap each H3 block (a "signal") and its following content (up to the next
    #    H3/H2/eyebrow/end) in a card div.
    body_html = re.sub(
        r"(<h3>.*?</h3>)(.*?)(?=(<h3>|<h2>|<div class='eyebrow'>|$))",
        r"<div class='card'>\1\2</div>",
        body_html,
        flags=re.DOTALL,
    )

    # 4) Inside cards, restyle the two bold mini-labels so each starts a labelled line.
    body_html = body_html.replace(
        "<strong>What happened —</strong>",
        "<span class='lbl'>WHAT HAPPENED</span><br/><strong style='font-weight:normal'></strong>",
    ).replace(
        "<strong>What it means for Kore.ai —</strong>",
        "<span class='lbl lbl-blue'>WHAT IT MEANS FOR KORE.AI</span><br/>",
    )

    # 5) Turn Threat cells (High/Med/Low) into a priority indicator: a coloured
    #    left accent bar on the cell (reliable in xhtml2pdf, unlike inline-block
    #    chips) plus a blue-scale bold label. Stays within the blue+black palette.
    def _dot(match: "re.Match") -> str:
        val = match.group(1).strip().lower()
        bar, txt, label = {
            "high":   (PDF_BLUE,      PDF_BLUE,  "High"),
            "med":    (PDF_BLUE_SOFT, PDF_BLUE,  "Med"),
            "medium": (PDF_BLUE_SOFT, PDF_BLUE,  "Med"),
            "low":    (PDF_GREY_SOFT, PDF_GREY,  "Low"),
        }.get(val, (None, None, None))
        if not bar:
            return match.group(0)
        return (
            f"<td class='threat' style='border-left:4pt solid {bar};'>"
            f"<span style='color:{txt};font-weight:bold;'>{label}</span></td>"
        )

    body_html = re.sub(r"<td>\s*(High|Med|Medium|Low)\s*</td>", _dot, body_html, flags=re.IGNORECASE)
    return body_html


def render_pdf(markdown_text: str, now_local: datetime, config: dict | None = None) -> bytes | None:
    """Render the digest to a polished, blue+black, Inter Tight PDF that mirrors the
    Kore.ai 'Competitive Signal Report' design. Returns None on failure."""
    try:
        import markdown as md
        from xhtml2pdf import pisa
    except ImportError:
        print("PDF deps missing (xhtml2pdf/markdown); skipping PDF.")
        return None

    clean = _EMOJI_RE.sub("", markdown_text)
    body_html = md.markdown(clean, extensions=["extra", "sane_lists"])
    body_html = _postprocess_html(body_html, now_local, config or {})

    reg = (FONTS_DIR / "InterTight-Regular.ttf").as_uri()
    bold = (FONTS_DIR / "InterTight-Bold.ttf").as_uri()
    year = now_local.strftime("%Y")
    head_eyebrow = f"COMPETITIVE SIGNAL REPORT · ENTERPRISE AI PLATFORM · {now_local.strftime('%d %b %Y').upper()}"

    html = f"""<html><head><meta charset="utf-8"><style>
@page {{
  size: A4; margin: 2.5cm 1.6cm 1.9cm 1.6cm;
  @frame header_frame {{ -pdf-frame-content: headerContent; top: 1.0cm; left: 1.6cm; right: 1.6cm; height: 1.2cm; }}
  @frame footer_frame {{ -pdf-frame-content: footerContent; bottom: 1.0cm; left: 1.6cm; right: 1.6cm; height: 0.8cm; }}
}}
@font-face {{ font-family: 'Inter Tight'; src: url('{reg}'); font-weight: normal; }}
@font-face {{ font-family: 'Inter Tight'; src: url('{bold}'); font-weight: bold; }}
body {{ font-family: 'Inter Tight'; color: {PDF_INK}; font-size: 9.8pt; line-height: 1.45; }}

/* Running header */
#headerContent {{ width: 100%; }}
.hdr {{ width: 100%; border-bottom: 0.75pt solid {PDF_RULE}; padding-bottom: 3px; }}
.hdr td {{ border: none; padding: 0; }}
.hdr-eyebrow {{ color: {PDF_GREY}; font-size: 6.8pt; letter-spacing: 1.2px; }}

/* Footer */
#footerContent {{ color: {PDF_GREY}; font-size: 6.8pt; letter-spacing: 0.8px; text-align: right; }}

/* Cover block */
.cover {{ margin-bottom: 4px; }}
.eyebrow {{ color: {PDF_GREY}; font-size: 7pt; letter-spacing: 1.6px; font-weight: bold; margin-top: 14px; margin-bottom: 2px; }}
.cover-title {{ color: {PDF_BLACK}; font-size: 23pt; font-weight: bold; line-height: 1.1; margin: 1px 0 5px 0; }}
.cover-meta {{ color: {PDF_GREY}; font-size: 8.2pt; margin: 0; }}

/* Headings — clear section separation via generous top margin + thin rule */
h2 {{ color: {PDF_BLACK}; font-size: 13pt; font-weight: bold; margin: 6px 0 8px 0; padding-bottom: 4px; border-bottom: 0.75pt solid {PDF_RULE}; }}
h3 {{ color: {PDF_BLACK}; font-size: 10.5pt; font-weight: bold; margin: 0 0 5px 0; }}
a {{ color: {PDF_BLUE}; text-decoration: none; }}
strong, b {{ color: {PDF_BLACK}; font-weight: bold; }}
p {{ margin: 4px 0; }}
li {{ margin-bottom: 4px; }}
hr {{ border: none; border-top: 0.5pt solid {PDF_RULE}; margin: 12px 0; }}

/* Bottom-line callout — white with a strong blue left bar (kept very light, not a blue block) */
blockquote {{ background: {PDF_CALLOUT_BG}; border: 0.75pt solid {PDF_CARD_BORDER}; border-left: 4pt solid {PDF_BLUE}; margin: 10px 0 6px 0; padding: 9px 12px; color: {PDF_BLACK}; }}
blockquote strong {{ color: {PDF_BLUE}; }}
blockquote p {{ margin: 0; }}

/* Signal cards — WHITE fill, neutral grey border, blue left accent, clear gaps between */
.card {{ background: {PDF_CARD_BG}; border: 0.75pt solid {PDF_CARD_BORDER}; border-left: 3pt solid {PDF_BLUE}; padding: 9px 13px; margin: 11px 0; }}
.card h3 {{ color: {PDF_BLACK}; }}
.card p {{ margin: 4px 0; }}
.lbl {{ color: {PDF_GREY}; font-size: 6.6pt; letter-spacing: 1.2px; font-weight: bold; }}
.lbl-blue {{ color: {PDF_BLUE}; }}

/* Tables — white rows, neutral header band (blue kept to a thin accent rule), clear row separators */
table {{ border-collapse: collapse; width: 100%; font-size: 8.4pt; margin: 8px 0; }}
th {{ background: #f3f5fa; color: {PDF_BLACK}; text-align: left; padding: 6px 7px; font-weight: bold; font-size: 7.6pt; letter-spacing: 0.4px; border-bottom: 1.5pt solid {PDF_BLUE}; }}
td {{ padding: 6px 7px; border-bottom: 0.5pt solid {PDF_RULE}; vertical-align: top; color: {PDF_INK}; }}
td.threat {{ white-space: nowrap; font-weight: bold; color: {PDF_BLACK}; }}
</style></head><body>
<div id="headerContent">
  <table class="hdr"><tr>
    <td class="hdr-eyebrow" align="left">{head_eyebrow}</td>
    <td align="right">{_wordmark_html()}</td>
  </tr></table>
</div>
<div id="footerContent">© {year} KORE.AI · CONFIDENTIAL · ALL RIGHTS RESERVED · PAGE <pdf:pagenumber> / <pdf:pagecount></div>
{body_html}</body></html>"""

    buf = io.BytesIO()
    try:
        result = pisa.CreatePDF(src=html, dest=buf)
    except Exception as exc:
        print(f"PDF render failed: {str(exc)[:120]}")
        return None
    if result.err:
        print("PDF render reported errors; skipping PDF.")
        return None
    return buf.getvalue()


def save_pdf(pdf_bytes: bytes, now_local: datetime) -> Path:
    DIGESTS_DIR.mkdir(exist_ok=True)
    out_path = DIGESTS_DIR / f"{now_local.strftime('%Y-%m-%d-%H%M')}.pdf"
    out_path.write_bytes(pdf_bytes)
    print(f"Saved PDF to {out_path}")
    return out_path


def send_email(
    config: dict,
    markdown_text: str,
    now_local: datetime,
    subject: str | None = None,
    attachments: "list[dict] | None" = None,
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
  body {{ font-family: 'Inter Tight', -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
         line-height: 1.55; color: #1f2430; max-width: 720px; margin: 0 auto; padding: 20px 18px; }}
  h1 {{ font-size: 25px; color: #0b0f19; border-bottom: 2px solid #dbe3f4; padding-bottom: 10px; margin-bottom: 14px; }}
  h2 {{ font-size: 18px; color: #0b0f19; margin-top: 28px; margin-bottom: 6px; }}
  h3 {{ font-size: 15px; color: #1d4ed8; margin-top: 18px; margin-bottom: 4px; }}
  a {{ color: #1d4ed8; text-decoration: none; }}
  hr {{ border: none; border-top: 1px solid #dbe3f4; margin: 24px 0; }}
  code {{ background: #f4f4f4; padding: 1px 4px; border-radius: 4px; }}
  blockquote {{ background: #eef3fd; border-left: 4px solid #1d4ed8; margin: 14px 0;
                padding: 12px 16px; border-radius: 4px; }}
  blockquote strong {{ color: #1d4ed8; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 13px; margin: 12px 0; }}
  th {{ background: #1d4ed8; color: #ffffff; text-align: left; padding: 8px 10px; font-size: 12px; }}
  td {{ padding: 8px 10px; border-bottom: 1px solid #dbe3f4; vertical-align: top; }}
</style></head><body>{html_body}</body></html>"""

    email_cfg = config.get("email", {})
    if subject is None:
        subject_prefix = email_cfg.get("subject_prefix", "🤖 Agentic AI Daily —")
        subject = f"{subject_prefix} {now_local.strftime('%A, %d %b %Y')}"
    sender = email_cfg.get("from", "Agentic AI Digest <onboarding@resend.dev>")
    recipients = config.get("recipients", [])
    if not recipients:
        fail("No recipients configured in config.yaml.")

    payload = {
        "from": sender,
        "to": recipients,
        "subject": subject,
        "html": html,
    }
    if attachments:
        payload["attachments"] = attachments

    resp = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
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
    news_items = verify_news_items(config, news_items, now_local)

    if news_items:
        # Freshness comes from the RSS feed; the model only synthesises (no search).
        prompt = build_prompt(config, now_local, knowledge_base, news_items=news_items)
        digest, _ = generate_digest(config, prompt, use_search=False)
        # Output-grounding governance: strip any claim the writer invented from the
        # knowledge base so only verified-item facts survive.
        digest = ground_digest(config, digest, news_items)
        # Link governance: bind every hyperlink to a verified source URL; unlink the
        # rest so a hallucinated/mismatched URL can never appear.
        digest = bind_links(digest, news_items)
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

    # Render the PDF (Inter Tight, blue+black), archive it, and attach to the email.
    attachments = None
    pdf_bytes = render_pdf(digest, now_local, config)
    if pdf_bytes:
        save_pdf(pdf_bytes, now_local)
        attachments = [{
            "filename": f"agentic-ai-digest-{now_local.strftime('%Y-%m-%d-%H%M')}.pdf",
            "content": base64.b64encode(pdf_bytes).decode("ascii"),
        }]

    if dry_run:
        print("DIGEST_DRY_RUN set — skipping email.")
        return
    send_email(config, digest, now_local, attachments=attachments)
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
    news_items = verify_news_items(config, news_items, now_local)

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


def _is_paused(config: dict) -> bool:
    """True if config.pause_until is in the future (UTC). Used for one-off skips."""
    raw = config.get("pause_until")
    if not raw:
        return False
    try:
        pu = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    except Exception:
        print(f"Could not parse pause_until={raw!r}; ignoring.")
        return False
    if pu.tzinfo is None:
        pu = pu.replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) < pu:
        print(f"Paused until {pu.isoformat()} — skipping this run (no email).")
        return True
    return False


def main() -> None:
    config = load_config()

    # One-off pause: skip the whole run (no fetch, no model call, no email)
    # while pause_until is in the future. Self-clears once the time passes.
    if _is_paused(config):
        return

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
