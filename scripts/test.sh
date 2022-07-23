#!/bin/bash
USAGE="$0"' [-h]

Runs tests.

  -h)
    Displays this help message.

  -p)
    Show print statements.

'

# Getopts
while getopts "hp" opt; do
  case "$opt" in
    h)
        echo "$USAGE"
        exit 0
        ;;
    p)
        SHOW_PRINT=1
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
export DAILYBKUP_CONFIG_FILE=${GIT_ROOT}/testdata/config.yaml
ARGS=( poetry run pytest )
if [ "$SHOW_PRINT" = "1" ]
then
    ARGS+=( -s )
fi
${ARGS[@]}
