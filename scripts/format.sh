#!/bin/bash
USAGE="$0"' [-h]

Runs formatting for the project.

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
        shift
        ;;
    *)
        echo "ERROR: UNKNOWN ARGUMENT: $1" >&2
        exit 1
        ;;
  esac
done

# Script
poetry run black .
