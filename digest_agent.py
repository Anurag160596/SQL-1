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

import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
import yaml

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.yaml"
DIGESTS_DIR = ROOT / "digests"
KB_DIR = ROOT / "knowledge_base"
KB_CHAR_BUDGET = 24000  # cap KB text injected into the prompt


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


def build_prompt(config: dict, now_local: datetime, knowledge_base: str = "") -> str:
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

    today = now_local.strftime("%A, %d %B %Y")
    window = (
        f"{since.strftime('%Y-%m-%d %H:%M %Z')} to "
        f"{now_local.strftime('%Y-%m-%d %H:%M %Z')}"
    )

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

Use Google Search aggressively to find the most important, genuinely RECENT \
developments — prioritize the last {lookback} hours (window: {window}), and at \
most the last 3 days. Do not include stale or undated items as if they were news. \
If a section has nothing genuinely new, say so briefly rather than padding.
{kb_block}
## What to cover (sweep all of these)
{topic_lines}

## Competitor watchlist (give this its own prominent section)
Prioritize and specifically search for news about each of these companies:
{watch_lines}

## Output format (Markdown only — no preamble, no "here is your digest")
Start directly with an H1 title line. Structure:

# Agentic AI Daily Digest — {today}

**TL;DR** — 3-5 bullet points capturing the single most important things today.

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


def generate_digest(config: dict, prompt: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        fail("GEMINI_API_KEY is not set.")

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        fail("google-genai not installed. Run: pip install -r requirements.txt")

    model_name = os.environ.get("GEMINI_MODEL") or config.get("model", {}).get(
        "name", "gemini-2.5-flash"
    )
    temperature = float(config.get("model", {}).get("temperature", 0.4))

    client = genai.Client(api_key=api_key)
    search_tool = types.Tool(google_search=types.GoogleSearch())

    print(f"Generating digest with {model_name} (Google Search grounding)...")
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[search_tool],
            temperature=temperature,
        ),
    )

    text = (getattr(response, "text", None) or "").strip()
    if not text:
        fail("Gemini returned an empty digest.")

    sources = extract_sources(response)
    if sources:
        text += "\n\n---\n\n### 📎 Grounding sources\n" + "\n".join(
            f"- [{title}]({url})" for title, url in sources
        )
    return text


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
    out_path = DIGESTS_DIR / f"{now_local.strftime('%Y-%m-%d')}.md"
    out_path.write_text(markdown_text + "\n", encoding="utf-8")
    print(f"Saved digest to {out_path}")
    return out_path


def send_email(config: dict, markdown_text: str, now_local: datetime) -> None:
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


def main() -> None:
    config = load_config()
    tz_name = config.get("timezone", "Asia/Kolkata")
    now_local = local_now(tz_name)

    knowledge_base = load_knowledge_base()
    if knowledge_base:
        print(f"Loaded knowledge base ({len(knowledge_base)} chars).")
    prompt = build_prompt(config, now_local, knowledge_base)
    digest = generate_digest(config, prompt)
    save_digest(digest, now_local)

    dry_run = os.environ.get("DIGEST_DRY_RUN", "").lower() in {"1", "true", "yes"}
    if dry_run:
        print("DIGEST_DRY_RUN set — skipping email.")
        return
    send_email(config, digest, now_local)
    print("Done.")


if __name__ == "__main__":
    main()
