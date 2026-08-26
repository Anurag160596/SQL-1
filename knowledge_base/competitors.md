# Competitor Battlecards

16 tracked competitors, each as a **living battlecard** built to undercut. Structure:
**What it is → Recent (sourced) → Pricing → Analyst standing → Customers →
Exploitable weaknesses (by lever) → Sales trap questions → Triggers to watch.**

- **Battlecard framing** = Kore.ai's internal positioning (one-sided), strongest for the
  three we have decks on (Cresta, PolyAI, Parloa).
- The other 10 were hardened via web research (June 2026); key claims carry a source.
  Re-verify figures before external use — some pricing/TCO numbers are third-party
  estimates (vendors rarely publish list pricing), flagged inline.

Undercut levers (shorthand): 💲 Pricing/TCO · 🔎 Proof/validation · 📡 Channel/coverage ·
🛡️ Reliability/governance · ✳️ Other (M&A/integration/lock-in/instability).

**The master wedge (applies to almost everyone):** In the *conversational/agentic-AI-for-CX*
category, the analyst Leaders are pure-play platforms — **Kore.ai, NiCE Cognigy, Omilia**
(Forrester Wave Q2 2026) and **Google + Kore.ai** (Gartner MQ Conversational AI 2025).
CCaaS incumbents lead *CCaaS* MQs; big-tech leads *CRM/ITSM* MQs; the startups have *no*
CX analyst validation at all. Only **NiCE Cognigy** is a true peer-Leader.

Grouping: **CX-native agents** (Sierra, Decagon, Cresta, PolyAI, Parloa) ·
**CCaaS incumbents** (Genesys, NICE/Cognigy, Five9) ·
**Horizontal enterprise** (Glean, Moveworks) ·
**Big-tech platforms** (Agentforce, ServiceNow, IBM) ·
**Voice & dev-framework challengers** (Rasa, ElevenLabs, Ringg AI).

---

## Cresta · CX-native agents
**What it is:** Contact-center AI built on a conversation-data moat (millions of real
transcripts). Insights, AI Analyst, Quality Management, Automation Discovery, agent-assist,
AI agents. Launched **Conductor** (Jun 11, 2026), a dev-native agent-build environment +
AI Agent Testing 2.0. Forrester-cited explainability. Customers: United, Alaska, Cox.

**Exploitable weaknesses**
- 🛡️ Prompt-plus-custom-code build surfaces broken handoffs, invalid tool refs, unreachable
  steps only at test/production, not build time. Cresta concedes the prompt-vs-code split is
  a manual call ("an IVR that calls an LLM" if over-coded).
- 💲 Flagged on pricing complexity / cost attribution.
- 🔎 Strong in conversation intelligence; less proven on full-lifecycle enterprise platform
  breadth (release engineering, cross-agent trace, model-agnostic tiering).

**Kore.ai counter:** ABL compiles — compile-time validation + zero-LLM deterministic mode.
Cross-agent trace trees, 100% conversation evaluation, Git-native releases, per-agent cost
attribution. Concede the data moat, reframe it as a design input, not a substitute for
production reliability.

**Trap Qs:** "When a prompt-built agent breaks a compliance step, do you find out at build
time or in production?" · "How is cost attributed per agent/intent/tool?"
**Triggers:** Conductor customer proof, pricing changes, analyst placements, expansion beyond
conversation intelligence.

## PolyAI · CX-native agents
**What it is:** Voice-first / voice-only customer-service automation, centered on inbound voice.
**Exploitable weaknesses**
- 📡 Narrow — lacks unified omnichannel across chat/messaging/digital.
- 💲 Consumption pricing with fewer cost-optimization options; Gartner notes long-term TCO
  can be "less predictable."
- ✳️ Build leans on PolyAI's own teams/roadmap → slower, vendor-dependent iteration.

**Kore.ai counter:** One stack across voice **and** digital; voice-native (SSML, barge-in,
sub-500ms) plus cross-channel session resume; no-code self-service build.
**Trap Qs:** "What happens when a voice conversation needs to continue on chat?" · "Can your
business users build/change agents without the vendor?"
**Triggers:** moves into digital/omnichannel, pricing changes, enterprise logos, funding.

## Parloa · CX-native agents
**What it is:** Voice-first contact-center AI; Gartner calls it an "AI Agent Management
Platform" with agent-assist (the **Arch** design layer).
**Exploitable weaknesses**
- 🔎 **Not evaluated** by Gartner MQ, either Forrester Wave, either Everest PEAK, or IDC
  MarketScape; ~1 verified G2 review.
- 📡 Limited geographic reach (customer base largely Europe — Gartner excluded it on
  geography); narrower scope than a full enterprise platform.

**Kore.ai counter:** Leader across six analyst evaluations; 80+ connectors, 250+ CRM/ERP
integrations, prebuilt vertical apps; global enterprise deployments.
**Trap Qs:** "Which independent analysts have evaluated their platform?" · "How many verified
enterprise references outside their home region?"
**Triggers:** US/enterprise expansion, first analyst evaluations, funding, big logos.

