# SQL-1

## 🤖 Agentic AI Daily Digest

An **undercut engine** for the enterprise CX / contact-center / agentic-AI market.
It emails a **deep-dive daily digest** that doesn't just report competitor news — it
turns each development into an **attack angle + Kore.ai counter + team-tagged play**
(Sales / PMM / Analyst Relations / Product). A separate **rapid-alert sweep** fires an
immediate email when a high-value competitor event breaks.

- **Brain:** Gemini with Google Search grounding (live web research).
- **Memory:** a [`knowledge_base/`](knowledge_base/) of Kore.ai positioning + living
  competitor battlecards, injected into every run.
- **Delivery:** email via [Resend](https://resend.com).
- **Digest:** GitHub Actions cron every 12h at `02:30` & `14:30 UTC` (~08:00 & 20:00 IST).
  Hero section: **⚔️ Undercut Opportunities.** Archived to [`digests/`](digests/) as both
  `YYYY-MM-DD-HHMM.md` and a **PDF** (Inter Tight, blue + black) which is also attached to the email.
- **Rapid alerts:** GitHub Actions cron every 4 hours (`DIGEST_MODE=alerts`); emails
  **only** when a high-value trigger (price change, outage, exec exit, lost logo,
  analyst downgrade, M&A) is genuinely breaking — otherwise sends nothing.

### How it works

```
config.yaml ──▶ digest_agent.py ──▶ Gemini (Google Search) ──▶ Markdown digest
                                                                   │
                                          ┌────────────────────────┴───────────┐
                                          ▼                                     ▼
                                 digests/YYYY-MM-DD-HHMM.md            Resend email → you
```

### Configure what it tracks

Everything lives in [`config.yaml`](config.yaml) — no code changes needed:

- `recipients` — who gets the email.
- `topics` — the broad areas swept daily.
- `watchlist` — **your competitor list.** Each entry has a `name` and a `focus`
  (what to emphasize, or `"anything notable"`).
- `model`, `lookback_hours`, `timezone` — tuning knobs.

### Knowledge base (the agent's "memory")

[`knowledge_base/`](knowledge_base/) holds standing context — Kore.ai's positioning
(`kore-ai.md`) and profiles of all tracked competitors (`competitors.md`). The agent
loads every `.md` file there and injects it into the prompt, so each digest is framed
by who we are, who we track, and each rival's documented strengths/gaps. Edit the
markdown directly to update the memory — no code changes needed.

### Setup (one-time)

1. **Get the keys**
   - `GEMINI_API_KEY` — from [Google AI Studio](https://aistudio.google.com/apikey).
   - `RESEND_API_KEY` — from [Resend](https://resend.com/api-keys). Sign up with
     **anuragblr19@gmail.com** so the default `onboarding@resend.dev` sender can
     reach your inbox without verifying a domain.

2. **Add them as GitHub repository secrets**
   Repo → **Settings → Secrets and variables → Actions → New repository secret**:
   - `GEMINI_API_KEY`
   - `RESEND_API_KEY`

3. **Get the workflow onto the default branch.**
   GitHub only runs `schedule:` cron jobs from the repo's **default branch**
   (`main`). Merge this branch into `main` for the daily run to fire.

4. **Test it** — Actions tab → **Agentic AI Daily Digest** → **Run workflow**.
   (Set `dry_run = true` to generate + commit without sending an email.)

### Run locally

```bash
pip install -r requirements.txt
cp .env.example .env          # then fill in your keys
set -a; source .env; set +a
python digest_agent.py        # add DIGEST_DRY_RUN=1 to skip the email
```

### Files

| File | Purpose |
|------|---------|
| `config.yaml` | Topics, watchlist, **undercut levers & alert triggers**, recipients, model. |
| `digest_agent.py` | The agent: research → undercut analysis → email (daily + alerts modes). |
| `knowledge_base/` | Kore.ai positioning + living competitor battlecards (the memory). |
| `.github/workflows/daily-digest.yml` | Digest cron (every 12h) + manual trigger. |
| `.github/workflows/undercut-alerts.yml` | Rapid-alert sweep every 4 hours. |
| `digests/` | Dated archive of every daily digest. |
| `alerts_state.json` | Dedup state for rapid alerts (auto-managed; prevents re-alerting the same event for 7 days). |

### Run modes

| Mode | How | What it does |
|------|-----|--------------|
| Daily digest | default (`DIGEST_MODE=daily`) | Full deep-dive with the Undercut Opportunities hero section; archived + emailed. |
| Rapid alerts | `DIGEST_MODE=alerts` | Short-window sweep; emails only on a breaking high-value trigger, else nothing. |
| Dry run | `DIGEST_DRY_RUN=1` | Generate without sending email (works in either mode). |
