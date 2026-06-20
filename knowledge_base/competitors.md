# Competitor Battlecards

13 tracked competitors, each as a **living battlecard** built to undercut. Structure:
**What it is → Exploitable weaknesses (by lever) → Kore.ai counter & evidence →
Sales trap questions → Undercut triggers to watch.**

- **Battlecard framing** = Kore.ai's internal positioning (one-sided), strongest for the
  three we have decks on.
- `⚠️ No internal battlecard yet` = scaffolded from general market knowledge; the agent
  must verify/refresh via web search before any claim is used externally.

Undercut levers (shorthand used below): 💲 Pricing/TCO · 🔎 Proof/validation ·
📡 Channel/coverage · 🛡️ Reliability/governance · ✳️ Other.

Grouping: **CX-native agents** (Sierra, Decagon, Cresta, PolyAI, Parloa) ·
**CCaaS incumbents** (Genesys, NICE/Cognigy, Five9) ·
**Horizontal enterprise** (Glean, Moveworks) ·
**Big-tech platforms** (Agentforce, ServiceNow, IBM).

---

## Cresta · CX-native agents
**What it is:** Contact-center AI built on a conversation-data moat (millions of real
transcripts). Products: Insights, AI Analyst, Quality Management, Automation Discovery,
agent-assist, AI agents. Launched **Conductor** (Jun 11, 2026), a dev-native agent-build
environment + AI Agent Testing 2.0. Forrester-cited explainability. Customers: United,
Alaska, Cox.

**Exploitable weaknesses**
- 🛡️ Determinism/governance: prompt-plus-custom-code build surfaces broken handoffs,
  invalid tool refs and unreachable steps only at test/production, not build time. Cresta
  itself concedes the prompt-vs-code split is a manual call ("an IVR that calls an LLM" if
  over-coded).
- 💲 Pricing/TCO: flagged on pricing complexity / cost attribution.
- 📡 Scope: deep in conversation intelligence; less proven on full-lifecycle enterprise
  platform breadth (release engineering, cross-agent trace, model-agnostic tiering).

**Kore.ai counter & evidence:** ABL compiles — compile-time validation + zero-LLM
deterministic mode make critical/compliance paths guaranteed, not probabilistic.
Cross-agent trace trees, 100% conversation evaluation, Git-native releases, per-agent cost
attribution. Concede the data moat gracefully, reframe it as a *design input*, not a
substitute for production-grade reliability.

**Sales trap questions:** "When a prompt-built agent breaks a compliance step, do you find
out at build time or in production?" · "How is cost attributed per agent/intent/tool?"

**Triggers to watch:** Conductor customer proof points, pricing changes, new analyst
placements, expansion beyond conversation intelligence into full build/deploy.

## PolyAI · CX-native agents
**What it is:** Voice-first / voice-only customer-service automation, centered on inbound
voice.

**Exploitable weaknesses**
- 📡 Channel: narrow — lacks unified omnichannel across chat/messaging/digital.
- 💲 Pricing/TCO: consumption-based pricing with fewer cost-optimization options; Gartner
  notes long-term TCO can be "less predictable."
- 🛡️ Build dependency: agent creation leans on PolyAI's own teams/roadmap → slower
  iteration, vendor-dependent.

**Kore.ai counter & evidence:** One stack across voice **and** digital (Contact Center AI,
Agent AI, Quality AI, Outbound); voice-native (SSML, barge-in, sub-500ms) **plus**
cross-channel session resume. No-code/low-code self-service build. Predictable
deterministic-flow economics.

**Sales trap questions:** "What happens when a voice conversation needs to continue on
chat?" · "Can your business users build and change agents without the vendor?"

**Triggers to watch:** moves into digital/omnichannel, pricing changes, enterprise logos,
funding, first/again analyst placements.

## Parloa · CX-native agents
**What it is:** Voice-first contact-center AI; Gartner calls it an "AI Agent Management
Platform" with an agent-assist module (the **Arch** design layer).

