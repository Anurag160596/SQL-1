# Knowledge Base — Agentic AI Competitive Intelligence (Kore.ai)

This folder is the **memory** for the daily digest agent. `digest_agent.py` loads
every `.md` file here and injects it into the model prompt as background context,
so each digest is grounded in who we are, who we track, and how we frame the market.

## Contents

| File | What's in it |
|------|--------------|
| `00-index.md` | This file. |
| `kore-ai.md` | Kore.ai's own positioning: platform, ABL, analyst standing, key terms. |
| `competitors.md` | **Living battlecards** for all 13 competitors, built to undercut. |

## Battlecard format (competitors.md)

Each competitor follows: **What it is → Exploitable weaknesses (by lever) →
Kore.ai counter & evidence → Sales trap questions → Undercut triggers to watch.**
This is what feeds the daily digest's **⚔️ Undercut Opportunities** section and the
rapid-alert sweep. Update a card and the next run uses it.

## How to maintain it

- **Edit the markdown directly** — no code changes needed. The agent re-reads it every run.
- Keep claims **sourced and dated**. Where a claim is Kore.ai's battlecard framing
  (i.e. one-sided positioning), it is labelled as such so the agent treats it as
  *positioning*, not neutral fact.
- When a competitor gets a new internal battlecard/deck, summarize the key points
  here so the agent picks it up.

## Provenance of this KB

Built from the user's own Google Drive + Notion materials (June 2026):
- `Kore.ai_vs_PolyAI_Analyst_Validation`, `Kore.ai_vs_Parloa_Analyst_Validation`
- `Kore_vs_Cresta_Exec`, `Kore_vs_Cresta_GoogleSlides`, `Cresta_vs_Kore_partner`
- Notion: "Cresta vs Conductor", "ABL Dynamic Value Instrument", "Google's OKF" notes

Competitors **without** an internal deck (Sierra, Decagon, Genesys, NICE/Cognigy,
Five9, Glean, Moveworks, Agentforce, ServiceNow, IBM) are profiled from general
market knowledge and flagged `⚠️ No internal battlecard yet — verify via web`.
The agent refreshes all of this with live web search at run time.
