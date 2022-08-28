# DailyBackup

## Phases

A backup consist of the following phases:

1. Compression
2. Encryption
3. Storage
4. Cleanup
5. Notification

## Development

For running the functional tests, you need to have a b2 account with a
configured API key. **A bucket must exist with name `daiybkup-test`**.

**All files on the `daiybkup-test` bucket will be deleted with the tests!**

Then, create a file `.env.test` with the following, substituting the elipsis:
```sh
export DAILYBKUP_B2_APPLICATION_KEY_ID="..."
export DAILYBKUP_B2_APPLICATION_KEY="..."
```

Running tests:
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
