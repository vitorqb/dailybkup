#!/bin/bash
USAGE="$0"' [-h] [-p] [-g PATTERN] [-f] [-u]

Runs tests.

  -h)
    Displays this help message.

  -g PATTERN)
    Grep tests by name/blob pattern.

  -p)
    Show print statements.

  -f)
    Run functional tests only

  -u)
    Run unit tests only

'

# Getopts
while getopts "hpg:fu" opt; do
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
    f)
        FUNCTIONAL=1
        ;;
    u)
        UNIT=1
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
echo "Setting DAILYBKUP_CONFIG_FILE=${GIT_ROOT}/testdata/config.yaml"
export DAILYBKUP_CONFIG_FILE=${GIT_ROOT}/testdata/config.yaml

# Loads env vars for test
echo "Soucing ${GIT_ROOT}/.env.test"
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
if ! [ -z "$UNIT" ]
then
    ARGS+=( -c "${GIT_ROOT}/pytest.unit.ini" )
fi
if ! [ -z "$FUNCTIONAL" ]
then
    ARGS+=( -c "${GIT_ROOT}/pytest.functional.ini" )
fi
echo ${ARGS[@]}
${ARGS[@]}
