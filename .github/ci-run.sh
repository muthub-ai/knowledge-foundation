#!/usr/bin/env bash
# Run a CI step and, if it fails, repeat the last 80 lines of its output as a GitHub error annotation, so the failure
# can be read from the Checks API (annotations) as well as the job log.
#   bash .github/ci-run.sh "<label>" <command> [args...]
label="$1"; shift
log="$(mktemp)"
set -o pipefail
"$@" 2>&1 | tee "$log"
rc=${PIPESTATUS[0]}
if [ "$rc" -ne 0 ]; then
  tail -n 80 "$log" | sed -e 's/%/%25/g' -e 's/\r/%0D/g' | awk 'BEGIN{ORS="%0A"} {print}' > "$log.enc"
  echo "::error title=${label} failed (exit ${rc})::$(cat "$log.enc")"
fi
exit "$rc"
