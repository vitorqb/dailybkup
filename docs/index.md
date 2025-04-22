# DailyBkup

A tool for backing up your files daily.


## Configuration

Backups rely on a yaml configuration file that defines what and how to
run a backup.

The program looks for a configuration file in a path specified by the
environmental variable `DAILYBKUP_CONFIG_FILE`. If not set, it
defaults to `~/.config/dailybkup.yaml`.

A custom configuration file can be set by using the `-c` flag, which
will take precendence over the environmental variable
`DAILYBKUP_CONFIG_FILE`.

```sh
python -m dailybkup -c CONFIG_FILE backup
```

### Options

#### Compression

Defines what and how to compress.

```yaml
compression:
    files:  # Required
        - /files/1
        - /files/2
    exclude:  # Required
        - /files/3
    tar_executable: "mytar"  # Defaults to "tar"
    tar_flags: ["--dereference", "-z"]  # Defaults to ["--dereference", "--checkpoint=1000", "-v", "-z"]
```

### Using Google Drive as storage

Follow the steps
[here](https://www.labnol.org/google-api-service-account-220404) to
create a Service Account with the proper rights for a shared folder on
your Google Drive.

Now make sure that, when running the upload command, the environmental
variable `GOOGLE_APPLICATION_CREDENTIALS` is set to the absolute path
to the service account json file. This takes care of authentication.

Then add a configuration section:

```yaml
storage:
    - type_: google_drive
      folder_id: "1-AaKa-AKOSjoajasaAO129SuQwybqLqb"
      suffix: .tar.gpg
```



## Running

Running a backup as as simple as:

```
python -m dailybkup  backup
```


## Scheduling

One of the easiest tools to run your backups daily is using
[systemd](https://en.wikipedia.org/wiki/Systemd) timers.

### Systemd

Here we will schedule a backup to run with the following criteria:


Create both files below:

```
# file:~/.config/systemd/user/dailybkup.timer
[Unit]
Description=Timer for Daily Backup

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=default.target
```

```
# file:~/.config/systemd/user/dailybkup.service
[Unit]
Description=Daily Backup
# Max 3 runs per hour
StartLimitInterval=3600
StartLimitBurst=3

[Service]
EnvironmentFile=%h/.config/dailybkup/env
ExecStart=/usr/bin/python -m dailybkup -c %h/.config/dailybkup/config.yaml backup
Restart=on-failure
# Restart after 2min
RestartSec=120
```

!!! info
    - We are configuring a backup that will:
        - Run once per day
        - Restart up to 3 times per hour on failure
        - Restart after 120s
    - You may also save those in other places - see [Where do I put my
    systemd unit
    files](https://unix.stackexchange.com/questions/224992/where-do-i-put-my-systemd-unit-file)
    - If you are configuring multiple backups, give each file a unique name.
    - Make sure `/usr/bin/python` is valid for your system, or update it accordingly.


Now, set your `config.yaml` file and an `env` file on the paths
specified above. For example:

```
# file:~/.config/dailybkup/config.yaml
storage:
  - type_: b2
    bucket: dailybkup-personal
    suffix: .tar
compression:
  files: [~/Downloads]
  exclude: []
notification:
  - type_: desktop
    sender_config:
      type_: "notify-send"
```

```
# file:~/.config/dailybkup/env
DAILYBKUP_B2_APPLICATION_KEY_ID=mykeyid
DAILYBKUP_B2_APPLICATION_KEY=mykey
```

Now use `systemctl` to enable the service

```sh
systemctl --user daemon-reload
systemctl --user enable dailybkup.timer
systemctl --user start dailybkup.timer
```

!!! warning
    Since there are sensitive data on the `env` file, you may want to give it
    restrictive permissions: `chmod 0600 ~/.dailybkup/env`

If you don't want to wait and want to give it a try, you can start the backup
immediately using

```sh
systemctl --user start dailybkup
```

You can check when the timer will activate by doing

```sh
systemctl --user status dailybkup.timer
```


## Releases

### 1.0.0

**Breaking Changes**

The configuration for `file` storage has changed:

*Before*  
```yaml
storage:
  - type_: file
    path: /home/user/backup.tar.gpg
```

*Now*  
```yaml
storage:
  - type_: file
    directory: /home/user/bkups
    suffix: .tar.gpg
```

The old behavior expected `path` to be the path to a file where the
entire backup would be saved.

The new behavior expects `directory` to be an existing directory. A
backup file will be created on this directory. The file name will
contain the date of the creation of the file, in the
`YYYY-MM-DDTHH:MM:SS` format. If `suffix` is given, it's appended to
the file name.

In the above example, we would end up with a file like
`/home/user/bkups/2022-12-25T23:28:39.tar.gpg`.