**Exploitable weaknesses**
- 🔎 Proof/validation: **not evaluated** by Gartner MQ, either Forrester Wave, either
  Everest PEAK, or IDC MarketScape; near-zero third-party reviews (~1 verified G2 review).
- 📡 Coverage: limited geographic reach (customer base largely Europe — Gartner excluded it
  on geographic presence); narrower contact-center scope than a full enterprise platform.

**Kore.ai counter & evidence:** Leader across **six** analyst evaluations (Gartner,
Forrester x2, Everest x2, IDC). 80+ connectors, 250+ CRM/ERP integrations, prebuilt
vertical apps. Global enterprise deployments and deep third-party proof.

**Sales trap questions:** "Which independent analysts have evaluated their platform?" ·
"How many verified enterprise references can they show outside their home region?"

**Triggers to watch:** US/enterprise expansion, first analyst evaluations, funding, big
logos, reviews accumulating.

## Sierra · CX-native agents
⚠️ No internal battlecard yet — verify via web.
**What it is:** Conversational AI agent platform for CX (co-founded by Bret Taylor & Clay
Bavor); strong brand, very well funded.
- **Likely angles to probe:** 🔎 enterprise analyst validation vs. their brand/hype; 🛡️
  determinism/governance & auditability for regulated industries; 💲 outcome-based pricing
  predictability; 📡 depth of voice + true omnichannel + back-office integration breadth.
- **Kore.ai counter:** ABL determinism/governance, 6x analyst Leader status, 250+
  integrations, voice-native stack.
- **Triggers:** funding/valuation, enterprise wins, voice push, new products, first analyst
  recognition, pricing disclosures.

## Decagon · CX-native agents
⚠️ No internal battlecard yet — verify via web.
**What it is:** AI customer-service agents for enterprise support; fast-rising, notable
consumer-tech logos.
- **Likely angles:** 🔎 analyst validation & enterprise references at scale; 📡
  omnichannel + voice depth; 🛡️ governance/compliance for regulated verticals; 💲 pricing
  model maturity.
- **Kore.ai counter:** governed full-scope platform, analyst Leader proof, vertical apps.
- **Triggers:** funding/valuation, customer wins, voice/omnichannel expansion, platform
  launches.

## Genesys · CCaaS incumbent
⚠️ No internal battlecard yet — verify via web.
**What it is:** Major CCaaS incumbent (Genesys Cloud) layering AI agents/Copilot across CX.
- **Likely angles:** 🛡️ agentic depth/determinism of bolt-on AI vs. AI-native design; 💲
  total platform cost & migration friction; 🔎 proof that AI agents (not just routing) win
  vs. AI-native challengers.
- **Kore.ai counter:** AI-native agentic platform + ABL, multi-model routing, fast
  idea-to-live build.
- **Triggers:** AI agent product moves, Salesforce/other partnerships, earnings/IPO status,
  analyst placements, large deals.

## NICE (Cognigy) · CCaaS incumbent
⚠️ No internal battlecard yet — verify via web.
**What it is:** NICE (CXone, Enlighten AI) **acquired Cognigy** — a CCaaS giant +
enterprise conversational-AI combination. Track Cognigy news here.
- **Likely angles:** ✳️ acquisition-integration risk (roadmap churn, platform stitching);
  🛡️ governance across two stacks; 💲 bundled-suite cost & lock-in; 📡 unified agent
  experience vs. assembled parts.
- **Kore.ai counter:** single AI-native platform (not stitched), ABL determinism,
  provider-agnostic models, 6x analyst Leader status.
- **Triggers:** Cognigy↔CXone integration milestones, joint launches, enterprise deals,
  earnings, analyst positioning, exec moves post-acquisition.

