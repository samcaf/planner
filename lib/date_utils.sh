#!/usr/bin/env bash

resolve_date() {
    local arg="${1:-}"

    if [[ -z "$arg" ]]; then
        date +%F
        return
    fi

    if [[ "$arg" =~ ^[+-][0-9]+$ ]]; then
        date -d "$arg days" +%F
        return
    fi

    if [[ "$arg" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        echo "$arg"
        return
    fi

    if [[ "$arg" == "tomorrow" ]]; then
        date -d "tomorrow" +%F
        return
    fi

    if [[ "$arg" == "yesterday" ]]; then
        date -d "yesterday" +%F
        return
    fi

    echo "Invalid date argument: $arg" >&2
    return 1
}
