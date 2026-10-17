---
type: Source
title: Three architectures for AI coding agents, and how enterprises should choose
resource: https://muthub.org/writing/three-architectures-for-ai-coding-agents.md
hash: sha256:3941a65959a49496228aefbae50601713d42394dfa166dc324635be4bb6ab5cf
generated:
  by: seed-import/1.0
  at: '2026-10-17T19:25:45+00:00'
published_at: '2025-12-16'
origin_kind: own-essay
license_note: Own work by the author; reproduced in full
author: human:muthu
---

# Three architectures for AI coding agents, and how enterprises should choose

Published 2025-12-16. Adapted from my LinkedIn posts of May 19, 2025 and December 13, 2025.

**Coding agents should be chosen by how their work gets verified, not by which model sits underneath.** Within one week in May 2025, Google DeepMind, OpenAI and GitHub each shipped a serious coding agent. They shared a goal, taking real software work off engineers' plates, but they rested on different architectural philosophies. Seven months on, I think those differences matter more to enterprises than the benchmark race does.

What separates them is less about capability and more about trust. Each design answers the question "why should I believe this change is safe?" in its own way, and that answer decides where it fits in a regulated firm.

## Platform-embedded: trust the controls you already have

[GitHub's Copilot coding agent](https://github.blog/news-insights/product-news/github-copilot-meet-the-new-coding-agent/), announced on May 19, 2025, lives inside the platform where code already flows. You assign it an issue. It spins up an environment on GitHub Actions, uses retrieval over code search for context, can be extended with Model Context Protocol servers, and pushes commits to a draft pull request.

The interesting part is governance. The agent can only push to branches it created. The developer who asked for the pull request cannot approve it. Its pull requests need human approval before CI/CD workflows run, and existing rulesets still apply. For a bank this is the easiest model to adopt, because it inherits maker/checker controls the firm has already proven. The limit is that it is only as good as those controls. If branch protection and review discipline are weak, the agent amplifies the weakness.

## Sandboxed execution: trust the evidence

[OpenAI's Codex](https://openai.com/index/introducing-codex/), launched as a research preview on May 16, 2025, takes a different stance. Each task runs in its own isolated cloud sandbox preloaded with the repository, and at launch internet access was switched off during execution. The agent works on many tasks in parallel and returns its changes with citations to terminal logs and test output as evidence of what it did. Repositories can carry an AGENTS.md file telling it which tests to run and which conventions to follow.

Here trust comes from isolation plus proof. That suits enterprises with strong test suites and a habit of asking for evidence. It suits poorly the codebases where tests are thin, because the evidence then proves little. A green test run on an untested module is a confident answer to the wrong question.

## Evolutionary search: trust the evaluator

[Google DeepMind's AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/), published on May 14, 2025, is the outlier. It pairs Gemini Flash for breadth with Gemini Pro for depth, scores every candidate program with automated evaluators, and evolves the best ones. DeepMind reports it found a scheduling heuristic that recovers on average 0.7% of Google's worldwide compute, and a kernel speedup that cut Gemini's training time by 1%.

The design only works where a solution can be scored automatically, and that is the lesson for enterprises. Most business software lacks a precise fitness function, so evolutionary search is not a general coding assistant. Where you do have one (query cost, batch run time, scoring latency, cloud spend) it deserves serious attention, because the machine can explore far more options than a team ever could.

## Then the editor became a fleet manager

By December the question had shifted from which agent to how many. [VS Code's November 2025 release](https://code.visualstudio.com/updates/v1_107), version 1.107, makes the hierarchy explicit. A local agent keeps running in the background and is a natural place to plan the work. From there a task can be handed off to a background agent, which can run in its own Git worktree so several can work without clobbering each other's files, or to a cloud agent that executes it autonomously. In my own use the local agent acts as the manager and the others as workers, and shared repository instructions keep them from inventing the project structure.

Worktrees solve file conflicts. They do not solve semantic conflicts. Two agents can each produce a clean, passing change that is wrong in combination: one renames a field while another adds a new consumer of the old name. The merge step, and the person who owns it, becomes the real integration point. Fleets move the bottleneck from writing code to merging it.

This changes the job of the engineer in the editor. Instead of writing a feature, they break it into tasks that agents can do in parallel without stepping on each other, then review and integrate the results. That is closer to a tech lead's work than a developer's, and most teams have not been trained for it. In my experience the engineers who thrive here are the ones who were already good at writing clear tickets.

> Automation is doing things right. Orchestration is doing the right things.

## One change, three agents

A worked example makes the trade-offs concrete. Say a shared logging library has a flaw, and forty services need to move to a patched version that also changes one method signature. Every large estate has a backlog of chores like this.

A platform-embedded agent treats it as forty issues and forty draft pull requests, each passing through the branch protection and reviewers that service already has. The governance is familiar, and the cost lands on reviewers: forty approvals, many for near-identical diffs. A sandboxed agent runs the forty upgrades in parallel and returns each with its test log. Where a service has real coverage around logging, that evidence is worth more than a reviewer's skim. Where it has none, the green result tells you the code compiles and little else. Evolutionary search has nothing to offer here, because there is no score to improve, only a migration that is right or wrong.

In practice the answer mixes them. Let the sandboxed agent do the work and attach evidence, route the result through existing review, and spend human attention on the few services where tests are thin. The choice was made per service, by looking at its verification, rather than once for the whole firm by looking at a vendor slide.

## What enterprises should take from this

- **Do not standardize on one agent.** The architectures are converging but not identical, and the best tool varies by task. A multi-vendor setup behind one governed gateway keeps options open as the market shifts.
- **Choose by verification path.** Use platform-embedded agents where your review controls are strong, sandboxed agents where your tests are strong, and evolutionary search only where you can score outcomes automatically.
- **Govern the harness, not the vendor.** Context, guardrails, sandboxing, identity and evidence capture are what make any agent safe. Own those layers so that switching vendors is a configuration change.
- **Give every agent its own identity.** Each agent action should be attributable to a non-human identity with scoped permissions, so the audit trail shows what the agent did and which person asked it to.
- **Design for asynchronous work.** Background and cloud agents change how teams plan and review. Maker/checker controls, merge ownership and audit trails have to move with them.

[Anthropic's guidance on building agents](https://www.anthropic.com/research/building-effective-agents) is a useful brake on all of this: start with the simplest solution that works, and add autonomy only when it pays for itself. It also notes that code suits agents well because solutions can be verified through automated tests. I read that as a condition, not a compliment. Agents are safest exactly where your verification is strongest, so the order of investment is tests and controls first, autonomy second.

**What to do on Monday morning:**

- Rate your twenty most active repositories on test coverage and review discipline, then map each to the agent architecture it can safely supervise.
- Issue a scoped non-human identity to each coding agent in your pilot and confirm its actions appear in audit logs.
- Run one multi-service backlog chore through a sandboxed agent, routing its evidence into your existing pull request review.
- Name a **merge owner** for every team running parallel background agents.

The firms that get this right will treat coding agents as a governed workforce with clear supervisors rather than as a smarter autocomplete. Which of your codebases have the test coverage and review discipline to supervise a fleet of agents today?

**Bottom line:** Stop waiting, start delegating, and build the factory rather than the widget. Pick agents by how you will verify them, and own the harness that makes any of them safe.
