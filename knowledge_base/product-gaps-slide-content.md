# Product Gaps — slide content (Kore.ai vs Rasa · ElevenLabs · Ringg AI)

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
| **03** | **Validated, and voice-native out of the box.** Leader in the Gartner MQ for Conversational AI Platforms 2025 and the Forrester Wave Q2 2026; in-house voice gateway with SSML, barge-in and sub-500ms scripted turns. `GARTNER` `FORRESTER` | **No CX analyst validation; voice is a build project.** Absent from both the 2025 Gartner MQ and the Forrester Wave. Voice is assembled by the customer — STT → Rasa server → TTS, a 1–3 second round trip, with barge-in as custom logic. `GARTNER` `FORRESTER` `PEER REVIEWS` |

**Trap questions:** "Who ships a policy change on Friday — a business owner or your ML
engineers?" · "What is the fully-loaded cost once you add hosting, ops, upgrades and the
people to own the stack?" · "Which independent analyst has evaluated Rasa for customer service?"

---

## Slide 2 · Kore.ai vs ElevenLabs

**Eyebrow:** STRATEGIC POSITIONING ▪ KORE.AI VS ELEVENLABS
**Action title:** Great voice is the easy part — the platform around it wins the deal
**Strategic frame:** A lifelike voice does not resolve a regulated customer request.
Enterprises need the orchestration, governance and cost control that sit behind it.

> **Positioning note — do not attack voice quality.** ElevenLabs' synthesis is genuinely
> best-in-class and Kore.ai can consume it. Concede it in the first sentence, then move the
> conversation to everything that surrounds the voice.

| | **Kore.ai** — ENTERPRISE-GRADE, AI-NATIVE PLATFORM | **ElevenLabs** — VOICE INFRASTRUCTURE |
|---|---|---|
| **01** | **A complete CX stack, not a component.** Contact Center AI, Agent AI, Quality AI and Outbound run as one stack with 80+ connectors and 250+ CRM/ERP integrations, plus prebuilt healthcare, banking and retail apps. `FORRESTER` `IDC` | **Ships a voice layer; the CX platform is your project.** Independent reviews describe a platform where "someone has to design the agent, wire the telephony, and connect the CRM," with thin customer-service automation and limited production monitoring. No native WFM, QM or case management. `PEER REVIEWS` |
| **02** | **Cost you can forecast and attribute.** Per-agent, per-intent and per-tool cost attribution, with model tiering that routes the simple ~80% to fast models and the complex ~20% to reasoning models. `EVEREST` | **Credit burn and 2× burst pricing.** Overage runs $0.08/min and doubles to $0.16/min once concurrency is exceeded; credits roll over only two cycles and are forfeited on downgrade. In the G2 corpus "expensive" appears 171 times and pricing complaints another 148; Trustpilot sits at 3.2 on pricing opacity. `G2` `VENDOR` |
| **03** | **Policy enforced at runtime, not in a prompt.** Deterministic zero-LLM mode for compliance paths, compile-time validation, cross-agent trace trees and 100% conversation evaluation — an auditable record, not a best-effort instruction. `EVEREST` | **Guardrails by instruction; no CX analyst validation.** Hallucination control is prompt guidance ("answer from the knowledge base, else say I don't know") plus pre-deployment simulations. Absent from the Gartner MQ for Conversational AI and the Forrester Wave for customer service; its Gartner Peer Insights presence sits in text-to-speech and dubbing categories. `GARTNER` `FORRESTER` `VENDOR` |

**Trap questions:** "Who builds, monitors and governs the agent once the voice sounds
great — and what does that team cost?" · "For a regulated flow, is the policy enforced at
runtime or written into a prompt, and what do you show an auditor?" · "What is your
forecast cost when volume spikes past your concurrency limit at 2× per minute?"

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
| **04** | **The platform does the work after the call.** 80+ connectors and 250+ CRM and ERP integrations, multi-step flows across systems, cross-agent trace trees and 100% conversation evaluation. `FORRESTER` `IDC` `EVEREST` | **The platform stops at the call.** Published connectors are Google Sheets, Typeform, Shopify, Calendly, Notion and HubSpot plus a generic API. Reviewers report the agent struggles with interruptions and complex requests, complex branching is hard to configure, and analytics are too shallow to show where calls break down. `G2` `PEER REVIEWS` `VENDOR` |

