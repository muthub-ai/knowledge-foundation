---
type: Source
title: If you can't prove why an AI wrote it, you can't ship it
resource: https://muthub.org/writing/if-you-cant-prove-why-an-ai-wrote-it.md
hash: sha256:6e8f59afd70156179c68ab30dccf45bcf4fa306bd67c7a52d8265b253fd620f4
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2026-02-24'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# If you can't prove why an AI wrote it, you can't ship it

Published 2026-02-24. Adapted from my LinkedIn post of February 21, 2026.

**If you cannot prove why an AI wrote a function, you cannot safely deploy it.** Shipping AI-generated code without tracking its origin and reasoning looks like velocity. In a regulated environment it is unmanaged risk with a delayed invoice.

When a remote agent introduces a vulnerability, the first question from risk and audit will be simple: which model produced this, from what instruction, and who approved it? Most teams today cannot answer. We need **deterministic provenance** for non-deterministic models, and it is time to extend the software bill of materials into an **AI bill of materials**.

## Provenance is an old idea with a new gap

The software supply chain community already solved part of this. SLSA defines provenance as ["the verifiable information about software artifacts describing where, when and how something was produced."](https://slsa.dev/spec/v1.0/provenance) Build systems can now attest to what they built. That covers the pipeline from source to artifact.

The gap is upstream of the source. `git blame` tells you which account committed a line. It does not tell you whether a person wrote it, an agent wrote it, or a person accepted an agent's suggestion after a quick look. When the author field is a developer and the actual author is a model, your audit trail is accurate and misleading at the same time.

## The problem with autonomous agents

Remote and multi-agent platforms work asynchronously. They read codebases, run terminal commands and commit changes with little oversight. If an agent hallucinates a dependency or corrupts a configuration file mid-task, an ordinary rollback is not enough. You have to revert both the code and the agent's working context, or it repeats the same mistake from the same bad assumptions.

There is also a timing problem that I think gets too little attention. Provenance has to be captured when the code is created. It cannot be reconstructed afterwards. Prompts, intermediate reasoning and tool calls are ephemeral by default. If the record was not written at the moment of generation, no forensic effort will recover it six months later when an examiner asks.

## Three patterns for code provenance

1. **Attribution mapping.** A vendor-neutral record maps specific line ranges to the model and conversation that produced them, creating an audit trail for debugging after deployment.
2. **Git-native session state.** The AI session itself becomes version-controlled metadata: prompts, reasoning and token usage stored alongside the code, so both the code and the agent's context can be recovered.
3. **Centralized telemetry and governance.** Platform audit logs and code referencing satisfy baseline governance, but abstract step-by-step reasoning away from the version-control history.

The first pattern now has a concrete form. [Agent Trace](https://agent-trace.dev/) is an open specification started by Cursor and published as a version 0.1.0 RFC in January 2026. It records file paths, line ranges, a model identifier, a link to the producing conversation and a contributor type of human, AI, mixed or unknown, and its schema covers Git, Mercurial and Jujutsu. It is a request for comments, not a settled standard, but it is the first vendor-neutral format I have seen that asks the right questions. The second pattern has tools too. Earlier this month Entire [released its open-source CLI](https://entire.io/blog/hello-entire-world), which hooks into Git to capture agent sessions as checkpoints on a separate branch and lets you rewind to a known-good state.

These patterns are complementary, not competing. Attribution answers "what did the AI touch?" Session state answers "why did it do that?" Central telemetry answers "is this happening across the enterprise, and is it within policy?" A regulated team needs all three answers, at different levels of detail for different audiences.

## What I found testing it

I evaluated a Git-native checkpointing tool locally with Claude Code, using an auto-commit strategy. It created a checkpoint after every agent response, capturing system state and reasoning without manual effort. When the agent drifted and corrupted a file, one rewind command restored both the codebase and the agent's memory to the last known-good state.

The experience changed how I think about rollback. Reverting code is a solved problem. Reverting *intent* is not, and that is what actually stops an agent from making the same mistake twice. It also raised a trade-off I had not anticipated: session history contains whatever the developer typed, which can include customer details, credentials pasted by mistake or internal design notes. Capturing everything creates a new store of sensitive data. Provenance records need the same classification, retention and access controls as the code they describe, and possibly stricter ones.

## From SBOM to AI-BOM

Line-level attribution covers the code. The models and data behind your AI systems need their own inventory. CycloneDX's [ML-BOM](https://cyclonedx.org/capabilities/mlbom/) extends the bill of materials to represent models, datasets and their dependencies, including dataset provenance and training configuration. Pair that with code attribution and you can answer the question regulators will ask with increasing frequency: which model versions touched which production systems?

The [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) gives the governance frame, organized around Govern, Map, Measure and Manage, with a generative AI profile published in July 2024. None of it works without records. You cannot measure or manage what you never captured.

## A decision rule for depth

Not every line needs the same treatment. My rule of thumb is that provenance depth should scale with blast radius. Internal tooling can live with attribution and central logs. Code that moves money, touches customer data or enforces a control should carry full session history and named human approval, retained for as long as the code runs. The goal is a proportionate record, set in policy, not maximum logging everywhere.

Starting is less work than it sounds. Pick an attribution format, preferably an open one, and require it from the coding tools you buy. Decide where session history lives and who can read it. Then add one pipeline check that refuses a merge into a high-risk repository when the provenance record is missing. That last step matters most. Provenance that is optional decays the same way architecture documents do: everyone agrees it is valuable, and nobody keeps it current.

So I will ask the question I put to my own teams: if an examiner pointed at one AI-written function in production tomorrow, how long would it take you to show who prompted it, which model wrote it and who approved it?

**Bottom line:** Provenance is not paperwork. It is what lets a regulated team say yes to agents: every change traceable to its intent, its model and the person who approved it, captured at creation and governed like the code itself.
