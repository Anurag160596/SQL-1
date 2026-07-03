# The Undercut Engine — a competitive-intelligence agent

**A product case study.** How I turned an ambiguous business problem — "we can't keep up with competitors" — into an autonomous AI system that produces owned decisions twice a day, and what product, strategy, and growth judgment went into it.

> **Format note:** this is written as a hiring case study, not a repo readme. It leads with the problem and the decisions, then shows the build. Reading time ≈ 6 minutes.

---

## TL;DR

- **Problem:** B2B competitive intelligence is slow, manual, and rarely actionable. Insight arrives late and with no owner.
- **What I built:** an agent that reads the enterprise-CX / agentic-AI market twice daily, turns each competitor move into an *attack angle + our counter + a team-tagged play*, and fires an immediate alert only when something high-value breaks.
- **The hard part (and the interesting part):** not the generation — the **judgment**. Precision over recall, decisions over headlines, resilience and honesty as first-class features.
- **Status:** live on a cron schedule since June 2026, running unattended, at near-zero marginal cost.

---

## 1. The opportunity

Every B2B company says it "tracks competitors." In practice that means a graveyard of Slack links, a battlecard deck last updated two quarters ago, and a monthly email nobody reads to the end. The intelligence exists — it's just late, unstructured, and un-owned. By the time a rival's pricing change reaches the AE who needed it, the deal is lost.

I refused to accept the problem as stated. The question isn't *"how do we track competitors better."* It's:

> **How do we turn every competitor move into a decision, assigned to an owner, within hours?**

That reframe is the entire product. Everything downstream — the accuracy layer, the team routing, the twice-daily cadence — falls out of taking *"decision with an owner, within hours"* literally.

## 2. Who it's for — the jobs to be done

One market event creates four different jobs, for four different teams:

| When a rival does this… | …this team has a job to do | …and needs this cut of the event |
|---|---|---|
| Ships performance-based pricing | **Sales** | a trap question for the next call |
| Repackages the platform | **Product Marketing** | counter-messaging, fast |
| Lands (or loses) an analyst nod | **Analyst Relations** | a validation angle to press |
| Launches a new capability | **Product** | a roadmap signal, prioritized |

A generic "here's the news" digest serves none of them well. So the agent writes the *same event four ways*, each tagged to the team that owns the response. Intelligence becomes action instead of a newsletter.

## 3. The product, in one move

Every signal is forced through the same shape — **threat → counter → owner** — before it's allowed into the digest. A real pairing the agent produced:

> **◤ Competitor signal.** Salesforce launched *Agentforce Help Agent* with **performance-based pricing** — a pull on enterprise budgets and a pricing-narrative land-grab.
>
> **◢ Our counter (routed to PMM + Sales).** Lead with **cost-per-outcome, determinism, and governance**. Sales trap question: *"When a prompt-built agent breaks a compliance step, do you find out at build time — or in production?"*

The daily digest leads with a **⚔️ Undercut Opportunities** hero section; a separate rapid-alert sweep runs every four hours and stays silent unless a high-value trigger (pricing change, outage, exec exit, lost logo, analyst downgrade, M&A) is genuinely breaking.

## 4. The product decisions — where the judgment lives

A demo generates text. A product makes decisions and lives with the tradeoffs. Here are the six that shaped this one.

**Decision 1 — Precision over recall.** Two verification gates (a deterministic source-quality filter, then a model review that confirms each item is genuinely *about* the named competitor) plus an output-grounding audit that deletes any claim not tied to a verified, dated source. *Traded coverage for trust the GTM team can quote in front of a customer.* A wrong battlecard is worse than a missing one.

**Decision 2 — Decisions, not headlines.** Every item must carry an attack angle, a counter, and a named team — or it doesn't ship. *Traded volume for the thing that actually changes what a team does Monday.* This is what keeps it from decaying into "another AI newsletter."

**Decision 3 — Config is the product surface.** The watchlist, the undercut levers the agent hunts for, and the alert triggers all live in a single YAML a non-engineer can edit. *Traded a slicker UI for a strategist who can retarget the entire engine in five minutes* — policy separated from mechanism.

**Decision 4 — Resilience is a feature.** A five-model fallback chain (Gemini → OpenRouter alternates), retry-with-exponential-backoff, and a 7-day dedup state so the same event never re-alerts. *Traded simplicity for a system that still delivers when a free-tier model 503s at 2am.* An unattended product that silently dies is worse than no product.

**Decision 5 — Honesty guardrails.** If the model didn't actually perform a live web search, the digest is banner-flagged "unverified" and breaking alerts are suppressed entirely. *Traded the appearance of always-on for output the reader never has to double-check.*

**Decision 6 — Zero-marginal-cost sourcing.** Fresh news comes from Google News RSS (free, no API key), fed to the model to synthesize rather than paying per search call. *Traded a premium data feed for a product that runs indefinitely at near-zero cost.*

## 5. How it works

```
config.yaml ─▶ fetch news (RSS) ─▶ [GATE] verify ─▶ synthesize ─▶ [GATE] ground ─▶ deliver (email + PDF)
  strategy         dated,            drop mis-        KB-grounded    delete un-        archived,
  layer            in-window         attributions     undercut       sourced           team-tagged,
                   items             & look-alikes    analysis       claims            on a schedule
```

- **Brain:** a model with live web-search grounding, model-agnostic behind a fallback chain.
- **Memory:** a knowledge base of 13 living competitor battlecards + our own positioning, injected into every run.
- **Delivery:** email plus a branded PDF, on a GitHub Actions cron — twice daily for the digest, every four hours for the alert sweep.

## 6. Outcomes & what I'd measure next

**Shipped and operating unattended** twice daily since June 2026, with a rolling dated archive and an alert channel that stays quiet unless something real breaks — all on a living base of 13 battlecards built from internal decks plus fresh web research.

If I owned this as a funded product, I'd move past shipping-metrics to **leading indicators of value**:

- **Play-adoption rate** — how often a routed play is actually used by the team it was sent to.
- **Time-from-event-to-action** — the metric the original reframe was built to shrink.
- **Battlecard win-rate** — do deals where the counter was used close at a higher rate?

…then feed those signals back to prioritize which undercut levers the engine hunts for. That loop — ship, measure the *outcome* not the output, re-prioritize — is how I'd run it as a product, not a project.

---

## What this case study is meant to show

| Discipline | Evidence in this build |
|---|---|
| **Product** | Problem reframing · jobs-to-be-done · explicit tradeoffs · shipped & operating |
| **Strategy** | 13-competitor market map · positioning wedges · war-gaming every move |
| **Growth** | Distribution by design · one system → four teams · near-zero marginal cost · leading-indicator metrics |

*Contact: anuragblr19@gmail.com*