## Five9 · CCaaS incumbent
⚠️ No internal battlecard yet — verify via web.
**What it is:** CCaaS provider with AI agents / intelligent virtual agents (Genius AI).
- **Likely angles:** 🛡️ agentic depth/determinism vs. AI-native; 💲 platform cost; 🔎
  analyst standing on agentic (vs. CCaaS) specifically.
- **Kore.ai counter:** AI-native + ABL, multi-model routing, full lifecycle depth.
- **Triggers:** AI agent releases, partnerships, enterprise wins, earnings, M&A.

## Glean · Horizontal enterprise
⚠️ No internal battlecard yet — verify via web.
**What it is:** Enterprise search + Work AI; horizontal **Glean Agents** for knowledge
workers. Employee-facing, overlaps on enterprise agent platform.
- **Likely angles:** 📡 not purpose-built for customer-facing CX/voice/contact-center; 🛡️
  determinism for transactional/regulated CX flows; 🔎 CX analyst validation.
- **Kore.ai counter:** purpose-built CX/CCAI, voice-native, deterministic transactional
  flows, vertical apps.
- **Triggers:** Glean Agents capabilities, funding/valuation, any move toward
  customer-facing/CX use cases.

## Moveworks · Horizontal enterprise
⚠️ No internal battlecard yet — verify via web.
**What it is:** Enterprise copilot / AI agents for IT & employee support (ITSM/HR).
**Being acquired by ServiceNow.** Cross-reference ServiceNow entry.
- **Likely angles:** 📡 internal-employee focus, not customer-facing CX/voice; ✳️
  acquisition-integration uncertainty; 🛡️ determinism for external CX.
- **Kore.ai counter:** customer-facing CX depth, voice-native, governed deterministic flows.
- **Triggers:** ServiceNow integration progress, post-acquisition product direction,
  expansion of agent use cases.

## Agentforce (Salesforce) · Big-tech platform
⚠️ No internal battlecard yet — verify via web.
**What it is:** Salesforce's agentic platform on Data Cloud/Einstein; agentic-CRM
positioning; evolving releases + consumption/credit pricing.
- **Likely angles:** 💲 per-conversation / credit pricing unpredictability at scale; 🔒
  data-cloud + ecosystem lock-in; 🛡️ determinism/governance of LLM agents for compliance;
  📡 standalone CX/voice depth outside the Salesforce estate.
- **Kore.ai counter:** provider-agnostic & CRM-agnostic, ABL determinism, predictable
  deterministic-flow economics, voice-native omnichannel.
- **Triggers:** new Agentforce versions, pricing changes, adoption numbers, service/CX agent
  capabilities, partner moves.

## ServiceNow Agent Platform · Big-tech platform
⚠️ No internal battlecard yet — verify via web.
**What it is:** Agentic AI on the Now Platform — AI Agents, Now Assist, AI Agent
Orchestrator. **Acquired Moveworks.**
- **Likely angles:** 📡 workflow/IT-ops heritage vs. customer-facing CX/voice; 🔒
  Now-Platform lock-in; 💲 platform + per-agent cost; ✳️ Moveworks integration risk.
- **Kore.ai counter:** CX/CCAI-native, voice-native, provider-agnostic, deterministic
  customer-facing flows.
- **Triggers:** AI Agent Orchestrator releases, Moveworks integration, CX/service agent
  moves, adoption, pricing.

## IBM Agent Platform · Big-tech platform
⚠️ No internal battlecard yet — verify via web.
**What it is:** IBM agentic AI, primarily **watsonx Orchestrate** (Agent Builder, Agent
Catalog) for enterprise automation.
- **Likely angles:** 📡 automation/back-office focus vs. dedicated CX/contact-center; 💲
  services-heavy TCO; 🔎 CX-specific analyst validation; time-to-value/build speed.
- **Kore.ai counter:** purpose-built CX platform, idea-to-live in days, voice-native,
  vertical apps, 6x analyst Leader status.
- **Triggers:** watsonx Orchestrate releases, agentic capabilities, partnerships,
  customer-service deployments.
