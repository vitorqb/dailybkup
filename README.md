# DailyBackup

## User Documentation

https://vitorqb.github.io/dailybkup/latest

## Phases

A backup consist of the following phases:

1. Compression
2. Encryption
3. Storage
4. Cleanup
5. Notification

## Development

### Running Tests

For running the functional tests, you need to have a b2 account with a
configured API key. **A bucket must exist with name `daiybkup-test`**.

**All files on the `daiybkup-test` bucket will be deleted with the tests!**

Then, create a file `.env.test` with the following, substituting the elipsis:
```sh
export DAILYBKUP_B2_APPLICATION_KEY_ID="..."
export DAILYBKUP_B2_APPLICATION_KEY="..."
```

For functional tests, you will need to start wiremock

```
$ ./scripts/wiremock.sh -h
./scripts/wiremock.sh [-h] [-p PORT]

Uses docker to run wiremock, used for tests.

  -h)
    Displays this help message.

  -p PORT)
    The port in which to run it. Defaults to 9000.
```

Running the tests:
```
$ ./scripts/test.sh -h
./scripts/test.sh [-h] [-p] [-g PATTERN] [-f] [-u]

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
```


### Developer Tools

Some scripts are inside the `devtools` folder, and may help you with
the app development to test some stuff.

The `gdrive_client.py` is a helper that allows you to test functionality of
`gdrive_utils.GDriveClient`.

It requires a Google Service Account JSON file for the login. See
[Using Google Drive as storage](./docs/index.md#login) to see how to
generate the file.

Example usage:

```sh
poetry run ./devtools/gdrive_client.py --service-account-json-file=sa.json delete --file-id 999xxxx9-xxxxxxxxxxxxxxxxx-xxxxxx
poetry run ./devtools/gdrive_client.py --service-account-json-file=sa.json list --parent-id=9-xxxx-xxxxxxxxxxxxxxxxxxxxxxxxxx
poetry run ./devtools/gdrive_client.py --service-account-json-file=sa.json upload --parent-id '9-xxxx-xxxxxxxxxxxxxxxxxxxxxxxxxx' ./foo
```
