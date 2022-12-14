#!/bin/bash
USAGE="$0"' [-h] [-p PORT]

Uses docker to run wiremock, used for tests.

  -h)
    Displays this help message.

  -p PORT)
    The port in which to run it. Defaults to 9000.

  -d)
    Daemonize.
'

# Defaults
PORT=9000
VERSION=2.35.0
IMAGE=wiremock/wiremock

# Getopts
while getopts "hp:d" opt; do
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
    --)
        break
        ;;
    *)
        echo "ERROR: UNKNOWN ARGUMENT: $1" >&2
        exit 1
        ;;
  esac
done

# Script
CMD=( docker run -i -t --rm -p "$PORT:8080" )
if [ "$DAEMON" = 1 ]
then
    CMD+=( -d )
fi
CMD+=( "$IMAGE:$VERSION" )
"${CMD[@]}"
