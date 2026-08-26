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
| **03** | **Leader, and voice-native out of the box.** Named a Leader in the Gartner MQ for Conversational AI Platforms 2026 and the Forrester Wave for customer service, the only vendor leading both. In-house voice gateway with SSML, barge-in and sub-500ms scripted turns. `GARTNER` `FORRESTER` | **Evaluated, never a Leader, and voice is a build project.** Gartner gave Rasa an honorable mention in the 2026 MQ with no quadrant position, and Forrester included it in the 2026 Wave without naming it a Leader. As a self-hosted framework, the customer assembles and operates the voice path, STT to Rasa to TTS, and implements barge-in. `GARTNER` `FORRESTER` |

**Trap questions:** "Who ships a policy change on Friday — a business owner or your ML
engineers?" · "What is the fully-loaded cost once you add hosting, ops, upgrades and the
people to own the stack?" · "Gartner and Forrester have both looked at Rasa. Which one names
it a Leader?"

> ⚠️ **Corrected Aug 2026.** An earlier draft said Rasa has "no CX analyst validation." That is
> wrong for 2026 and a prepared buyer will catch it. Rasa *is* evaluated. It is simply never a
> Leader and holds no quadrant position. Use that line instead.

> **Caveat on the latency figure.** The widely quoted "1–3 second round trip" for a Rasa voice
> build comes from Voiceflow and Dasha, both of whom sell against Rasa. The architecture is
> verifiable from Rasa's docs; the number is not. Benchmark it rather than quoting it.

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
| **03** | **Runs the operation, not just the call.** Contact Center AI, Agent AI, Quality AI and Outbound run as one stack, with 80+ connectors, 250+ CRM and ERP integrations, cross-agent trace trees and 100% conversation evaluation. `FORRESTER` `IDC` | **Automates the call, does not run the contact centre.** The Agents docs cover knowledge base and RAG, a workflow builder, testing, analytics, SIP and Twilio telephony, batch outbound, and transfer to a human. Not in the docs: queue management, workforce management, quality management and QA scoring, supervisor monitoring, and case management. It hands a call to a human. It does not run the human side. `VENDOR` |
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
