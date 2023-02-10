#!/bin/bash
USAGE="$0"' [-h] [-p PORT] [-n NAME] [-d]

Uses docker to run wiremock, used for tests.
If a docker container is already running w/ the same name, skip.

  -h)
    Displays this help message.

  -p PORT)
    The port in which to run it. Defaults to 9000.

  -n NAME)
    A name to give the container. Defaults to ${PROJECT}_wiremock or
    wiremock if not set.

  -d)
    Daemonize.
'

# Imports
source ${TOOLS_FILE:-./scripts/_tools.sh}

# Defaults
PORT=9000
VERSION=2.35.0
IMAGE=wiremock/wiremock
if [ -z $PROJECT ]
then
    NAME=wiremock
else
    NAME=${PROJECT}_wiremock
fi


# Getopts
while getopts "hp:dn:" opt; do
  case "$opt" in
    h)
        echo "$USAGE"
        exit 0
        ;;
    d)
        DAEMON=1
        ;;
    p)
        PORT="$OPTARG"
        ;;
    n)
        NAME="$OPTARG"
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

# Helpers
_is_running() {
    ID=$(docker ps -q --filter "name=^${NAME}\$")
    if [ -z $ID ]
    then
        return 1
    fi
    return 0
}

# Script
if _is_running
then
    msg "Wiremock already running!"
    exit 0
fi
CMD=( docker run -i -t --rm --name $NAME -p "$PORT:8080" )
if [ "$DAEMON" = 1 ]
then
    CMD+=( -d )
fi
CMD+=( "$IMAGE:$VERSION" )
"${CMD[@]}"
