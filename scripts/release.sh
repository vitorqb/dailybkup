#!/bin/bash
USAGE="$0"' [-h] -v VERSION

Creates a release.

  -h)
    Displays this help message.

  -v VERSION)
    The version to be release (format x.y.z)
'

source ${TOOLS_FILE:-./scripts/_tools.sh}

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

# Helpers
function uncommit_files_exist() {
    git update-index --refresh
    ! git diff-index --quiet HEAD --
}

# Script
if [ -z "$VERSION" ]
then
    echo "Missing VERSION" >&2
    exit 1
fi

if uncommit_files_exist
then
    echo "Uncommited files exist: do something about it!" >&2
    exit 1
fi

msg "Writting to dailybkup/version.py"
cat >dailybkup/version.py <<EOF
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# THIS FILE IS AUTOMATICALLY GENERATED - DO NOT MODIFY IT!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
VERSION = "$VERSION"
EOF

msg "Setting version in poetry..."
poetry version "$VERSION" || exit 1

msg "Creating release commit..."
git add . && git commit -m "Version $VERSION" && git push  || exit 1

msg "Building..."
poetry build  || exit 1

msg "Creating github release..."
gh release create v$VERSION --generate-notes ./dist/dailybkup-$VERSION-py3-none-any.whl ./dist/dailybkup-$VERSION.tar.gz  || exit 1

msg "Releasing docs..."
./scripts/docs-release.sh -v"$VERSION"  || exit 1

msg "Publishing to AWS..."
./scripts/_publish-to-aws.sh || exit 1
