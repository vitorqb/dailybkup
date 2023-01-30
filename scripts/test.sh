#!/bin/bash
USAGE="$0"' [-h] [-p] [-g PATTERN] [-f] [-u] [-o] -- [FILES]

Runs tests. If not FILE is given, run all tests otherwise only tests from file.

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

  -n)
    Do NOT run tests that require optional dependencies. If not given, reads the
    value of DAILYBKUP_DEV_OPTIONAL_DEPS (1 or 0)
'

# Defaults
if [ -z "$DAILYBKUP_DEV_OPTIONAL_DEPS" ] || [ "$DAILYBKUP_DEV_OPTIONAL_DEPS" == 1 ]
then
    SKIP_OPTIONAL_DEPS=0
else
    SKIP_OPTIONAL_DEPS=1
fi

# Getopts
while getopts "hpg:fun:" opt; do
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
    n)
        SKIP_OPTIONAL_DEPS=1
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

FILES="${@:$OPTIND}"

# Find root directory
GIT_ROOT="$(git rev-parse --show-toplevel)"

# Set's config file for tests
echo "Setting DAILYBKUP_CONFIG_FILE=${GIT_ROOT}/testdata/config.yaml"
export DAILYBKUP_CONFIG_FILE=${GIT_ROOT}/testdata/config.yaml

# Loads env vars for test
echo "Soucing ${GIT_ROOT}/.env.test"
if [ -f ${GIT_ROOT}/.env.test ]
then
    source ${GIT_ROOT}/.env.test
fi

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

if [ "$SKIP_OPTIONAL_DEPS" == 1 ]
then
    ARGS+=( -m "not gdrive" )
fi

ARGS+=( ${FILES[@]} )
echo ${ARGS[@]}
"${ARGS[@]}"
