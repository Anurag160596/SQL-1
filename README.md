# SQL-1

## 🤖 Agentic AI Daily Digest

A scheduled agent that emails you a **deep-dive daily digest** of news across the
Agentic AI space — model & lab releases, agent frameworks & tooling, research
papers, funding/product/industry moves, plus a **competitor watchlist** you control.

- **Brain:** Gemini with Google Search grounding (live web research).
- **Delivery:** email via [Resend](https://resend.com).
- **Schedule:** GitHub Actions cron at `02:30 UTC` (~08:00 IST), daily.
- **Archive:** every digest is committed to [`digests/`](digests/) as `YYYY-MM-DD.md`.

### How it works

```
config.yaml ──▶ digest_agent.py ──▶ Gemini (Google Search) ──▶ Markdown digest
                                                                   │
                                          ┌────────────────────────┴───────────┐
                                          ▼                                     ▼
                                 digests/YYYY-MM-DD.md                 Resend email → you
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
| `config.yaml` | Topics, competitor watchlist, recipients, model — your control panel. |
| `digest_agent.py` | The agent: research → markdown → save → email. |
| `.github/workflows/daily-digest.yml` | Daily cron + manual trigger. |
| `digests/` | Dated archive of every digest. |
