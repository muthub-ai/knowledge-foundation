#!/usr/bin/env bash
# Run a CI step and, if it fails, repeat the last 120 lines of its output as GitHub error annotations, so the failure
# can be read from the Checks API (annotations) as well as the job log. GitHub cuts an annotation at about 4 KB, so the
# tail is split into numbered parts of at most 3,500 bytes (colour codes removed); the last part holds the summary.
#   bash .github/ci-run.sh "<label>" <command> [args...]
label="$1"; shift
log="$(mktemp)"
set -o pipefail
"$@" 2>&1 | tee "$log"
rc=${PIPESTATUS[0]}
if [ "$rc" -ne 0 ]; then
  tail -n 120 "$log" | sed -e 's/\x1b\[[0-9;]*[A-Za-z]//g' -e 's/\r//g' > "$log.tail"
  split -C 3500 -d "$log.tail" "$log.part."
  n=$(ls "$log".part.* | wc -l); i=0
  for p in "$log".part.*; do
    i=$((i + 1))
    msg=$(sed -e 's/%/%25/g' "$p" | awk 'BEGIN{ORS="%0A"} {print}')
    echo "::error title=${label} failed (exit ${rc}), part ${i} of ${n}::${msg}"
  done
fi
exit "$rc"
