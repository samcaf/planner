#!/bin/bash

set -euo pipefail

VERBOSE=true
ARG=""

# -------------------------
# Parse args
# -------------------------
while [[ $# -gt 0 ]]; do
    case "$1" in
        -s|--silent)
            VERBOSE=false
            shift
            ;;
        *)
            ARG="$1"
            shift
            ;;
    esac
done

# -------------------------
# Resolve date via Python (single source of truth)
# -------------------------
TARGET_DATE=$(python3 - <<EOF
from lib.date_utils import resolve_date
import sys

arg = "${ARG:-today}"
print(resolve_date(arg))
EOF
)

YEAR=$(date -d "$TARGET_DATE" +%Y)
MONTH=$(date -d "$TARGET_DATE" +%m)
DAY=$(date -d "$TARGET_DATE" +%d)

DIR="data/$YEAR/$MONTH"
FILE="$DIR/$YEAR-$MONTH-$DAY.pln"

mkdir -p "$DIR"

# -------------------------
# Prevent overwrite
# -------------------------
if [[ -f "$FILE" ]]; then
    echo "Already exists: $FILE"
    if $VERBOSE; then
        vim "$FILE"
    fi
    exit 0
fi

# -------------------------
# Build from templates
# -------------------------
WEEKDAY=$(date -d "$TARGET_DATE" +%a | tr '[:upper:]' '[:lower:]')

MORNING="data/templates/morning.pln"
TEMPLATE="data/templates/${WEEKDAY}.pln"
EVENING="data/templates/evening.pln"

touch "$FILE"

[[ -f "$MORNING" ]] && cat "$MORNING" >> "$FILE"
[[ -f "$TEMPLATE" ]] && cat "$TEMPLATE" >> "$FILE"
[[ -f "$EVENING" ]] && cat "$EVENING" >> "$FILE"


if $VERBOSE; then
    echo "Created $FILE"
    vim "$FILE"
fi
