#!/bin/bash

set -euo pipefail

DAYS=90
SILENT=false

START_DATE=""
END_DATE=""
SINGLE_DAY=""

while [[ $# -gt 0 ]]; do
case "$1" in
--days)
DAYS="$2"
shift 2
;;
--day)
SINGLE_DAY="$2"
shift 2
;;
--start)
START_DATE="$2"
shift 2
;;
--end)
END_DATE="$2"
shift 2
;;
-s|--silent)
SILENT=true
shift
;;
*)
echo "Unknown argument: $1"
exit 1
;;
esac
done

ARGS=()

if [[ -n "$SINGLE_DAY" ]]; then
ARGS+=(--day "$SINGLE_DAY")
elif [[ -n "$START_DATE" && -n "$END_DATE" ]]; then
ARGS+=(--start "$START_DATE")
ARGS+=(--end "$END_DATE")
else
ARGS+=(--days "$DAYS")
fi

python3 -m build.dashboard "${ARGS[@]}"

if ! $SILENT; then
xdg-open build/dashboard.html >/dev/null 2>&1 &
fi