## Sierra · CX-native agents | $15.8B valuation, ~$150M ARR
**What it is:** Conversational AI agent platform for CX, co-founded by **Bret Taylor** (OpenAI
chair) & Clay Bavor. Expanding beyond support into mortgage, insurance claims, healthcare RCM.
**Recent:** Raised **$950M at a $15.8B post-money valuation, May 2026** (Tiger Global + GV)
([TechCrunch](https://techcrunch.com/2026/05/04/sierra-raises-950m-as-the-race-to-own-enterprise-ai-gets-serious/)).
**~$150M ARR** by Feb 2026, crossed $100M ARR ~7 quarters after its Feb 2024 launch; claims
40%+ of the Fortune 50 ([CNBC](https://www.cnbc.com/2026/05/04/bret-taylor-sierra-fundraise-openai.html)).
**Pricing:** outcome-based (per successful resolution) — premium-priced; exact terms not public.
**Analyst standing:** strong brand and funding, but **no Leader placement in Gartner MQ
Conversational AI 2025 or Forrester CAI for Customer Service Q2 2026** (those Leaders are
Kore.ai, NiCE Cognigy, Omilia, Google).
**Customers:** named logos limited publicly; claims Fortune 50 breadth.
**Exploitable weaknesses**
- 🔎 Brand/hype and funding outrun **independent CX analyst validation** — not a Leader in the
  CX-specific Waves/MQs where Kore.ai is.
- 🛡️ Autonomous LLM agents → determinism/auditability questions for regulated industries.
- 💲 Outcome/per-resolution pricing can be unpredictable; "what counts as a resolution?" ambiguity.
- 📡 Verify true voice + omnichannel + back-end integration depth vs. a full enterprise platform.
**Trap Qs:** "Which independent analyst evaluations name Sierra a Leader for customer service?" ·
"For a regulated flow, how is the agent's decisioning made deterministic and auditable?"
**Triggers:** new funding/valuation, voice push, enterprise logos, first analyst recognition.

## Decagon · CX-native agents | $4.5B valuation, ~$35M ARR
**What it is:** AI customer-service agents ("AI concierge") for enterprise support; founder
Jesse Zhang.
**Recent:** **$4.5B valuation, Jan 2026** ($250M Series D, Coatue + Index)
([Bloomberg](https://www.bloomberg.com/news/articles/2026-01-28/ai-customer-support-startup-decagon-valued-at-4-5-billion));
tripled from **$1.5B** (Series C $131M, Jun 2025). **~$35M revenue in 2025** — a steep
revenue-to-valuation gap. Added 100+ enterprise customers in 2025
([BusinessWire](https://www.businesswire.com/news/home/20260128580542/en/Decagons-Valuation-Triples-to-$4.5-Billion-as-it-Ushers-in-the-Age-of-AI-Concierge)).
**Pricing:** custom; reported per-resolution/outcome leaning. (unverified specifics)
**Analyst standing:** **no CX analyst Leader validation** (not in Gartner/Forrester CX Leaders).
**Customers:** Avis Budget Group, Mercado Libre, Deutsche Telekom; plus Notion, Duolingo,
Rippling, Bilt, Eventbrite, Substack, Oura, Affirm, Chime.
**Exploitable weaknesses**
- 🔎 **~$35M revenue at a $4.5B valuation** — proof-of-durability and analyst-validation gap.
- 📡 Predominantly digital/chat support heritage; verify voice + true omnichannel depth.
- 🛡️ Governance/compliance depth for regulated verticals (banking, healthcare) unproven vs. ABL.
- 💲 Pricing-model maturity for high-volume enterprise economics.
**Trap Qs:** "What's their production containment rate in a regulated vertical, and how is it
audited?" · "Which analyst names them a Leader for enterprise customer service?"
**Triggers:** funding/valuation, voice/omnichannel expansion, platform launches, churn signals.

## Genesys · CCaaS incumbent | Gartner CCaaS Leader (11th yr), ~$2.6B Cloud ARR
**What it is:** Cloud CCaaS / "experience orchestration" platform (Genesys Cloud CX), adding
agentic AI. Privately held (Hellman & Friedman, Permira); pre-IPO.
**Recent:** Cloud ARR **~$2.6B, +35% YoY** (FY2026); **AI ARR >$250M**
([CX Today](https://www.cxtoday.com/contact-center/genesys-q4-2026-results/)).
**$1.5B strategic investment from Salesforce + ServiceNow (Jul 2025, ~$15B val)** — used to
**buy out existing holders**, not fund growth; reportedly cooled IPO urgency
([Genesys](https://www.genesys.com/company/newsroom/announcements/genesys-announces-1-5-billion-investment-by-salesforce-and-servicenow)).
Confidential S-1 since Oct 2024, no public IPO. Layoffs Nov 2025 (<1%). More-autonomous AI
Agents only hit GA ~Q4 FY26.
**Pricing:** per-agent tiers **CX1 ~$75 → CX4 ~$240/agent/mo**, plus **metered "AI tokens"**
(overage risk) and separate per-minute telephony; third parties estimate services add 50–100%
to Year-1 ([CheckThat.ai](https://checkthat.ai/brands/genesys/pricing) — third-party, indicative).
**Reliability:** multi-month **UAE-region outage from ~Mar 2026** (underlying cloud provider),
no ETTR as of mid-May 2026 ([Genesys status](https://status.mypurecloud.com/history)).
**Analyst standing:** Gartner CCaaS MQ Leader (11th yr); Forrester Wave CCaaS Q2 2025 Leader.
(Note: these are *CCaaS* evaluations, not the conversational-AI-for-CX category.)
**Customers:** Coca-Cola, eBay, Heineken, Lenovo, PayPal, Bosch.
**Exploitable weaknesses**
- 💲 AI bolted onto a seat model via per-agent tiers + **AI-token** consumption → overage
  unpredictability as automation scales; telecom + services inflate true TCO.
- 🛡️ Reliability exposure to third-party cloud infra (multi-month UAE outage, no ETTR).
- 🔎 Agentic autonomy only reached GA ~Q4 FY26 — thin production track record on determinism.
- ✳️ Roadmap tied to **Salesforce + ServiceNow** (who fund it *and* build competing agents) →
  lock-in/coopetition; private-company opacity (no public financials).
**Trap Qs:** "As AI deflection grows, is your cost per-seat + AI-token or per-outcome — what was
last quarter's token overage vs. your allowance?" · "During the multi-month regional outage,
what was your SLA recourse, and how much resilience is Genesys's vs. an infra/partner dependency?"
**Triggers:** AI agent moves, IPO/S-1 progress, earnings, more outages, Salesforce/ServiceNow
dynamics.

## NICE (Cognigy) · CCaaS incumbent | ⭐ peer-Leader — take most seriously
**What it is:** Market-leading CCaaS (CXone Mpower, Enlighten AI). **Acquired Cognigy** —
now "NiCE Cognigy," the native conversational/agentic layer.
**Recent:** Cognigy acquired for **~$955M (~25x revenue)**, announced Jul 28 2025, **closed
Sep 8 2025** — NICE's biggest deal ever; founder Philipp Heltewig → GM & Chief AI Officer
([NICE](https://www.nice.com/press-releases/nice-to-acquire-cognigy-advancing-the-leading-cx-ai-platform-to-accelerate-ai-first-customer-experience);
[Aragon — 25x premium](https://aragonresearch.com/nice-acquires-cognigy-at-a-25x-premium/)).
Q1 FY2026 revenue **$769M (+10%)**, cloud 79%, **AI ARR +66% YoY**. New CEO **Scott Russell**
(ex-SAP) since Jan 2025. NiCE World 2026: AgentForge, **Guardian Agent** (governance),
Agentic Engagement Plane.
**Pricing:** per-agent tiers ~$110–$249/agent/mo, top **Ultimate ~$249 + ~$0.25/session**; best
AI gated to the top tier ([CloudTalk](https://www.cloudtalk.io/blog/nice-cxone-pricing/) — third-party).
**Analyst standing:** Gartner CCaaS MQ Leader (11th yr, top-right on both axes); **Leader,
Forrester Wave: Conversational AI for Customer Service Q2 2026 — alongside Kore.ai and Omilia**
([CX Foundation](https://cxfoundation.com/blog/forrester-wave-conversational-ai-2026)).
**Customers:** Cognigy — Bosch, Nestlé, Lufthansa Group, Mercedes-Benz, Toyota (1,250+
enterprises); CXone — Teleperformance, Carnival UK, IAG.
**Exploitable weaknesses**
- ✳️ **Cognigy is a bolt-on** (~25x-revenue acquisition), stitched into CXone/Enlighten —
  **two AI lineages** (Enlighten Autopilot/Copilot vs. Cognigy) with overlap/roadmap ambiguity.
- 💲 Best AI gated to ~$249/agent Ultimate + per-session fees → high fully-loaded TCO.
- 🛡️ Governance ("Guardian Agent") only shipped 2026 — new, not battle-tested across the merged stack.
- 📡 User-reported CRM-integration friction, complex SSO/SCIM, Studio UI lag.
- ✳️ New CEO executing the most expensive deal in company history → execution/continuity pressure.
**Trap Qs:** "Is your CXone AI agent running on Cognigy or Enlighten — and which is the committed
3-year roadmap?" · "Show fully-loaded cost at our volume (Ultimate seats + per-session AI), and
how guardrails enforce deterministic, auditable behavior across both AI layers."
**Triggers:** Cognigy↔CXone integration milestones, joint launches, earnings, analyst placements.

## Five9 · CCaaS incumbent | seat-model under AI pressure
**What it is:** Public (NASDAQ: FIVN) CCaaS; "Intelligent CX Platform" + **Genius AI**, pivoting
to "Agentic CX." Core revenue still seat-based.
**Recent:** Q1 2026 revenue **+9% to $305.3M**; **AI revenue +68% YoY (~$125M run rate, 13% of
subscription)** ([No Jitter](https://www.nojitter.com/contact-centers/five9-reported-strong-q1-2026-earnings-ai-growth)).
**New CEO Amit Mathradas (eff Feb 2, 2026)**; Burkland retired to Chairman. **Three layoff rounds
in ~12 months** + senior-exec purge (CMO, EVP Strategy, HR head)
([CX Today](https://www.cxtoday.com/contact-center/five9-confirms-its-second-round-of-layoffs-in-a-year-affecting-4-of-its-workforce/)).
**Piper Sandler Jan 2026 downgrade**: AI "continue[s] to impact primarily seat-based models like
Five9's"; stock near 52-week low (~$16, ~90% off peak)
([InflectionCX](https://www.inflectioncx.com/intelligence/analysis/state-of-five9-2026-ai-pivots-stock-collapse-cx-leaders)).
Activist (Anson) board seat; sale speculation. Acquired Acqueon (Aug 2024).
**Pricing:** per-seat, **50-seat minimum**, multi-year; ~$119–$229+/user/mo + AI consumption overages
([Platform28](https://www.platform28.com/blog/five9-pricing-breakdown) — third-party).
**Analyst standing:** Gartner CCaaS MQ Leader (8th); **Forrester Wave CCaaS 2025 = Strong Performer
(NOT a Leader)**; Forrester flagged Five9's WFM "lacks scalability for enterprise-level customers"
([CX Today](https://www.cxtoday.com/contact-center/the-forrester-wave-for-ccaas-platforms-2025-top-takeaways/)).
**Customers:** Alaska Airlines, Wyndham, PUMA, ALDO, Kyndryl.
**Exploitable weaknesses**
- 💲 **Seat-based model structurally exposed to AI deflection** (analyst-flagged); 50-seat min +
  multi-year lock-in + AI overages → opaque, front-loaded cost.
- 🔎 **Strong Performer, not Leader** (Forrester CCaaS 2025) + explicit enterprise WFM scalability gap.
- ✳️ Organizational instability — three layoff rounds, exec purge, new CEO, activist pressure,
  sale speculation → roadmap-continuity risk for a multi-year bet.
- 🛡️ AI is a bolt-on over a legacy seat platform (IVA→GenAI Studio→"AI Agents"→"Agentic CX");
  governance is a 2025 add-on.
**Trap Qs:** "As containment rises, what happens to your committed seat spend — can you model
cost-per-resolution two years out?" · "Forrester rated Five9 a Strong Performer with enterprise
WFM scalability gaps — what containment are you getting in production today?"
**Triggers:** earnings, layoffs/exec moves, acquisition news, analyst placements, pricing changes.

## Glean · Horizontal enterprise | employee-facing, not CX
**What it is:** Enterprise search + **Work AI**; horizontal **Glean Agents** for knowledge workers.
**Employee-facing — not a customer-facing contact-center product.**
**Recent:** **Series F $150M at $7.2B (Jun 2025)**, up from $4.6B (Sep 2024)
([CNBC](https://www.cnbc.com/2025/06/10/glean-gen-ai-search-startup-raises-150-million-at-7-billion-value.html)).
ARR ~$100M (Jan 2025) → $200M (Dec 2025) → **~$300M (May 2026)**, positioning as an AI
budget-consolidation play
([TechCrunch](https://techcrunch.com/2026/05/28/gleans-top-line-crosses-300m-as-ai-budget-cutting-becomes-its-major-selling-point/)).
Glean Agents launched Feb 2025, GA May 2025.
**Pricing:** no public list; ~per-seat + Work AI add-on + "FlexCredits" + ~10% support fee
(third-party estimates — unverified).
**Analyst standing:** Gartner **Emerging Leader** (GenAI Knowledge Management — employee
productivity); Forrester Wave **Cognitive Search** Q4 2025 (flagged **narrower connector
ecosystem**). **No CX/contact-center analyst validation.**
**Customers:** Reddit, Databricks, Duolingo, Booking.com, Deutsche Telekom, Grammarly.
**Exploitable weaknesses**
- 📡 **Employee-facing, not customer-facing; no voice/contact-center.** Glean's own "support"
  offering helps *internal* agents find answers, not customer self-service.
- 🔎 Recognition is in KM/cognitive-search categories — **absent from CX conversational-AI Leaders.**
- 🛡️ Narrower connector ecosystem (Forrester) → weaker for high-volume, transactional, integrated CX.
- 💲 Opaque seat pricing + add-ons + support fees → TCO unpredictability for per-interaction CX economics.
**Trap Qs:** "Does Glean handle customer-facing voice and omnichannel, or internal employee search?" ·
"Which CX analyst evaluation names Glean for customer service?"
**Triggers:** any move toward customer-facing/CX, funding, enterprise adoption.

## Moveworks · Horizontal enterprise | now a ServiceNow business unit
**What it is:** Employee-facing AI assistant/agents for **IT, HR, finance** (Slack/Teams/ITSM).
Acquired by ServiceNow; being folded into **ServiceNow Otto**. **Not customer-facing CX.**
**Recent:** ServiceNow acquired for **$2.85B** (announced Mar 10 2025, **DOJ second-request review**,
**closed Dec 15 2025**) — ServiceNow's largest deal
([ServiceNow](https://newsroom.servicenow.com/press-releases/details/2025/ServiceNow-to-extend-leading-agentic-AI-to-every-employee-for-every-corner-of-the-business-with-acquisition-of-Moveworks-03-10-2025-traffic/default.aspx);
[TechCrunch — DOJ](https://techcrunch.com/2025/07/18/servicenows-acquisition-of-moveworks-is-reportedly-being-reviewed-over-antitrust-concerns/)).
~$100M ARR (Sep 2024), 5M+ users, 350+ enterprises. Founder Bhavin Shah → SVP/GM at ServiceNow.
**Pricing:** headcount-based (~$15–$45+/employee/yr; ACVs to $1M+) — third-party (unverified).
**Analyst standing:** Gartner MQ **AI Apps in ITSM 2025 = Challenger**; dated Forrester 2020
IT-Ops report. **No CX/CCaaS/conversational-AI-for-CX validation.**
**Customers:** Siemens, Toyota, Unilever, Broadcom, CVS Health.
**Exploitable weaknesses**
- 📡 **Internal IT/HR support, not external CX; no voice / no contact-center channel.**
- 🔎 IT/ITSM analyst recognition only — absent from CX evaluations.
- ✳️ **Acquisition-integration risk** — roadmap now subordinate to ServiceNow/Otto; the prolonged
  DOJ review already pushed buyers to evaluate alternatives.
- 💲 Headcount-based pricing misaligned with CX per-resolution/per-conversation economics.
**Trap Qs:** "Does it deflect customer voice/omnichannel, or internal employee tickets?" · "Post-
ServiceNow, what's the standalone Moveworks roadmap vs. absorption into Otto?"
**Triggers:** Otto integration milestones, CX/voice moves, roadmap clarity.

## Agentforce (Salesforce) · Big-tech platform | >$1B ARR, but not a CAI Leader
**What it is:** Salesforce's agentic platform on Data Cloud/Data 360 + Atlas Reasoning Engine +
Einstein Trust Layer. Pushing into CX via **Agentforce Voice / Contact Center** (early 2026).
**Recent:** 2.0 (Dec 2024) → **3 (Jun 2025: MCP, observability, web-search grounding)** → **360
(Oct 2025)**. Q1 FY27 (May 2026): **Agentforce ARR $1.2B (+205% YoY)**; ~29,000 deals closed in
Q4 FY26 ([Salesforce IR](https://investor.salesforce.com/news/news-details/2026/Salesforce-Delivers-Record-First-Quarter-Fiscal-2027-Results/default.aspx)).
**Pricing chaos — reworked 3+ times in ~18 months:** $2/conversation → **Flex Credits** ($0.10/credit;
standard action ~20 credits ≈ $2, voice ~30) → per-user SKUs ~$125/user; **one model per org**
([Concret.io](https://www.concret.io/blog/new-agentforce-pricing-model);
[SaaStr](https://www.saastr.com/salesforce-now-has-3-pricing-models-for-agentforce-and-maybe-right-now-thats-the-way-to-do-it/)).
**Analyst standing:** Gartner MQ **CRM Customer Engagement Center 2025 Leader** — but **NOT a Leader**
in Gartner Conversational AI 2025 or **Forrester CAI for Customer Service Q2 2026** (Kore.ai, NiCE
Cognigy, Omilia lead) ([CX Foundation](https://cxfoundation.com/blog/forrester-wave-conversational-ai-2026)).
**Customers:** 1-800Accountant (~70% chat deflection), Reddit (~46% deflection), Wiley (213% ROI).
**Exploitable weaknesses**
- 💲 **Pricing unpredictability / credit anxiety** — "what counts as a conversation?"; CIOs wary of
  consumption overruns; of ~5,000 early deals only ~3,000 were paid (SaaStr).
- ✳️ **Data Cloud / platform lock-in** — Data Cloud is effectively a prerequisite; harder to
  decouple governance from Salesforce.
- 🛡️ Hallucination/governance — reported **3–27% hallucination** depending on grounding; heavy
  guardrail/data-quality burden on the buyer.
- 📡 CX/voice depth requires **third-party telephony** (Amazon Connect / 20+ CCaaS partners);
  missing WFM/QM; **not a conversational-AI Leader.**
**Trap Qs:** "Which pricing model are you on, and can you forecast cost as autonomous agents drive
continuous high-volume interactions?" · "For voice, whose telephony/WFM/QM are you relying on —
and which analyst names Agentforce a Leader for *customer service conversational AI*?"
**Triggers:** new versions, pricing changes, adoption numbers, Voice/Contact Center traction.

## ServiceNow Agent Platform · Big-tech platform | ITSM-native, expanding to CX
**What it is:** Agentic AI native to the Now Platform — Now Assist, AI Agents + AI Agent Studio,
**AI Agent Orchestrator**, AI Control Tower + Agent Fabric (MCP/A2A), now unified as **Otto**
(Knowledge 2026, folding in Moveworks).
**Recent:** AI Agents/Orchestrator/Studio announced Jan 2025 (avail Mar 2025); **2026 repackaging
to Foundation/Advanced/Prime (eff Apr 9 2026; custom agents only on Prime; old SKUs EOS Jul 1 2026)**
([TechTarget](https://www.techtarget.com/searchitoperations/news/366641692/ServiceNow-AI-pricing-change-takes-on-enterprise-ROI-struggles)).
Now Assist ACV **doubled YoY, on path to >$1B FY26**
([ServiceNow IR](https://investor.servicenow.com/news/news-details/2026/ServiceNow-Reports-First-Quarter-2026-Financial-Results/default.aspx)).
Acquired Moveworks ($2.85B, closed Dec 2025).
**Pricing:** **"assists" consumption** (small task ~25 assists, agentic action ~150); committed pool +
overage; list pricing is effectively quote-only.
**Analyst standing:** Gartner MQ **AI Apps in ITSM 2025 = sole Leader**; Forrester Wave **Customer
Service Solutions Leader** — but cautions cited as **complexity and cost**
([ServiceNow](https://www.servicenow.com/blogs/2026/leader-forrester-wave-customer-service-solutions)).
**Customers:** Adobe (8,000+ IT/HR staff on Now Assist), Southeastern.
**Exploitable weaknesses**
- 💲 **Assists consumption TCO unpredictability** — "AI Control Tower offers hazy view of spend"
  (CIO); an agent **retry loop** "gobbles assist credits with each iteration."
- ✳️ **ITSM-centric lock-in** — rip-and-replace adoption; **custom AI agents only on the top Prime tier.**
- 🛡️ Forrester flags a gap between ServiceNow's agentic-AI vision and IT operational maturity.
- 📡 **No native voice/PSTN** — Contact Center relies on third-party CCaaS (3CLogic, Cisco, Webex);
  ITSM heritage, not purpose-built external CX.
**Trap Qs:** "How do you forecast 'assists' when agentic actions cost 6× a simple task and retry loops
burn credits?" · "For customer voice, whose telephony are you integrating — and is your CX agent
ITSM-workflow-bound or a standalone omnichannel platform?"
**Triggers:** Otto/Moveworks integration, pricing-tier changes, CX/voice moves, earnings.

## IBM watsonx Orchestrate · Big-tech platform | slipped to Gartner Challenger
**What it is:** IBM's enterprise agentic platform — **Agent Builder** + **Agent Catalog** (150+ agents)
+ ADK; repositioned at Think 2026 as a multi-vendor **"agentic control plane."** Back/mid-office
strength (HR, procurement, finance, sales).
**Recent:** Think 2025 launch; **Think 2026 next-gen Orchestrate (control plane: Granite/Claude/GPT/
Mistral)**; **IBM–Anthropic partnership (Oct 2025)**; contact-center **agent assist GA mid-2026**
(Genesys integration + **ElevenLabs** voice)
([IBM](https://www.ibm.com/new/announcements/introducing-agent-assist-in-watsonx-orchestrate-to-transform-contact-center-performance)).
**Pricing:** consumption — **Resource Units (1 RU = 1,000 tokens)** + MAUs; Essentials ~$500/mo,
Standard ~$6,360/mo (third-party — IBM doesn't publish clean list pricing).
**Analyst standing:** Gartner MQ **Conversational AI Platforms 2025 = Challenger (slipped from
Leader)**; Gartner flagged **"confusing overlaps between watsonx Orchestrate and watsonx Assistant"**
([CX Today](https://www.cxtoday.com/customer-analytics-intelligence/gartner-magic-quadrant-for-conversational-ai-platforms-2025-the-rundown/)).
Leader in 7 *adjacent* AI MQs (Data Science, App Dev, etc.).
**Customers:** internal AskIBM (300k+ monthly interactions), Riyadh Air, MyLÚA Health, Georgia Tech, UFC.
**Exploitable weaknesses**
- 💲 **RU/token consumption unpredictability** at scale; G2 reviewers flag "expensive," better for
  large enterprises than smaller/short projects.
- ✳️ Complexity / **IBM-ecosystem + consulting gravity** — steep learning curve, SI dependency,
  "operational retraining burden" to manage agent drift.
- 🔎 **Slipped to Gartner Challenger** in Conversational AI; **Orchestrate vs. Assistant overlap**
  confuses buyers seeking a clear CX stack.
- 📡 Back-office orientation; **voice/contact-center is newer/bolt-on** (2026 GA via Genesys/ElevenLabs).
**Trap Qs:** "Are you on watsonx Orchestrate or watsonx Assistant for customer-facing conversational AI —
and why did Gartner move IBM to Challenger?" · "How do you forecast RU/token spend for high-volume CX?"
**Triggers:** Think announcements, Orchestrate/Assistant consolidation, voice/contact-center traction,
analyst movement.

---

# Group 5 · Voice & dev-framework challengers

Added Aug 2026. These three are **not** enterprise CX platforms — they are a developer
framework (Rasa), voice infrastructure (ElevenLabs) and an early-stage voice-agent
startup (Ringg AI). They surface in deals as "cheaper / faster / we'll build it
ourselves" alternatives, so the wedge is **platform completeness, governance and
independent validation**, not feature-for-feature voice quality.

**Source discipline for this group:** claims below are tagged by evidence type —
`G2` / `PEER REVIEWS` (Gartner Peer Insights, TrustRadius, SoftwareAdvice) /
`PUBLIC NEWS` / `VENDOR` (the vendor's own site or pricing page). Where the only
available source is a rival vendor's comparison blog, the claim is **excluded** or
flagged as unverified — several "Ringg is voice-only" claims circulating in
alternative-vendor blogs are contradicted by Ringg's own site and are not used here.
Reddit was not directly retrievable at build time; nothing here is sourced to Reddit.

## Rasa · Voice & dev-framework | open-core developer framework, CALM
**What it is:** Pro-code conversational-AI framework. Post-2024 it splits into the free
**Rasa Developer Edition** (ships CALM), **Rasa Pro** (the licensed pro-code framework +
infrastructure) and **Rasa Studio** (no-code UI on top). Self-hosted by design — the
customer owns hosting, scaling, monitoring and upgrades.
**Pricing:** Developer Edition free but capped at **1,000 conversations/month** (100/mo for
internal employee-facing agents); **Growth ≈ $35,000/year** for ~500k conversations with
support; Enterprise quote-only — plus the customer's own infra and ops cost
([Voiceflow](https://www.voiceflow.com/blog/rasa-chatbot), [Rasa docs](https://rasa.com/docs/pro/intro/)).
**Analyst standing:** **not evaluated** in the Gartner MQ for Conversational AI Platforms
2025 (Leaders: Google, Kore.ai; Rasa appears in no quadrant) or the Forrester Wave for
Conversational AI Platforms for Customer Service
([CX Today rundown](https://www.cxtoday.com/customer-analytics-intelligence/gartner-magic-quadrant-for-conversational-ai-platforms-2025-the-rundown/)).

**Exploitable weaknesses**
- ✳️ **Engineer-only build surface.** G2 reviewers: "not a plug-and-play tool… requires much
  technical expertise in NLP concepts, Python and deployment workflows"; "designed for machine
  learning experts." Business users cannot ship a change without a developer
  ([G2](https://www.g2.com/products/rasa/reviews?qs=pros-and-cons)).
- 💲 **Cost and licensing bite at scale.** The free tier is a demo-sized cap; real volume
  starts at five figures a year *plus* self-hosting cost. Gartner Peer Insights reviewers flag
  **"licensing and cost are complex"** and limited community resources
  ([Gartner Peer Insights](https://www.gartner.com/reviews/product/rasa-platform)).
- 🔎/📡 **No CX analyst validation and a hand-built voice path.** Absent from both the Gartner MQ
  and the Forrester Wave. Voice is assembled by the customer (STT → Rasa server → TTS, a
  **1–3 second** round trip, with barge-in as custom logic); reviewers also call analytics
  less comprehensive than competitors
  ([Voiceflow](https://www.voiceflow.com/blog/rasa-chatbot), [Dasha](https://dasha.ai/tips/rasa-alternatives)).

**Kore.ai counter:** One governed platform instead of a framework plus a build project —
voice-native gateway (SSML, barge-in, sub-500ms scripted turns) rather than a stitched STT/TTS
pipeline; ABL lets domain experts author compile-valid agents, so change velocity does not
depend on the engineering backlog; Leader in the Gartner MQ 2025 and Forrester Wave Q2 2026.
Concede Rasa's real strength — self-hosting and data control — then price the total build,
run and maintain cost against a managed enterprise platform.
**Trap Qs:** "Who ships a policy change on Friday — a business owner, or your ML engineers?" ·
"What is the fully-loaded cost once you add hosting, ops, upgrades and the people to own the
stack?" · "Which independent analyst has evaluated Rasa for customer service?"
**Triggers:** licensing/tier changes, CALM/Studio releases, first analyst evaluation, enterprise
logos, funding, any move to managed hosting.

## ElevenLabs · Voice & dev-framework | voice infrastructure moving into agents
**What it is:** Best-in-class TTS/voice-cloning company that extended into **ElevenLabs Agents**
(voice + chat agents for websites, apps and call centers). Genuinely strong voice quality and
low synthesis latency; integrations exist for Salesforce, HubSpot, Zendesk, ServiceNow, Twilio,
Vonage and Genesys, plus any API via MCP. Deloitte partnership (Nov 2025); powers IBM watsonx
Orchestrate's contact-center agent assist voice layer.
**Pricing:** credit-based. Business **$825/month for 11M credits (~13,750 minutes)**; additional
minutes **$0.08/min**, **burst $0.16/min (2×) once concurrency is exceeded**; credits roll over
only **two billing cycles** and are **forfeited on downgrade**. Enterprise is custom and adds
SSO, HIPAA/BAA, SOC 2, GDPR ([ElevenLabs](https://elevenlabs.io/pricing/agents),
[CloudTalk](https://www.cloudtalk.io/blog/elevenlabs-pricing/)).
**Analyst standing:** **no CX analyst validation** — absent from the Gartner MQ for Conversational
AI Platforms and the Forrester Wave for Customer Service. Its Gartner Peer Insights presence sits
in **voice/AI-dubbing and text-to-speech** categories, not conversational AI for customer service.
**Customers:** Freedom Forever (reported 90% cost reduction, 50% smaller human agent workforce).

**Exploitable weaknesses**
- 📡 **Voice infrastructure, not a CX platform.** Independent reviews describe it as a platform
  where "someone has to design the agent, wire the telephony, and connect the CRM," with
  **thin customer-service automation and limited production monitoring**, and engineering work
  needed to integrate with existing contact-center tooling. No native WFM, QM, agent-assist or
  case management ([CloudTalk](https://www.cloudtalk.io/blog/elevenlabs-voice-agent-review/),
  [Cekura](https://www.cekura.ai/blogs/elevenlabs-review)).
- 💲 **Credit-burn TCO unpredictability.** Long calls and the higher-cost multilingual models
  chew quota faster than teams model, and many hit overage in month two or three; burst pricing
  doubles the per-minute rate exactly when volume spikes. In the G2 corpus the word "expensive"
  appears **171 times** and pricing complaints a further **148 times**; Trustpilot sits at **3.2**
  on pricing opacity, credit burn on failed generations, and concurrency limits — against a
  **4.5/5 across ~1,140 G2 reviews** for the product overall
  ([G2](https://www.g2.com/products/elevenlabsio/reviews),
  [Metadata Marketer](https://metadatamarketer.com/elevenlabs-intelligence-report/)).
- 🛡️ **Governance depth for regulated CX is unproven.** Hallucination control is prompt-level
  guidance ("answer from the knowledge base, else say I don't know") plus simulations and
  pre-deployment tests — guardrails by instruction, not deterministic policy enforcement with an
  audit trail. Voice cloning also puts consent/impersonation risk on the buyer's compliance
  register ([ElevenLabs guidance](https://elevenlabs.io/agents)).

**Kore.ai counter:** Never argue voice quality — concede it, and reframe the deal as everything
that surrounds the voice: deterministic policy execution at runtime (ABL, zero-LLM mode for
compliance paths), compile-time validation, cross-agent trace, 100% conversation evaluation,
per-agent cost attribution, and 250+ CRM/ERP integrations out of the box. Position ElevenLabs
as a **voice layer Kore.ai can consume**, not a platform that replaces one.
**Trap Qs:** "Who builds, monitors and governs the agent once the voice sounds great — and what
does that team cost?" · "For a regulated flow, is the policy enforced at runtime or written into
a prompt, and what do you show an auditor?" · "What is your forecast cost when volume spikes past
your concurrency limit at 2× per minute?"
**Triggers:** CX platform build-out (WFM/QM/case management), pricing or credit-model changes,
first analyst evaluation, enterprise CX logos, CCaaS partnerships, voice-cloning/consent incidents.

## Ringg AI · Voice & dev-framework | early-stage, India-led voice agents
**What it is:** Bengaluru-based AI voice-agent platform (voice, chat, WhatsApp, web), strongest in
Hindi and Indian regional languages, with direct telephony integrations and fast setup. Vendor
claims sub-400ms latency, 120K+ interactions/hour and up to 10,000 concurrent calls.
**Recent:** **$5.5M Series A led by Arkam Ventures (Jan 2026)**; ~**$6.64M raised in total**.
Reports **20+ customers** across India, the US and Saudi Arabia and ~**1.5M voice conversations
per month**, ~75% resolved without a human. Funding is explicitly earmarked for reliability, lower
cost and **on-prem/data-residency deployments** — i.e. those are roadmap, not shipped history
([YourStory](https://yourstory.com/2026/01/voice-ai-startup-ringgai-seriesa-arkam-ventures),
[Entrepreneur India](https://india.entrepreneur.com/news-and-trends/voice-ai-startup-ringg-ai-secures-usd-55-mn-series-a/502061)).
**Pricing:** usage-based, roughly **$0.06–$0.10 per minute**; still sales-gated with no published
enterprise list pricing.
**Analyst standing:** **none** — not evaluated by Gartner, Forrester, Everest or IDC.
**Customers (vendor-listed):** CRED, PharmEasy, Flipkart, PolicyBazaar, Groww, DCB Bank, Practo,
Tabby, smallcase, Shiprocket.
**G2:** reported at 4.8/5 for regional-language coverage, cost and easy telephony setup.
**Treat the rating as unconfirmed** — a rival's comparison page puts the profile at roughly
**five reviews**, G2 blocks automated retrieval, and the G2 API account has no catalog access
for this product. Verify the live profile before quoting the rating or the count.

**Exploitable weaknesses**
- 🔎 **Early-stage proof.** ~$6.6M total funding and 20+ customers against enterprise platforms
  with hundreds of deployments; **zero independent analyst evaluation**; references concentrated
  in India.
- 🛡️ **Data residency and compliance are roadmap, not shipped.** *The decisive gap for regulated
  buyers.* Ringg's **own Series A announcement (Jan 2026)** states the capital is going into
  research and model development **to enable on-premise deployments for large enterprises that
  require higher levels of control, stricter compliance standards and data residency assurances**,
  and to **"eliminate dependence on third-party APIs"** — i.e. today there is no on-prem option,
  no stated regional data residency, and customer conversation data transits third-party model,
  STT and TTS APIs ([YourStory](https://yourstory.com/2026/01/voice-ai-startup-ringgai-seriesa-arkam-ventures),
  [Ringg AI](https://www.ringg.ai/blog/ringg-ai-announcing-our-5-5-millon-usd-series-a)).
  Compliance is **self-asserted marketing copy** — "SOC 2 compliance", encryption and data
  anonymization on the site, HIPAA on the healthcare page — with **no public trust centre, no
  SOC 2 Type II report, no ISO 27001, no PCI DSS, no HITRUST, no FedRAMP and no published DPDP or
  GDPR position** found as of Aug 2026. For a bank, insurer or hospital, that is an unclearable
  procurement gate, not a feature gap.
- 📡 **SMB-tier integration surface.** Published connectors are Google Sheets, Typeform, Shopify,
  Calendly, Notion and HubSpot plus a generic API request — no Salesforce/ServiceNow-class CRM
  depth, no CCaaS/WFM/QM, and post-call execution (CRM write-back, follow-up, retry logic) lands
  on the customer ([Ringg AI](https://www.ringg.ai/)).
- 🛡️ **Orchestration ceiling — UNVERIFIED, do not use externally.** Claims that the agent
  struggles with interruptions and multi-step requests, that complex branching is hard to
  configure, and that analytics are shallow, trace **only to rival vendors** selling a Ringg
  alternative ([omnidim.io](https://omnidim.io/blogs/alternatives-ringg),
  [tabbly.io](https://www.tabbly.io/blogs/ringg-ai-review-tabbly-alternative),
  [ringlyn.com](https://www.ringlyn.com/blog/ringlyn-ai-vs-ringg-ai-alternative/)). Each asserts
  "G2 reviewers say" without quoting a review. Same source class as the "voice-only" claim this
  card already rejects. **Verify against the live G2 profile before any use.**

**Kore.ai counter:** Concede price-per-minute and Indic-language coverage — then move the
conversation to what an enterprise actually buys. On residency and governance the contrast is
binary, so lead with it in any regulated deal: Kore.ai deploys in **public cloud, sovereign
regions, private cloud or on-premises with data residency by region**, holds **SOC 2 Type II,
ISO 27001, PCI DSS, HITRUST, FedRAMP Moderate and GDPR**, signs **BAAs**, publishes a
[public trust centre](https://trust.kore.ai/), and supports **bring-your-own-LLM** so inference
runs on an internal model instead of a third-party API — with PII tokenization, tenant isolation
and immutable audit trails on every agent action. Then add multi-step orchestration that survives
interruption, 250+ CRM/ERP integrations, cross-agent trace, 100% conversation evaluation, and
Leader placement in the Gartner MQ 2025 and Forrester Wave Q2 2026. Where the buyer is cost-led,
price the rework: a cheap per-minute agent that cannot keep data in-country or write back to the
system of record becomes a second project.
**Trap Qs:** "Where does our customer audio and PII physically live, and which third-party APIs
does it pass through before you answer?" · "Can we see the SOC 2 Type II report and the trust
centre, or is the claim only on the website?" · "When is on-premise generally available, with
named production references on it?" · "When the customer interrupts mid-flow or the request spans
three back-end systems, what happens?" · "Which independent analyst has evaluated the platform,
and how many enterprise references exist outside India?"
**Triggers:** on-prem/data-residency GA and its first production reference, **SOC 2 Type II /
ISO 27001 / DPDP attestation evidence or a published trust centre**, proprietary in-house model
replacing third-party APIs, new funding, first analyst evaluation, US/Middle East enterprise
logos, published enterprise pricing, CCaaS or CRM partnerships.
