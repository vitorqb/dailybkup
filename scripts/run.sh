#!/bin/bash
USAGE="$0"' [-h]

Runs the app.

  -h)
    Displays this help message.

'

# Getopts
while getopts "h" opt; do
  case "$opt" in
    h)
        echo "$USAGE"
        exit 0
        ;;
    --)
        # Leave the args for the wrapped command
        break
        ;;
    *)
        echo "ERROR: UNKNOWN ARGUMENT: $1" >&2
        exit 1
        ;;
  esac
done

ARGS="${@:$OPTIND}"

# Script
poetry run python -m dailybkup "${ARGS[@]}"
