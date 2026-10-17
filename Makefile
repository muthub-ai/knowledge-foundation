# Everyday commands, run on the Mac from the repository root. Models come from .env (see .env.example).
PY := PYTHONPATH=tools python3
include $(wildcard .env)
export

.PHONY: ingest curate check test graph stale evals ask

ingest:            ## file every capture in inbox/ (local classifier decides, Claude writes)
	@git rev-parse --abbrev-ref HEAD | grep -qv '^main$$' || { echo "Switch to a branch first: git switch -c ingest/$$(date +%Y%m%d)"; exit 1; }
	$(PY) tools/librarian/ingest.py $$(ls inbox/*.md 2>/dev/null | grep -v README)
	$(PY) -m kb normalize

curate:            ## hand the branch to the curator (Claude Code) to finish and open the pull request
	claude "Read AGENTS.md and follow skills/curate.md for this branch."

check:             ## everything CI checks on a pull request
	$(PY) -m kb check
	python3 -m llmw2 --bundle wiki check

test:              ## unit tests
	PYTHONPATH=tools:tests:$$PYTHONPATH python3 -m unittest discover -s tests

graph:             ## build the graph into dist/
	$(PY) -m kb graph --out dist

stale:
	$(PY) -m kb stale

evals:             ## live right-note rate (asks the models)
	$(PY) -m kb evals --live

ask:               ## make ask Q="What is a curated overlay?"
	llmwiki2 --bundle wiki ask "$(Q)"
