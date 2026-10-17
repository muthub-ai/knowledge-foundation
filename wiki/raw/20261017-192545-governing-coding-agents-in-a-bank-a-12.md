---
type: Source
title: 'Governing coding agents in a bank: a 12-point checklist'
resource: https://muthub.org/playbooks/governing-coding-agents.md
hash: sha256:ab2934934c2bc5c6112d063bc8f969ba31832ed2fa423b404fac0c032663bead
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2026-10-11'
origin_kind: own-post
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Governing coding agents in a bank: a 12-point checklist

Reviewed 2026-10-11.

Most banks I talk to are past the question of whether to use coding agents. The question now is what has to be true before agents touch code that moves money, holds customer data or sits in front of a regulator. This is my answer, written as a checklist you can hold a program against.

None of these controls is exotic. What separates programs that scale from programs that stall is doing all twelve at once, and building them into the platform instead of a review board. If a control depends on someone remembering to apply it, agents will outrun it within a quarter.

## 1. Write down what each agent may do

Scope every agent by repository, environment and action: read, propose, commit, deploy. Default to propose-only and widen access per use case. [OWASP calls the failure mode excessive agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/), and it is the easiest one to prevent on day one.

Check: Every agent has a written scope, and the platform enforces it.

## 2. Give every agent its own identity

No shared service accounts and no long-lived tokens pasted into configuration. Each agent gets a workload identity with short-lived credentials, so every action is attributable. Patterns such as [SPIFFE](https://spiffe.io/docs/latest/spiffe-about/overview/) and the [MCP authorization specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) show the direction.

Check: You can name which agent made any change, and revoke it in minutes.

## 3. Send every model call through one gateway

A single AI gateway gives you one place for the model allowlist, logging, data-loss controls, rate limits and cost. Teams that wire models directly into tools end up with as many policies as they have teams.

Check: No production path calls a model except through the gateway.

## 4. Govern the tools as well as the models

Agents act through tools, and tool descriptions are an attack surface: [Invariant Labs showed tool poisoning](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) in practice. Keep an internal registry of approved MCP servers and block the rest, the way [GitHub added registry and allowlist controls](https://github.blog/changelog/2025-09-12-internal-mcp-registry-and-allowlist-controls-for-vs-code-insiders/) for Copilot.

Check: Unregistered tool servers are blocked by default.

## 5. Curate the context agents read

Agents follow whatever standards they can see. Give them your approved patterns, architecture decisions and security standards as owned, dated context, and retire stale material. [Anthropic treats context as a finite resource](https://anthropic.com/engineering/effective-context-engineering-for-ai-agents); in a bank it is also a control.

Check: Every context source an agent reads has an owner and a review date.

## 6. Put policy in the pipeline

Architecture and security rules run as code on every pull request, for human and agent changes alike, using tools such as [Open Policy Agent](https://www.openpolicyagent.org/docs). The [Architecture-as-Code prototype at aac.muthub.org](https://aac.muthub.org) shows what that looks like end to end, waivers included.

Check: A change that breaks a standard fails the build, with a named waiver path.

## 7. Keep maker and checker separate

Agents propose; a person with authority approves. Scale review effort to two questions: how far can this change reach, and how quickly can we undo it. A one-line fix in a test helper and a change to payment routing should not get the same review.

Check: No agent can approve its own change, and high-impact paths require named approvers.

## 8. Record provenance for every change

Capture which agent and model produced the change, from which spec or prompt, and who approved it. Emerging formats such as [Agent Trace](https://agent-trace.dev/) build on supply-chain ideas like [SLSA provenance](https://slsa.dev/spec/v1.0/provenance). If you cannot show why the code exists, you cannot defend it to an auditor.

Check: For any production change, you can show the agent, the inputs and the approver.

## 9. Scan everything agents add

Agents add dependencies, copy patterns and occasionally leak secrets. Run dependency, secret and license scanning on every change and keep software bills of materials current, so a new vulnerability maps to affected services in hours.

Check: Every merged change has passed dependency, secret and license checks.

## 10. Use specs for high-risk changes

For regulated logic, review the specification first and let tests trace back to it. [GitHub's Spec Kit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit) and the [Thoughtworks Radar](https://www.thoughtworks.com/radar/techniques/spec-driven-development) describe the approach. Auditors can review a contract; nobody can review every generated line.

Check: High-risk changes link to an approved spec, and tests trace to it.

## 11. Measure outcomes, not usage

Seats and prompts tell you nothing. Track delivery and stability measures in the spirit of [DORA's research](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report), plus rework and escaped defects. Be wary of perceived speed: [METR's randomized study](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) found experienced developers were slower with AI tools on their own codebases while believing they were faster.

Check: Every pilot has a baseline, a target and a gate before it scales.

## 12. Plan for the bad day

Have a kill switch per agent, a rollback path and an incident playbook for agent misbehavior, including prompt injection from content the agent reads. The [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) is a good list to red-team against. Rehearse it before an auditor or an attacker does it for you.

Check: You can disable any agent in minutes and have rehearsed doing it.

If you can tick all twelve, you are ready to widen agent access. If you cannot, the gaps tell you what to build next. Which of the twelve would your program fail today?
