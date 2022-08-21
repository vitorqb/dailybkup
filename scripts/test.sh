#!/bin/bash
USAGE="$0"' [-h] [-p] [-g PATTERN]

Runs tests.

  -h)
    Displays this help message.

  -g PATTERN)
    Grep tests by name/blob pattern.

  -p)
    Show print statements.

'

# Getopts
while getopts "hpg:" opt; do
  case "$opt" in
    h)
        echo "$USAGE"
        exit 0
        ;;
    p)
        SHOW_PRINT=1
        ;;
    g)
        GREP="$OPTARG"
        ;;
    --)
        break
        ;;
    *)
        echo "ERROR: UNKNOWN ARGUMENT: $1" >&2
        exit 1
        ;;
  esac
done

# Find root directory
GIT_ROOT="$(git rev-parse --show-toplevel)"

# Set's config file for tests
export DAILYBKUP_CONFIG_FILE=${GIT_ROOT}/testdata/config.yaml

# Loads env vars for test
source ${GIT_ROOT}/.env.test

# Constructs command and run
ARGS=( poetry run pytest )
if [ "$SHOW_PRINT" = "1" ]
then
    ARGS+=( -s )
fi
if ! [ -z "$GREP" ]
then
    ARGS+=( -k "$GREP" )
fi
${ARGS[@]}