**Three-point variant.** If the slide must hold three rows, merge 02 and 03 into a single
governance point (residency roadmap plus self-asserted compliance) and keep 01 and 04.

**Trap questions:** "Where does our customer audio and PII physically live, and which
third-party APIs does it pass through before you answer?" · "Can we see the SOC 2 Type II
report and the trust centre, or is the claim only on the website?" · "When is on-premise
generally available, with named production references on it?" · "Who updates the CRM and
schedules the follow-up after the call ends?"

---

## Sources

**Rasa**
- [G2 — Rasa reviews, pros and cons](https://www.g2.com/products/rasa/reviews?qs=pros-and-cons)
- [Gartner Peer Insights — Rasa Platform](https://www.gartner.com/reviews/product/rasa-platform)
- [Voiceflow — Rasa review: CALM, pricing and alternatives](https://www.voiceflow.com/blog/rasa-chatbot) *(tier and conversation-cap figures; vendor-adjacent blog, cross-checked against Rasa docs)*
- [Rasa documentation — editions and licensing](https://rasa.com/docs/pro/intro/)
- [CX Today — Gartner MQ for Conversational AI Platforms 2025 rundown](https://www.cxtoday.com/customer-analytics-intelligence/gartner-magic-quadrant-for-conversational-ai-platforms-2025-the-rundown/) *(full quadrant list; Rasa appears nowhere)*

**ElevenLabs**
- [ElevenLabs — Agents pricing](https://elevenlabs.io/pricing/agents)
- [CloudTalk — ElevenLabs voice agent review](https://www.cloudtalk.io/blog/elevenlabs-voice-agent-review/) and [pricing guide](https://www.cloudtalk.io/blog/elevenlabs-pricing/)
- [Cekura — ElevenLabs review: what real users say](https://www.cekura.ai/blogs/elevenlabs-review)
- [Metadata Marketer — ElevenLabs intelligence report](https://metadatamarketer.com/elevenlabs-intelligence-report/) *(G2 keyword counts, Trustpilot 3.2)*
- [Gartner Peer Insights — ElevenLabs](https://www.gartner.com/reviews/product/elevenlabs-1305017004)

**Ringg AI**
- [YourStory — Ringg AI raises $5.5M Series A](https://yourstory.com/2026/01/voice-ai-startup-ringgai-seriesa-arkam-ventures)
- [Entrepreneur India — Ringg AI Series A](https://india.entrepreneur.com/news-and-trends/voice-ai-startup-ringg-ai-secures-usd-55-mn-series-a/502061)
- [Ringg AI — product site](https://www.ringg.ai/) *(channels, integrations, compliance and customer claims)*
- [Ringg AI — Series A announcement](https://www.ringg.ai/blog/ringg-ai-announcing-our-5-5-millon-usd-series-a) *(on-prem, data residency and third-party API dependence, in the vendor's own words)*
- [G2 — Ringg AI reviews](https://www.g2.com/products/ringg-ai/reviews)

**Kore.ai position**
- Gartner MQ for Conversational AI Platforms 2025 (Leader — Google and Kore.ai)
- Forrester Wave: Conversational AI Platforms for Customer Service, Q2 2026 (Leader — Kore.ai, NiCE Cognigy, Omilia)
- [Kore.ai Trust Center](https://trust.kore.ai/) — published certifications and attestation reports
- Kore.ai deployment and compliance posture: public cloud, sovereign regions, private cloud and on-premises with data residency by region; SOC 2 Type II, ISO 27001, PCI DSS, HITRUST, FedRAMP Moderate, GDPR, BAAs; bring-your-own-LLM
- `knowledge_base/kore-ai.md` for the internal capability claims used in the green column

**Verification status:** figures were retrieved in August 2026 from the sources above.
G2 and Gartner Peer Insights block automated page retrieval, so their content reached this
document through search-result extracts — re-check the live pages before any customer-facing
use, and confirm current review counts and ratings.
