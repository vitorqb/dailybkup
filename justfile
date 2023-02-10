export TOOLS_FILE := justfile_directory() / "scripts" / "_tools.sh"
export PROJECT := "dailybkup"

run *ARGS:
    ./scripts/run.sh {{ARGS}}

test *ARGS:
    just test-unit {{ARGS}}
    just test-functional {{ARGS}}

test-functional *ARGS:
    ./scripts/wiremock.sh -d
    ./scripts/test.sh -f {{ARGS}}

test-unit *ARGS:
    ./scripts/test.sh -u {{ARGS}}

docs-release *ARGS:
    ./scripts/docs-release.sh {{ARGS}}

docs-serve *ARGS:
    ./scripts/docs-serve.sh {{ARGS}}

format *ARGS:
    ./scripts/format.sh {{ARGS}}

wiremock *ARGS:
    ./scripts/wiremock.sh {{ARGS}}

release *ARGS:
    ./scripts/release.sh {{ARGS}}

install-deps *ARGS:
    ./scripts/install-deps.sh
