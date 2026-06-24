#!/bin/bash

set -euo pipefail

FORCE=false
ARG=""

# -------------------------
# Parse args
# -------------------------
while [[ $# -gt 0 ]]; do
    case "$1" in
        -f|--force)
            FORCE=true
            shift
            ;;
        *)
            ARG="$1"
            shift
            ;;
    esac
done

# -------------------------
# Resolve date via Python
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

if $FORCE; then
    rm -f "$FILE";
else
    read -p "Delete '${FILE}'? [y/N] " YN && [ "${YN}" = 'y' ] && rm "${FILE}";
fi
