---
type: Source
title: 'Passive capture: knowledge that writes itself, with humans who approve it'
resource: https://muthub.org/writing/passive-capture.md
hash: sha256:9785f3e599fd605f9d27ae9d2f95cfcb8ccfab29cf446d08643df7ed67cf30d0
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2026-08-18'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Passive capture: knowledge that writes itself, with humans who approve it

Published 2026-08-18. Part 4 of the Context Engineering series.

**Documentation fails because it is a second job, so stop asking people to write it and start capturing what their work already produces.** Every enterprise has tried to fix knowledge with a documentation push. A wiki is launched, templates are written, teams are asked to keep pages current. Six months later the pages are stale and the effort quietly ends.

The problem is design, not discipline. Engineers are measured on shipping, and writing about what they shipped always loses that contest. Yet the knowledge we want is already being produced every day, as a by-product of the work itself.

## The exhaust of work

- **Commits and pull requests** explain what changed and, in review comments, why.
- **Tickets** capture intent, acceptance criteria and the decisions made along the way.
- **Incidents and post-mortems** record failure modes, blast radius and fixes.
- **Change and problem records** capture what was approved, what went wrong and what was learned.
- **Architecture reviews and decision records** capture the trade-offs. Michael Nygard introduced [architecture decision records](https://www.redhat.com/en/blog/architecture-decision-records) in 2011 because the reasoning behind decisions stays with whoever made them, and newcomers are left guessing.
- **Chat** captures the real debate, and then scrolls it away.

Foundation Capital calls the missing piece [decision traces](https://ashugarg.substack.com/p/ais-trillion-dollar-opportunity-context): the inputs gathered, the policy applied, the exception granted and who approved it. Systems of record keep the outcome and lose the trace. In their words, the reasoning connecting data to action was never treated as data in the first place. The opportunity is to capture it where the work happens, instead of asking people to reconstruct it later.

## Passive, not automatic

Passive capture means harvesting these signals without asking anyone to do extra work. It does not mean publishing whatever a model extracts. Raw exhaust is noisy, sensitive and often wrong. Between capture and trust sits a distillation process with five steps.

1. **Strip and redact.** Remove personal and sensitive data before anything else touches it. This is a security requirement, not an option.
2. **Classify.** Decide what kind of knowledge a signal carries: a dependency, a failure mode, a decision, an owner, a runbook step.
3. **Extract.** Pull out the lasting fact and discard the conversation around it.
4. **Reconcile.** Merge it with what is already known, resolve conflicts and flag contradictions.
5. **Approve.** A human who owns the application reviews the change before it becomes trusted context.

## Why the human gate matters

It is tempting to remove the human to go faster. Resist it. Generated documentation becomes fluent long before it becomes reliable, which is the [trust gap I wrote about last year](/writing/living-documentation-trust-gap): a page that is 90% right still needs a human, because nobody knows which 10% is wrong. A confident, wrong page is more dangerous than an empty one, because people and agents trust it. In regulated industries the approval is also the evidence: it shows who verified a piece of knowledge and when.

The trick is to make approval cheap. Do not ask owners to write. Ask them to review a proposed change, the way they already review a pull request. Agents do the drafting, merging and cross-referencing that humans neglect. As Karpathy put it in the gist behind the LLM wiki pattern, quoted in [Google's Open Knowledge Format announcement](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing), LLMs "don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass." People supply the judgment.

> Code fast, verify hard, and keep the humans in the loop.

Here is the counterintuitive part. The human gate is what makes the system fast over time, not what slows it down. Without it, a single confidently wrong page can poison trust in the whole layer, and teams go back to asking the expert. With it, every approved fact carries a name and a date, and people stop double-checking.

A practical decision rule keeps the gate cheap: tier it by consequence. A new contact name or a corrected link can be published as a clearly labeled draft and confirmed in a weekly batch. A new failure mode, a changed dependency, or anything that would alter how someone responds to an incident needs the owner's approval before agents treat it as verified. The review load stays small, and the risky changes still get a human.

## A feedback loop, not a pipeline

Passive capture is not a one-way flow. Every time an agent uses context and a person corrects it (an answer was wrong, a dependency was missing, a runbook step was outdated) that correction is itself a signal. Feed it back through the same steps. Over time the knowledge corrects itself where it is used, which is the only place anyone notices errors.

The failure mode to watch for is the rubber stamp. If owners approve every proposal within seconds, the gate has turned into theater. I would sample a few approved changes each month and check them against their sources, the way internal audit samples a control. When the sample turns up errors, the fix is usually upstream, in better classification or tighter extraction, rather than more reviewers.

## An incident, end to end

Here is what this looks like in practice. An incident is resolved and its post-mortem is written, as it would be anyway. The capture process reads the record and the linked change, strips personal data, and classifies what it found: a new failure mode, a dependency that was never documented, and a runbook step that turned out to be wrong.

It drafts three small updates to the application's context, each linked to its source, and opens them for review. The application owner approves two and corrects the third in a couple of minutes. The next time that failure appears, every person and agent sees the updated knowledge, with a note saying who verified it and when. No one wrote documentation, and the knowledge still improved, because it was harvested from work that had to happen anyway.

## Security, privacy and restraint

Harvesting operational signals means touching sensitive material: customer identifiers in tickets, credentials pasted into chat, internal names in incident notes. Redaction has to happen at the very start, before classification or any model sees the content. Access rules should follow the source. If a person could not read the original ticket, they should not be able to read knowledge derived from it. Every derived fact keeps a link to its source, so an auditor can trace any statement back to the evidence.

Restraint matters as much as reach. Some material should never be harvested: personal conversations, performance discussions, privileged legal advice, anything a person reasonably expected to be ephemeral. Be explicit about which sources are in scope, tell people, and prefer structured, work-related signals over ambient monitoring. A context layer that feels like surveillance will lose the trust it depends on, and the best knowledge comes from teams who see the system working for them.

## How to know it is working

- **Coverage:** the share of critical applications with current, owner-approved context.
- **Freshness:** the share of knowledge verified within its review window.
- **Reuse:** how often agents and people answer questions from the layer instead of escalating to an expert.
- **Time to context:** minutes from the start of an incident or change to having the background needed to act.

## Where to start

- **Start with incidents.** They are high-signal, already reviewed and painful enough that teams welcome help.
- **Capture decisions at the point of approval.** If an architecture or change review happens in a tool, record the rationale there, structured and linked.
- **Measure the approval load.** If owners spend more than a few minutes a week approving, the process is not filtering enough.
- **Track freshness.** Every captured fact gets a date and a review-by date, so decay is visible instead of silent.

**What to do on Monday morning:**

- Take one incident from last month, have an agent draft the context updates its post-mortem implies, and ask the owner to review them.
- Publish a short list of sources in scope for capture, and those explicitly excluded, to the teams whose work it touches.
- Set a target for owner approval time, such as ten minutes a week, and measure it from the first pilot.
- Add a last-verified date and a review-by date to every runbook for one critical service.

Think about the last major incident your teams resolved: how much of what they learned is written down anywhere an agent could find it today?

**Bottom line:** Stop asking people to document. Capture the knowledge their work already produces, distill it with agents, and keep a human approval gate before it becomes trusted. Knowledge that writes itself, with people who sign for it.
