#!/bin/bash
USAGE="$0"' [-h]
Publishes to codeartifact in aws.
  -h)
    Prints this help msg.
'

function usage() {
    echo "$USAGE"
    exit 1
}

while getopts "hv:" o; do
    case "${o}" in
        h)
            usage
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

# The repository to where we publish
export AWS_REGION="us-east-2"
export DOMAIN="default"
export REPOSITORY="default"
export POETRY_PUBLISH_URL=$(aws codeartifact get-repository-endpoint --domain "$DOMAIN" --repository "$REPOSITORY" --format pypi --query 'repositoryEndpoint' --output text)

# Check we actually fetch the url
if [ -z "$POETRY_PUBLISH_URL" ]
then
    echo "ERROR: Failed to query repository url"
    usage
fi
echo "Url: $POETRY_PUBLISH_URL"

# The username and password used to authenticate
export POETRY_PUBLISH_USERNAME=aws
export POETRY_PASSWORD=$(aws codeartifact get-authorization-token --domain "$DOMAIN" --query 'authorizationToken' --output text)

# This env var configures a repo called "default" in poetry
export POETRY_REPOSITORIES_DEFAULT_URL="$POETRY_PUBLISH_URL"

# The commands to publish
poetry publish -r default -u "$POETRY_PUBLISH_USERNAME" -p "$POETRY_PASSWORD"
