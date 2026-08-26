# Battle lines — Kore.ai Artemis vs ElevenLabs

Say the line. Show the proof. Ask the question.

---

## 1. Their agents can leave a conversation. They cannot delegate one.

**Proof —** ElevenLabs' own engineering blog: the architecture *"does not support traditional
parallel execution or supervisor delegation with returns."* Their docs on agent transfer:
*"a conversation takeover, not a delegated subtask"* and *"the parent agent doesn't receive
results back."*

**Artemis —** Six orchestration primitives. Supervisor, delegation, handoff, fan-out, escalation,
agent-to-agent federation.

**Ask —** "Can a supervisor delegate a task, keep control, and get the answer back?"

---

## 2. One model for every turn. You pay reasoning prices to check a balance.

**Proof —** The model is fixed per agent. No routing by cost, speed or complexity. And LLM cost is
billed **on top** of the $0.08 per minute.

**Artemis —** Agents declare tiers, not vendors. Fast models take the simple 80%. Reasoning models
take the complex 20%.

**Ask —** "When a balance check and a dispute hit the same agent, do they use the same model?"

---

## 3. No fallback. A model outage is an outage.

**Proof —** No model fallback anywhere in their documentation. One provider, one agent, one point
of failure.

**Artemis —** Provider-agnostic by design. Agents declare a tier and the platform routes.

**Ask —** "OpenAI goes down at 9am Monday. What happens to our contact centre?"

---

## 4. Their access control asks which agent. Ours asks which customer.

**Proof —** Knowledge base permissions are workspace-level, with silos between agents. The control
is which agent sees which document.

**Artemis —** Permission-scoped retrieval with citations. The agent returns only what this caller
is entitled to see, and shows where it came from.

**Ask —** "Two customers ask the same question. What stops the agent answering from a document only
one of them is entitled to?"

---

## 5. Azure? Not this year.

**Proof —** Private deployment runs on AWS and GCP. Azure arrives later in H2 2026.

**Artemis —** Launched on Microsoft Azure with native Microsoft Foundry and Agent 365 integration.

**Ask —** "We are an Azure shop and our data stays in our tenant. When can you deploy there?"

---

## 6. You sign an NDA to see how it deploys.

**Proof —** Their private-deployment documentation is *"available to authorized customers only."*

**Artemis —** Deployment architecture is on the table during evaluation.

**Ask —** "What is missing in a private deployment versus your cloud? Put it in writing."

---

## 7. Forty concurrent calls. Then the price doubles.

**Proof —** Business tier, $990 a month, 40 concurrent calls. Burst gives 3x concurrency with the
excess at double rate. Enterprise concurrency is not published.

**Ask —** "What concurrency is in our contract, and what does peak cost at the burst rate?"

---

## 8. They built a remarkable voice. We built the platform that runs the business.

**Proof —** Their portfolio grows into music, sound effects, dubbing and narration. There is no
enterprise search, no orchestrator for internal agents, no prebuilt HR, IT or Recruiting agents.

**Artemis —** AI for Service and AI for Work on one foundation. Banking, Healthcare, Retail, IT, HR
and Recruiting applications ship prebuilt.

**Ask —** "What serves our employees?"

---

## Two rules

**Concede the voice.** Immediately, and without qualification. It is the best in the market and
Artemis can consume it. Arguing it costs credibility and wins nothing.

**Do not attack their compliance or their deployment options.** They hold SOC 2, GDPR and HIPAA
BAAs, publish a trust centre, and now deploy on-premise, on-device and in your VPC. Those attacks
are spent. Lines 1 through 4 are architecture and will hold. Lines 5 and 6 are true this year.
