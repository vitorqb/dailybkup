#!/bin/bash
USAGE="$0"' [-h] [-c]

Runs formatting for the project.

  -h)
    Displays this help message.

  -c)
    If given, only check the files and return an exit code.
'

# Getopts
while getopts "hc" opt; do
  case "$opt" in
    h)
        echo "$USAGE"
        exit 0
        ;;
    --)
        ;;
    c)
        CHECK=1
        ;;
    *)
        echo "ERROR: UNKNOWN ARGUMENT: $1" >&2
        exit 1
        ;;
  esac
done

# Script
ARGS=()
if [ "$CHECK" = "1" ]
then
    ARGS+=( "--check" )
fi
poetry run black ${ARGS[@]} .
