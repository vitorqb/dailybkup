#!/bin/bash
USAGE="$0"' [-h] -v VERSION

Creates a release.

  -h)
    Displays this help message.

  -v VERSION)
    The version to be release (format x.y.z)
'

# Getopts
while getopts "hv:" opt; do
  case "$opt" in
    h)
        echo "$USAGE"
        exit 0
        ;;
    v)
        VERSION="$OPTARG"
        ;;
    *)
        echo "ERROR: UNKNOWN ARGUMENT: $1" >&2
        exit 1
        ;;
  esac
done

# Script
if [ -z "$VERSION" ]
then
    echo "Missing VERSION" >&2
    exit 1
fi

poetry run mike deploy --push --update-aliases $VERSION latest
poetry run mike set-default --push latest
