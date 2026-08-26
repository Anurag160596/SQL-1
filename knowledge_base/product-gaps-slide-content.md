# Product Gaps — slide content (Kore.ai vs Rasa · ElevenLabs · Ringg AI)

**Two parts.** *Part 1* compares platform and commercial posture (validation, cost, residency,
operating layer). *Part 2* compares **agentic architecture** — orchestration primitives, shared
memory, governed tool use, and trace — measured against Kore.ai's Artemis generation. Part 2 is
the sharper axis for a technical or architecture audience, and every claim in it comes from a
vendor's own documentation.

Deck-ready copy for the **Strategic Positioning** layout: an eyebrow, an action title,
a strategic frame, then two columns — Kore.ai (green) and the competitor (grey), three
numbered points each, every point stamped with its evidence source.

**Source tags used:** `G2` · `PEER REVIEWS` (Gartner Peer Insights, TrustRadius,
SoftwareAdvice) · `PUBLIC NEWS` · `VENDOR` (competitor's own site/pricing page) ·
`TRUST CENTRE` (published certifications and attestation reports) ·
`GARTNER` / `FORRESTER` (analyst evaluations).

**Absence claims.** Where a slide says a certification or report was not found, that is
absence of published evidence as of August 2026, not proof it does not exist. Phrase it that
way in the room, and make it a question to the vendor rather than an accusation.

**On Reddit:** Reddit blocks automated retrieval, so no claim here is tagged `REDDIT`.
Every gap below is anchored to a source that was actually retrieved. If a Reddit tag is
required on the slide, pull the thread manually and swap the tag — do not infer it.

**Rule for the grey column:** rival-vendor comparison blogs (Tabbly, OmniDimension,
Ringlyn, Dasha, CloudTalk et al. writing about a competitor they sell against) are
treated as leads to verify, not as sources. Where such a blog was the only evidence,
the claim was dropped — e.g. the widely repeated "Ringg AI is voice-only" is
contradicted by Ringg's own site and is **not** used.

---

## Slide 1 · Kore.ai vs Rasa

**Eyebrow:** STRATEGIC POSITIONING ▪ KORE.AI VS RASA
**Action title:** Ship governed agents without building the platform first
**Strategic frame:** Enterprises need agents their business owners can change, their
auditors can inspect, and their finance teams can forecast — not a framework their
engineers must first assemble, host and maintain.

| | **Kore.ai** — ENTERPRISE-GRADE, AI-NATIVE PLATFORM | **Rasa** — DEVELOPER FRAMEWORK, SELF-HOSTED |
|---|---|---|
| **01** | **Domain experts build, not just developers.** ABL lets business owners author compile-valid agents; broken handoffs, invalid tool references and unreachable steps are caught at build time. `GARTNER` `FORRESTER` | **Every change needs an ML engineer.** G2 reviewers: "not a plug-and-play tool… requires much technical expertise in NLP concepts, Python and deployment workflows"; "designed for machine learning experts." `G2` `PEER REVIEWS` |
| **02** | **Managed platform, forecastable cost.** One stack across voice and digital with per-agent, per-intent and per-tool cost attribution — no hosting, scaling or upgrade burden carried by the customer. `EVEREST` `IDC` | **Five-figure floor plus your own infrastructure.** The free Developer Edition caps at 1,000 conversations/month (100 for internal agents); real volume and support start around $35,000/year, on top of self-hosted infra and ops. Peer reviewers flag "licensing and cost are complex." `VENDOR` `PEER REVIEWS` |
| **03** | **Leader, and voice-native out of the box.** Named a Leader in the Gartner MQ for Conversational AI Platforms 2026 and the Forrester Wave for customer service, the only vendor leading both. In-house voice gateway with SSML, barge-in and sub-500ms scripted turns. `GARTNER` `FORRESTER` | **Evaluated, never a Leader, and voice is a build project.** Gartner gave Rasa an honorable mention in the 2026 MQ with no quadrant position, and Forrester included it in the 2026 Wave without naming it a Leader. Rasa does ship voice connectors for Twilio, Jambonz, AudioCodes and Genesys, so concede voice. `GARTNER` `FORRESTER` |

**Trap questions:** "Who ships a policy change on Friday — a business owner or your ML
engineers?" · "What is the fully-loaded cost once you add hosting, ops, upgrades and the
people to own the stack?" · "Gartner and Forrester have both looked at Rasa. Which one names
it a Leader?"

> ⚠️ **Corrected Aug 2026.** An earlier draft said Rasa has "no CX analyst validation." That is
> wrong for 2026 and a prepared buyer will catch it. Rasa *is* evaluated. It is simply never a
> Leader and holds no quadrant position. Use that line instead.

> ⚠️ **Corrected Aug 2026 — do not say Rasa lacks voice.** Rasa ships built-in connectors for
> **Twilio Media Streams, Jambonz, AudioCodes and Genesys Cloud AudioConnector**, ASR/TTS
> integrations for **Deepgram, Cartesia, Azure Speech and Rime**, and a Studio analytics dashboard
> (sessions, containment, latency, CSAT). The honest gap is commercial and operational: separate
> third-party speech contracts, and you run the stack. The widely quoted "1–3 second round trip"
> comes from Voiceflow and Dasha, both of whom sell against Rasa. Benchmark it, do not quote it.

**See also Slide 1B**, which reframes Rasa on portfolio completeness. That is the stronger slide
for an enterprise buyer.

---

## Slide 2 · Kore.ai vs ElevenLabs

**Eyebrow:** STRATEGIC POSITIONING ▪ KORE.AI VS ELEVENLABS
**Action title:** Great voice is the easy part. Running the contact centre wins the deal
**Strategic frame:** The question is not whether the voice is good. It is whether the platform
runs the operation behind it, at the capacity and in the jurisdiction the business requires.

> **Positioning note — do not run a "small vendor" play.** ElevenLabs raised $500M at an **$11B
> valuation** in Feb 2026 and crossed **$500M ARR** in April, with Cisco Webex and TELUS Digital
> partnerships. Concede voice quality, concede scale, and concede that human transfer works.
> Every gap below is taken from ElevenLabs' own pricing page, docs, or enterprise page.

| | **Kore.ai** — ENTERPRISE-GRADE, AI-NATIVE PLATFORM | **ElevenLabs** — VOICE PLATFORM, CX ADJACENT |
|---|---|---|
| **01** | **Leader in the CX category, twice over.** Named a Leader in the Gartner MQ for Conversational AI Platforms 2026, alongside Google, Salesforce and SoundHound AI, and a Leader in the Forrester Wave for customer service. The only vendor leading both. `GARTNER` `FORRESTER` | **Not evaluated in the CX category.** Does not appear in the Gartner MQ for Conversational AI Platforms 2026 or the Forrester Wave for customer service. Its Gartner Peer Insights presence sits in text-to-speech and AI dubbing. This is a category-position gap, not a company-quality gap. `GARTNER` `FORRESTER` |
| **02** | **Capacity and cost sized in the contract.** One stack across voice and digital, with per-agent, per-intent and per-tool cost attribution, and model tiering that routes the simple 80% to fast models. `EVEREST` | **Capacity is the constraint, and exceeding it costs double.** The top self-serve tier, Business at $990 a month, carries 12,375 minutes and 40 concurrent calls. Burst allows up to 3x that concurrency with the excess "charged at double the standard rate," so a volume spike is also a price spike. Enterprise concurrency is elevated but unpublished. Unused paid credits expire on downgrade or cancellation. `VENDOR` |
| **03** | **Runs the operation, not just the call.** Contact Center AI, Agent AI, Quality AI and Outbound run as one stack, with 80+ connectors, 250+ CRM and ERP integrations, cross-agent trace trees and 100% conversation evaluation. `FORRESTER` `IDC` | **The assist layer shipped, the workforce layer did not.** Agent Assist, supervisor dashboards, compliance flagging and scorecards all exist, so concede them. Absent from their contact-centre page: queueing, workforce management and campaign management. Routing and telephony remain integrations into your existing CCaaS rather than a stack they replace. `VENDOR` |
| **04** | **Residency by region, on infrastructure you choose.** Public cloud, sovereign regions, private cloud or on-premises. SOC 2 Type II, ISO 27001, PCI DSS, HITRUST, FedRAMP Moderate and GDPR, with BAAs and a public trust centre. Bring-your-own-LLM keeps inference inside the estate. `TRUST CENTRE` | **Residency covers storage, and only on Enterprise.** Isolated environments in the EU, India and Singapore, US by default, described in the docs as "an exclusive feature available to ElevenLabs' Enterprise customers." The same page states processing "may nevertheless occur outside of the selected location" unless Zero Retention Mode is enabled, that regional LLM availability varies, and that custom LLM and webhook integrations may require out-of-region processing. `VENDOR` |

**Trap questions:** "What concurrency do we get in the contract, and what does the 2x burst rate
cost at our peak?" · "Who runs queueing, workforce management and QA scoring for the human agents
once the bot transfers the call?" · "Residency covers storage. Will processing stay in region,
including your LLM calls and our webhooks?" · "Which independent analyst has evaluated you for
customer service rather than for text-to-speech?"

### ElevenLabs — what NOT to say

The earlier draft of this slide carried four claims that do not survive checking. They came from
CloudTalk and Cekura, who sell against ElevenLabs, and Metadata Marketer, an SEO aggregator.

| Do not say | Why |
|---|---|
| "Business is $825/month for 11M credits" | **Wrong.** The vendor page says **$990/month for 12,375 minutes**. |
| "Thin customer-service automation and limited production monitoring" | Rival-authored characterisation. Their docs list analytics, testing and A/B testing. |
| "'Expensive' appears 171 times in G2 reviews; Trustpilot 3.2" | SEO aggregator, unverifiable. Do not quote. |
| "Governance is unproven, guardrails are just prompts" | **Materially wrong.** They publish a trust centre, SOC 2, GDPR, HIPAA BAAs, Zero Retention Mode and regional residency. |
| "No agent assist, no QA scoring, no supervisor monitoring" | **Wrong as of Aug 2026.** All are marketed capabilities with a dedicated product page. See Slide 2B. |

---

## Slide 3 · Kore.ai vs Ringg AI

**Eyebrow:** STRATEGIC POSITIONING ▪ KORE.AI VS RINGG AI
**Action title:** A low price per minute does not clear a regulated procurement gate
**Strategic frame:** Enterprises buy agents that survive interruption, span back-end
systems, and leave an auditable trail — proven at scale, by independent evaluation.

> **Positioning note.** Concede Ringg's real strengths — price per minute, Indic-language
> coverage and fast telephony setup. The wedge is enterprise depth and proof, not cost.

| | **Kore.ai** — ENTERPRISE-GRADE, AI-NATIVE PLATFORM | **Ringg AI** — EARLY-STAGE VOICE AGENTS |
|---|---|---|
| **01** | **Proven at enterprise scale, independently.** Leader across six analyst evaluations — Gartner MQ 2025, two Forrester Waves, two Everest PEAK matrices and IDC MarketScape — with global enterprise deployments. `GARTNER` `FORRESTER` `EVEREST` `IDC` | **Early-stage proof.** $5.5M Series A led by Arkam (Jan 2026), ~$6.6M raised in total, 20+ customers and ~1.5M conversations/month, concentrated in India. No Gartner, Forrester, Everest or IDC evaluation. `PUBLIC NEWS` `VENDOR` |
| **02** | **Your data stays where the regulator requires.** Public cloud, sovereign regions, private cloud or on-premises, with data residency by region. SOC 2 Type II, ISO 27001, PCI DSS, HITRUST, FedRAMP Moderate and GDPR, BAAs signed, and a public trust centre. Bring-your-own-LLM keeps inference off third-party APIs, with PII tokenization and immutable audit trails. `VENDOR` `TRUST CENTRE` | **Data residency is roadmap, not shipped.** Ringg's own Series A announcement says the capital funds work to enable on-premise deployments for enterprises needing stricter compliance and data residency assurances, and to eliminate dependence on third-party APIs. So today there is no on-prem option, no stated regional residency, and customer audio and PII transit third-party model, STT and TTS APIs. `PUBLIC NEWS` `VENDOR` |
| **03** | **Compliance you can evidence in procurement.** Attestation reports and certifications are published and reviewable before a contract, not asserted on a web page. `TRUST CENTRE` | **Compliance is self-asserted.** SOC 2, encryption and data anonymization appear as marketing copy on the site, HIPAA on the healthcare page. No public trust centre, SOC 2 Type II report, ISO 27001, PCI DSS, HITRUST, FedRAMP, or published DPDP or GDPR position found as of August 2026. `VENDOR` |
| **04** | **The platform does the work after the call.** 80+ connectors and 250+ CRM and ERP integrations, multi-step flows across systems, cross-agent trace trees and 100% conversation evaluation. `FORRESTER` `IDC` `EVEREST` | **The platform stops at the call.** The published connector list is Google Sheets, Typeform, Shopify, Calendly, Notion and HubSpot plus a generic API request. No Salesforce or ServiceNow-class CRM, no CCaaS, WFM or QM appears on it, so CRM write-back, follow-ups and retry logic sit with the customer. `VENDOR` |

**Three-point variant.** If the slide must hold three rows, merge 02 and 03 into a single
governance point (residency roadmap plus self-asserted compliance) and keep 01 and 04.

### Ringg AI — leads to verify, NOT for customer-facing use

These circulate widely and are **retracted from the slide** because the only sources are
rival vendors selling a Ringg alternative, each asserting what "G2 reviewers" said without
quoting a review. Verify against the live G2 profile before using any of them.

| Claim | Only found in | How it is attributed |
|---|---|---|
| Agent struggles when callers interrupt or ask multi-step questions; analytics could go deeper on where calls break down | [omnidim.io](https://omnidim.io/blogs/alternatives-ringg) *(rival)* | "G2 reviewers note…" — no review quoted |
| Complex call branching, nuanced agent personas and multi-step conditional logic are difficult or impossible to configure | [tabbly.io](https://www.tabbly.io/blogs/ringg-ai-review-tabbly-alternative) *(rival)* | "G2 reviewers repeatedly flag…" — no review quoted |
| Struggles with complex multi-step workflows involving conditional logic; analytics shallow | [ringlyn.com](https://www.ringlyn.com/blog/ringlyn-ai-vs-ringg-ai-alternative/) *(rival)* | "independent evaluations suggest…" — no citation |
| Voice-only, no chat, WhatsApp, SMS or email | tabbly.io *(rival)* | Contradicted by [Ringg's own site](https://www.ringg.ai/), which lists voice, chat, WhatsApp and web |

**Sample-size caveat.** Ringlyn states Ringg AI's G2 profile carries only about **five
reviews**. If accurate, no claim of a repeated reviewer pattern is credible, and the 4.8/5
rating is a five-review average. G2 blocks automated retrieval and the G2 API account has no
catalog access for this product, so neither the count nor the rating was independently
confirmed. **Check the live profile before quoting either number.**

**Trap questions:** "Where does our customer audio and PII physically live, and which
third-party APIs does it pass through before you answer?" · "Can we see the SOC 2 Type II
report and the trust centre, or is the claim only on the website?" · "When is on-premise
generally available, with named production references on it?" · "Who updates the CRM and
schedules the follow-up after the call ends?"

---

## Sources

**Rasa**
- [Rasa Spring 2026 release — 3.16 / Studio 1.16](https://rasa.com/blog/behind-the-release-notes-product-updates-spring-2026) *(what shipped, and what is absent from the portfolio)*
- [Rasa Pro documentation](https://rasa.com/docs/pro/) *(product components: Pro, Studio, Developer Edition, Copilot)*
- [Kore.ai platform](https://www.kore.ai/platform) *(portfolio scope for the green column)*
- [G2 — Rasa reviews, pros and cons](https://www.g2.com/products/rasa/reviews?qs=pros-and-cons)
- [Gartner Peer Insights — Rasa Platform](https://www.gartner.com/reviews/product/rasa-platform)
- [Voiceflow — Rasa review: CALM, pricing and alternatives](https://www.voiceflow.com/blog/rasa-chatbot) *(tier and conversation-cap figures; vendor-adjacent blog, cross-checked against Rasa docs)*
- [Rasa documentation — editions and licensing](https://rasa.com/docs/pro/intro/)
- [CX Today — Gartner MQ for Conversational AI Platforms **2026** rundown](https://www.cxtoday.com/customer-analytics-intelligence/gartner-magic-quadrant-conversational-ai-2026/) *(current report: Leaders are Google, Salesforce, SoundHound AI, Kore.ai; Rasa and Sierra get honorable mentions without quadrant positions)*
- [CX Today — Gartner MQ 2025 rundown](https://www.cxtoday.com/customer-analytics-intelligence/gartner-magic-quadrant-for-conversational-ai-platforms-2025-the-rundown/) *(prior report; Rasa absent entirely)*

**ElevenLabs** *(rebuilt on primary sources; rival-authored sources removed)*
- [ElevenLabs — Agents pricing](https://elevenlabs.io/pricing/agents) *(tiers, concurrency, burst, overage, credit expiry)*
- [ElevenLabs — Agents platform docs](https://elevenlabs.io/docs/agents-platform/overview) *(what the platform does and does not include)*
- [ElevenLabs — Data residency docs](https://elevenlabs.io/docs/overview/administration/data-residency) *(regions, Enterprise gating, processing caveat)*
- [ElevenLabs — Enterprise page](https://elevenlabs.io/enterprise) *(SOC 2, GDPR, HIPAA BAAs, Zero Retention, named customers)*
- [ElevenLabs — Agent Assist](https://elevenlabs.io/agents/agent-assist) *(human-agent assist, supervisor dashboard, compliance flagging, scorecards, role-play training)*
- [ElevenLabs — AI call center](https://elevenlabs.io/agents/ai-call-center) *(IVR replacement, routing, CCaaS/ticketing/CRM as integrations; queueing, WFM and campaign management absent)*
- [ElevenLabs — homepage portfolio](https://elevenlabs.io/) *(media product breadth: Music, SFX, Dubbing, Narration, Scribe)*
- [ElevenLabs — Trust Center](https://compliance.elevenlabs.io/)
- [ElevenLabs — Series D](https://elevenlabs.io/blog/series-d) · [$500M ARR](https://elevenlabs.io/blog/500m-arr-and-new-investors) · [CNBC on the $11B valuation](https://www.cnbc.com/2026/02/04/nvidia-backed-ai-startup-elevenlabs-11-billion-valuation.html)
- *Removed as rival-authored or unverifiable:* CloudTalk, Cekura, Metadata Marketer

**Ringg AI**
- [YourStory — Ringg AI raises $5.5M Series A](https://yourstory.com/2026/01/voice-ai-startup-ringgai-seriesa-arkam-ventures)
- [Entrepreneur India — Ringg AI Series A](https://india.entrepreneur.com/news-and-trends/voice-ai-startup-ringg-ai-secures-usd-55-mn-series-a/502061)
- [Ringg AI — product site](https://www.ringg.ai/) *(channels, integrations, compliance and customer claims)*
- [Ringg AI — Series A announcement](https://www.ringg.ai/blog/ringg-ai-announcing-our-5-5-millon-usd-series-a) *(on-prem, data residency and third-party API dependence, in the vendor's own words)*
- [G2 — Ringg AI reviews](https://www.g2.com/products/ringg-ai/reviews)

**Kore.ai position**
- **Gartner MQ for Conversational AI Platforms 2026 (current) — Leader**, with Google, Salesforce and SoundHound AI. Kore.ai is the only vendor leading both this MQ and the latest Forrester Wave.
- Gartner MQ for Conversational AI Platforms 2025 (prior — Leaders were Google and Kore.ai)
- Forrester Wave: Conversational AI Platforms for Customer Service, Q2 2026 (Leader — Kore.ai, NiCE Cognigy, Omilia)
- [Kore.ai Trust Center](https://trust.kore.ai/) — published certifications and attestation reports
- Kore.ai deployment and compliance posture: public cloud, sovereign regions, private cloud and on-premises with data residency by region; SOC 2 Type II, ISO 27001, PCI DSS, HITRUST, FedRAMP Moderate, GDPR, BAAs; bring-your-own-LLM
- `knowledge_base/kore-ai.md` for the internal capability claims used in the green column

**Verification status:** figures were retrieved in August 2026 from the sources above.
G2 and Gartner Peer Insights block automated page retrieval, so their content reached this
document through search-result extracts — re-check the live pages before any customer-facing
use, and confirm current review counts and ratings.

---

## Slide 1B · Kore.ai vs Rasa — enterprise platform completeness
### The strongest Rasa slide. Use this one.

**Eyebrow:** STRATEGIC POSITIONING ▪ KORE.AI VS RASA
**Action title:** Rasa builds the agent. An enterprise platform runs the whole operation
**Strategic frame:** The agent is one component. A complete enterprise AI platform also equips and
measures the humans behind it, runs the employee side of the business, and ships the industry logic
you would otherwise build.

> **Do not fight Rasa capability-by-capability.** They have closed most of that gap: CALM, flows,
> MCP, A2A, an orchestrator that holds state, built-in Twilio, Jambonz, AudioCodes and Genesys voice
> connectors, a Studio analytics dashboard, and OpenTelemetry tracing. Concede all of it in one
> sentence. Then fight on scope, where the difference is structural rather than incremental.

| | **Kore.ai** — ENTERPRISE AI PLATFORM | **Rasa** — AGENT DEVELOPMENT FRAMEWORK |
|---|---|---|
| **01** | **A portfolio, not a product line.** Agent Platform {Artemis}, plus AI for Service (AI Agents, Agent AI assistance, Agentic Contact Center, Quality AI, Proactive Outreach) and AI for Work (Enterprise Search, Intelligent Orchestrator, prebuilt agents, admin controls). `VENDOR` | **One product line.** Rasa Pro, Rasa Studio, Developer Edition, Copilot and MCP Tools. Excellent at building and running an agent. That is the whole catalogue. `VENDOR` |
| **02** | **Equips and measures the humans too.** Agent assist, quality assurance and scoring, and outbound campaigns run on the same platform as the AI agents, so deflected and handled conversations sit in one system of record. `VENDOR` | **The human side of service is absent.** No agent assist, no quality management or QA scoring, no workforce management, and no outbound campaign management appear in Rasa's product documentation or in the Spring 2026 release. The bot deflects; equipping and scoring the humans is someone else's platform. `VENDOR` |
| **03** | **Prebuilt industry applications.** Banking, Healthcare, Retail, IT, HR and Recruiting ship with regulated workflows and integrations, so a vertical journey is configured rather than built. `VENDOR` | **No prebuilt industry applications.** Every vertical journey, and its compliance logic, is scoped, built, tested and maintained by the customer. Time-to-value is a build plan. `VENDOR` |
| **04** | **Employee side, marketplace and reach.** Enterprise Search and Intelligent Orchestrator for AI for Work, a marketplace of prebuilt agents and templates, 300+ integrations and 40+ channels, plus Microsoft and AWS strategic integration. `VENDOR` | **Customer-facing only, and you assemble the ecosystem.** No enterprise search, no prebuilt-agent marketplace, no template or integration catalogue. Integrations arrive through MCP and custom actions, which is flexible and is also work. `VENDOR` |

**Trap questions:** "The bot deflects 60%. Who equips, coaches and scores the humans handling the
other 40%, and which product does that?" · "When we need a banking or healthcare journey live this
quarter, are we configuring a prebuilt application or scoping a build?" · "What runs our outbound
campaigns and our employee-facing search?" · "Over three years, how many of these do we build and
maintain ourselves?"

**Where this lands and where it does not.** This slide is decisive when the buyer wants a platform
to standardise a service organisation on. It is weak when the buyer is an engineering team that
explicitly wants a framework to own, self-host and control. Against that buyer, do not run this
slide — run data residency, LLM-agnosticism and total cost instead, and expect a real contest.


---

## Slide 2B · Kore.ai vs ElevenLabs — enterprise platform completeness
### Use this with Slide 2A. Together they are the strongest pairing.

**Eyebrow:** STRATEGIC POSITIONING ▪ KORE.AI VS ELEVENLABS
**Action title:** Their portfolio grows sideways into media. Ours grows up into the enterprise
**Strategic frame:** ElevenLabs now covers the customer conversation well. An enterprise AI platform
also has to serve the enterprise's own work, and ship the industry logic that makes a quarter.

> ⚠️ **Read this before presenting.** ElevenLabs has moved fast into CX and now markets **Agent
> Assist for human agents**: real-time next-best-action and knowledge surfacing on live calls, a
> **supervisor dashboard** with live transcripts, sentiment and compliance flags, **automatic
> flagging of missed disclosures and script deviations**, **auto-generated scorecards**, after-call
> summaries with CRM sync, and **role-play training agents** with tone scoring. Agents run across
> **voice, chat, email and WhatsApp in 70+ languages**. **Concede every bit of that in one
> sentence.** Anyone claiming ElevenLabs has no agent assist or QA will be corrected in the room.

| | **Kore.ai** — ENTERPRISE AI PLATFORM | **ElevenLabs** — VOICE AND MEDIA PLATFORM WITH CX |
|---|---|---|
| **01** | **Breadth runs into the enterprise.** AI for Service (AI Agents, Agent AI assistance, Agentic Contact Center, Quality AI, Proactive Outreach) and AI for Work (Enterprise Search, Intelligent Orchestrator, prebuilt agents, admin controls), on one Artemis foundation. `VENDOR` | **Breadth runs into media.** Text to Speech, Music, Sound Effects, Voice Cloning, Dubbing, Narration and Scribe, alongside ElevenAgents and the API. World-class, and pointed at audio production rather than enterprise operations. `VENDOR` |
| **02** | **Serves employees, not only customers.** Enterprise Search, an intelligent orchestrator for internal agents, prebuilt HR, IT and Recruiting agents, and admin controls over the whole AI estate. `VENDOR` | **No employee side.** No enterprise search, no orchestrator for internal agents, no prebuilt HR, IT or Recruiting agents, and no governance plane spanning an enterprise's own AI. The platform ends at the customer conversation. `VENDOR` |
| **03** | **Prebuilt regulated industry applications.** Banking, Healthcare, Retail, IT, HR and Recruiting ship with regulated workflows and integrations, so the vertical journey is configured. `VENDOR` | **Function templates, not industry applications.** Prebuilt templates cover sales, support and scheduling. The banking or healthcare journey, and its compliance logic, is the customer's build. `VENDOR` |
| **04** | **Owns the contact-centre stack end to end.** Agent assist, quality, outbound and the AI agents run on one platform, with 300+ integrations and 40+ channels. `VENDOR` | **Assist yes, workforce no, and the stack stays yours.** Agent assist, supervisor dashboards and scorecards are real. Queueing, workforce management and campaign management are absent from their contact-centre page, and routing and telephony are integrations into your existing CCaaS. `VENDOR` |

**Trap questions:** "Assist and scorecards are there. Who runs queueing, workforce management and
campaign management, and are routing and telephony yours or our existing CCaaS?" · "What serves our
**employees** — search, internal agents, and the governance plane over them?" · "Is a banking or
healthcare journey a prebuilt application, or our build on a sales template?" · "Three years out,
how much of our enterprise AI estate does this platform cover?"

**Where this lands and where it does not.** Decisive with a buyer standardising an enterprise AI
estate across customers *and* employees. Weak where the buyer only wants the best voice agent for a
customer-facing use case — there ElevenLabs is genuinely strong, and the argument moves to Slide 2A
(orchestration ceiling), concurrency economics, and processing-level residency.


---

## Slide 2C · Kore.ai Artemis vs ElevenLabs — extended talk track

Ammunition beyond Slides 2, 2A and 2B, organised by durability. Use the **architectural** gaps in
any deal; they are design decisions, not backlog items. Use the **timing** gaps now and re-check
them each quarter, because ElevenLabs is closing gaps fast.

> ⚠️ **Correction that costs us a point.** ElevenLabs now offers **on-premise, on-device and VPC
> deployment**. The full ElevenAgents runtime runs **in your VPC, connected to your own LLM,
> telephony and retrieval**, with all text, audio and call data staying inside your infrastructure.
> The "their residency is storage-only" attack **only applies to the standard multi-tenant cloud
> service.** Against a buyer willing to take a private deployment, that argument is dead. Do not
> lead with it. ([ElevenLabs private deployments](https://elevenlabs.io/docs/eleven-api/private-deployment/overview))

### A · Architectural — durable, worth building a slide on

| # | Gap | Artemis | ElevenLabs | Source |
|---|---|---|---|---|
| **A1** | **Model routing and cost architecture** | Agents declare **tiers, not vendors**. Routing picks the model per task by cost, speed and complexity: fast models for the simple ~80%, reasoning models for the complex ~20%. | Model is configured **statically at the agent level**. No dynamic per-task routing, no tiering, and **no documented fallback** — so a model outage is an agent outage, and every turn pays the price of your most expensive turn. | `VENDOR DOCS` |
| **A2** | **Orchestration primitives** | Six: supervisor, delegation, handoff, fan-out, escalation, A2A federation. | One: handoff. Their docs: transfer is **"a conversation takeover, not a delegated subtask"** and **"the parent agent doesn't receive results back."** | `VENDOR DOCS` |
| **A3** | **A2A federation** | First-class primitive — agents collaborate across organisational boundaries. | **MCP yes, A2A not documented.** Tools are connected; cross-organisation agent federation is not addressed. | `VENDOR DOCS` |
| **A4** | **Authoring artifact** | **ABL** — a compiled, declarative language. The topology is validated and governed as a reviewable blueprint before deploy. | **Configuration, not a compiled artifact.** Dashboard settings, prompts, a visual workflow builder and API calls. No build-time validation across the whole topology, and no Git-native release engineering or pre-flight gate documented. | `VENDOR DOCS` |
| **A5** | **Topology design and self-improvement** | **Arch** translates business objectives into production-ready ABL, designs the agent topology, and **continuously refines agents from real production traces**. | **No equivalent.** Design is human configuration; there is no architect layer that proposes or refines the topology from what happened in production. | `VENDOR DOCS` |
| **A6** | **Knowledge governance** | Permission-scoped retrieval with **citations** and **stale-knowledge tracking**. | Knowledge base is documents from files, URLs or text, with **workspace-level** permissions and per-agent silos. **No documented per-end-user permission-scoped retrieval** — the control is which agent sees which document, not which *caller* is entitled to which answer. | `VENDOR DOCS` |

### B · Timing — true today, re-check every quarter

| # | Gap | Why it matters now | Source |
|---|---|---|---|
| **B1** | **Azure is not available for private deployment until later H2 2026.** Private deployments support AWS and GCP only. | Decisive for a Microsoft-standardised enterprise. Artemis **launched on Microsoft Azure with native integration to Microsoft Foundry and Agent 365**. If the buyer runs on Azure and needs data in their own tenant, ElevenLabs cannot serve them this year. | `VENDOR DOCS` |
| **B2** | **The private-deployment architecture is behind an NDA.** Full technical documentation is "available to authorized customers only." | The buyer cannot evaluate the deployment architecture, its limits, or which features are unavailable **before committing**. Ask what is missing in a private deployment versus the cloud service, and get it in writing. | `VENDOR DOCS` |
| **B3** | **Cloud-service residency is storage-scoped and Enterprise-only.** Processing "may nevertheless occur outside of the selected location"; regional LLM availability varies; custom LLM and webhook integrations may require out-of-region processing. | Still valid **only** if the buyer is taking the standard cloud service. Superseded by a private deployment. | `VENDOR DOCS` |
| **B4** | **Concurrency ceiling and 2× burst.** Business tier at $990/month carries 40 concurrent calls; burst allows 3× concurrency with the excess at double rate; Enterprise concurrency unpublished. | A volume spike is also a price spike. Get the contracted concurrency and the burst rate in the commercials. | `VENDOR PRICING` |
| **B5** | **Reach and ecosystem.** Voice, chat, email and WhatsApp; integrations via MCP, named CRMs and 200+ telephony providers. | Artemis: **40+ voice and digital channels, 300+ integrations**, plus a marketplace of prebuilt agents and templates. | `VENDOR` |

### The three questions to actually ask

1. **"When a simple intent and a complex one hit the same agent, do they use the same model?"**
   Yes is the answer, and it means the buyer pays reasoning-model prices for every "what is my balance."
2. **"Can a supervisor agent delegate a task, keep control, and receive the result?"**
   No. The conversation leaves and does not come back.
3. **"We are an Azure shop and our data stays in our tenant. When can you deploy there?"**
   Later in H2 2026, on their own documentation.

### What NOT to claim about ElevenLabs

This card has been corrected four times. Every one of these was in an earlier draft and is wrong:

| Retired claim | Reality |
|---|---|
| "No on-prem or VPC — SaaS only" | Full ElevenAgents runtime deploys to your VPC, on-prem, or on-device. |
| "No agent assist, QA scoring or supervisor monitoring" | All marketed, with a dedicated product page. |
| "Governance unproven, guardrails are just prompts" | Trust centre, SOC 2, GDPR, HIPAA BAAs, Zero Retention Mode. |
| "Business is $825/month for 11M credits" | $990/month for 12,375 minutes. |

**Standing instruction:** re-verify this card against elevenlabs.io product pages before every
customer-facing use. Four corrections in one research pass is the rate this vendor moves at.


---

# Part 2 · Agentic capability gaps

Part 1 compares platforms. This part compares **agentic architecture** — what happens when one
customer request has to be worked by several agents, across several systems, under a policy that
must hold. It is the sharper axis, because it is where Kore.ai's Artemis generation is furthest
ahead and where the differences are checkable in each vendor's own documentation.

## The Kore.ai yardstick (Artemis)

| Capability | What Artemis provides |
|---|---|
| **Orchestration primitives** | **Six**: supervisor, delegation, handoff, fan-out, escalation, and agent-to-agent federation |
| **Memory** | **Dual-brain** — agentic reasoning and deterministic flows run **in parallel through shared memory**, in one language, under one runtime |
| **Authoring** | **ABL**, a compiled, declarative language: agents, systems and workflows are defined, validated and governed as reviewable blueprints |
| **Topology design** | **Arch** translates business objectives into production-ready ABL, designs the agent topology, and refines agents from real production traces |
| **Governance** | Enforced architecturally: every decision, path and outcome logged, traced and analysed in real time; deterministic constraints enforced by the platform, not the model |
| **Reach** | 40+ voice and digital channels, 300+ integrations |

Source: [Kore.ai — Artemis launch](https://www.kore.ai/news/kore-ai-launches-artemis-the-new-generation-of-the-kore-ai-agent-platform-for-building-governing-and-optimizing-enterprise-ai).
⚠️ **Reconcile before use:** the launch release says **six** primitives; the existing internal
strategic-positioning slide says **five**. Confirm which is current with product marketing.

---

## Slide 1A · Kore.ai vs Rasa — agentic

**Action title:** One assistant calling out is not a multi-agent system
**Strategic frame:** Rasa orchestrates. The question is what it orchestrates: tools and external
agents from a single assistant, or a governed topology of agents working a request together.

> **Do not say Rasa is "just an NLU framework."** It is outdated. Rasa 3.14 ships **A2A**, **MCP**,
> process calling, and an orchestrator that maintains state. Concede that, then go to topology,
> telemetry, and where policy is enforced.

| | **Kore.ai** — ARTEMIS | **Rasa** — SINGLE-ASSISTANT ORCHESTRATOR |
|---|---|---|
| **01** | **Six orchestration primitives.** Supervisor, delegation, handoff, fan-out, escalation and A2A federation, so one request can be decomposed across agents with a supervisor retaining control. `VENDOR` | **Orchestration outward, not a topology.** Rasa's orchestrator directs control between flows, MCP tools, A2A agents, RAG or fallback, and maintains state. Its orchestration page names **no supervisor, delegation, fan-out or escalation pattern**. It is one assistant calling out, not several agents working a request in parallel. `VENDOR` |
| **02** | **Shared memory across the topology.** Agentic reasoning and deterministic flows run in parallel over shared memory, in one language, under one runtime. `VENDOR` | **State per assistant.** Rasa tracks short memory, active state and persistent knowledge for the assistant. There is no documented shared working memory across a set of collaborating agents. `VENDOR` |
| **03** | **Telemetry is the platform.** Every decision, path and outcome logged, traced and analysed by AI in real time, with cross-agent trace trees. `VENDOR` | **Telemetry is a stack you assemble.** Tracing requires standing up Jaeger, an OpenTelemetry Collector or Langfuse and wiring it, and **metrics only emit once tracing is configured**. Real capability, but it is your integration project and your on-call. `VENDOR` |
| **04** | **Policy compiled, then enforced by the runtime.** ABL validates the topology before deploy; deterministic constraints are enforced by the platform, not left to the model. `VENDOR` | **Policy enforced inside flows.** Business rules hold within guided flows, but there is no compiled contract spanning agents, tools and handoffs that fails at build time. `VENDOR` |

**Trap questions:** "When one request needs three agents working in parallel with a supervisor
holding the outcome, what builds that?" · "Who stands up and runs your tracing backend, and what
happens to metrics if it is not configured?" · "Where is a cross-agent policy validated — at build
time, or the first time it runs in production?"

---

## Slide 2A · Kore.ai vs ElevenLabs — agentic

**Action title:** A handoff is one primitive, not an orchestration layer
**Strategic frame:** ElevenLabs agents can pass a call to another agent. They cannot delegate a
task and get the answer back. That single architectural fact sets the ceiling.

> **The strongest technical point on any of these slides, and it is quoted from their own docs.**

| | **Kore.ai** — ARTEMIS | **ElevenLabs** — AGENT TREE, ONE-WAY |
|---|---|---|
| **01** | **Six primitives, including delegation and fan-out.** A supervisor can dispatch work to several agents at once, retain control, and assemble the result. `VENDOR` | **One primitive: handoff.** `transfer_to_agent` moves the conversation to a child agent permanently. The docs state the transfer is **"a conversation takeover, not a delegated subtask"** and **"the parent agent doesn't receive results back."** No delegation, no fan-out, no supervisor that keeps control. `VENDOR` |
| **02** | **Parallel work on one request.** Fan-out queries several systems or agents simultaneously and reconciles the answers. `VENDOR` | **Sequential by construction.** With no fan-out, a request spanning three systems is worked in sequence inside one agent, or handed away and gone. `VENDOR` |
| **03** | **Shared memory, not a transcript.** Agents share working memory under one runtime, so context is structured state rather than replayed dialogue. `VENDOR` | **Context is the transcript.** The full transcript, language and audio settings inherit on transfer, and transfer tool calls are stripped from the child's view. Useful, but it is conversation history, not shared working state. `VENDOR` |
| **04** | **Compiled and governed before deploy.** ABL blueprints are validated and governed; the runtime enforces deterministic constraints. `VENDOR` | **Configured, then judged at run time.** Behaviour lives in prompts, a visual workflow builder, and pre-deployment simulations. The model decides at run time whether the rule applies. `VENDOR` |

**Trap questions:** "Can a supervisor agent delegate a task, keep control, and receive the result —
or does the conversation simply leave?" · "How do three systems get queried at once on a single
request?" · "When a compliance step must run every time, what enforces it — the platform, or the
model's judgement in that moment?"

---

## Slide 3A · Kore.ai vs Ringg AI — agentic

**Action title:** A prompt and a webhook is not an agent architecture
**Strategic frame:** Ringg automates a call well. Agentic work means decomposing a request across
agents and systems, holding state, and proving what happened.

> **Phrase as "not documented," not "does not exist."** These are absences from Ringg's developer
> docs as of August 2026. Ask them to point at the documentation.

| | **Kore.ai** — ARTEMIS | **Ringg AI** — SINGLE-PROMPT VOICE AGENT |
|---|---|---|
| **01** | **Six orchestration primitives and a designed topology.** Arch translates business objectives into ABL and designs the agent topology. `VENDOR` | **No documented multi-agent capability.** The developer docs cover prompt variables, knowledge bases, call-history APIs and webhooks. **No agent transfer, no multi-agent orchestration, and no MCP** appear in them. `VENDOR` |
| **02** | **Governed tool layer.** 300+ integrations with typed, validated tool contracts compiled into the blueprint. `VENDOR` | **Tool use is webhook-shaped.** A generic API request action plus a small set of SaaS connectors (Google Sheets, Typeform, Shopify, Calendly, Notion, HubSpot). Not a governed tool layer with typing, auth and build-time validation. `VENDOR` |
| **03** | **Shared memory across agents and sessions.** `VENDOR` | **No documented memory across sessions.** Nothing in the docs describes persistent state carried between conversations. `VENDOR` |
| **04** | **Evaluation and trace as platform features.** Every decision logged, traced and analysed in real time; agents refined from production traces. `VENDOR` | **No documented evaluation framework or model choice.** Observability is call-history APIs and webhooks for call started, completed, recording and analysis. `VENDOR` |

**Trap questions:** "Show us the documentation for agent-to-agent orchestration and tool calling." ·
"What does the agent remember about this customer from last week?" · "How do you evaluate agent
behaviour before a release, and what does the trace of a failed call look like?"

---

## Sourcing note for Part 2

Every claim in Part 2 comes from a **vendor's own product documentation or launch material** —
Kore.ai's Artemis release, Rasa's orchestration page and Rasa Pro tracing docs, ElevenLabs' agent
transfer and Agents docs, and Ringg's developer docs. No rival-authored comparison content is used
anywhere in this part.

- [Kore.ai — Artemis launch](https://www.kore.ai/news/kore-ai-launches-artemis-the-new-generation-of-the-kore-ai-agent-platform-for-building-governing-and-optimizing-enterprise-ai)
- [Rasa — AI orchestration](https://rasa.com/orchestration) · [Rasa Pro tracing](https://rasa.com/docs/pro/improve/tracing/) · [observability metrics](https://rasa.com/docs/pro/improve/observability-metrics/) · [A2A and MCP](https://rasa.com/blog/orchestrating-a2a-and-mcp-with-rasa)
- [ElevenLabs — agent transfer](https://elevenlabs.io/docs/eleven-agents/customization/tools/system-tools/agent-transfer) · [Agents platform overview](https://elevenlabs.io/docs/agents-platform/overview)
- [Ringg AI — developer docs](https://docs.ringg.ai/)

**Absence claims** ("no supervisor pattern named", "not documented") mean the capability is absent
from the vendor's published documentation as of August 2026. Put it to them as a question.
