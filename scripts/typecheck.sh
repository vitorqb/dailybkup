#!/bin/bash
USAGE="$0"' [-h]

Runs type checking for the project.

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
GIT_ROOT="$(git rev-parse --show-toplevel)"
poetry run mypy $GIT_ROOT/dailybkup/
