#!/bin/bash
USAGE="$0"' [-h]

Serves the documentation website locally.

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
        ;;
    *)
        echo "ERROR: UNKNOWN ARGUMENT: $1" >&2
        exit 1
        ;;
  esac
done

# Script
poetry run mkdocs serve
