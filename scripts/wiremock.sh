#!/bin/bash
USAGE="$0"' [-h] [-p PORT]

Uses docker to run wiremock, used for tests.

  -h)
    Displays this help message.

  -p)
    The port in which to run it.
'

# Defaults
PORT=9000
VERSION=2.35.0
IMAGE=wiremock/wiremock

# Getopts
while getopts "hp:" opt; do
  case "$opt" in
    h)
        echo "$USAGE"
        exit 0
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
docker run \
       -it \
       --rm \
       -p $PORT:8080 \
       $IMAGE:$VERSION
