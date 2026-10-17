# ADR 013: A local classifier decides; the Claude API writes

Status: accepted, October 17, 2026

## Context

Muthu chose this on Oct 17, 2026: decisions stay on his Mac at no cost per call; writing quality comes from Claude.

## Decision

LLM-Wiki-V2 uses a custom System One classifier on Ollama (tev1, 8k context) and a custom LLM provider pointing at Anthropic's OpenAI-compatible endpoint. The curator (Claude Code) and Semantica's LLM method use the Anthropic API.

## Consequences

Ingest runs on the Mac; the CI ingest workflow is a classic-mode fallback. Thresholds start from the Laya preset and are calibrated in Phase 0.
