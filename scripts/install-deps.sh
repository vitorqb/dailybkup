#!/bin/bash
#!/bin/bash
USAGE="$0"' [-h] [-o]

Install dependencies.

  -h)
    Displays this help message.

  -s)
    Skip optional dependencies. If not given, respects the value from
    DAILYBKUP_DEV_OPTIONAL_DEPS (1 or 0)
'

# Imports
source ${TOOLS_FILE:-./scripts/_tools.sh}

# Defaults
if [ -z "$DAILYBKUP_DEV_OPTIONAL_DEPS" ] || [ "$DAILYBKUP_DEV_OPTIONAL_DEPS" == 1 ]
then
    OPTIONAL_DEPENDENCIES=1
else
    OPTIONAL_DEPENDENCIES=0
fi


# Getopts
while getopts "hs" opt; do
  case "$opt" in
    h)
        echo "$USAGE"
        exit 0
        ;;
    s)
        OPTIONAL_DEPENDENCIES=0
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

ARGS=( poetry install )

if [ "$OPTIONAL_DEPENDENCIES" == 1 ]
then
    ARGS+=( --all-extras )
fi

msg "Running: ${ARGS[@]}"

"${ARGS[@]}"
