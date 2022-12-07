# DailyBkup

A tool for backing up your files daily.

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
StartLimitInterval=200
StartLimitBurst=5

[Service]
EnvironmentFile=%h/.dailybkup/env
ExecStart=/usr/bin/python -m dailybkup -c %h/.dailybkup/config.yaml backup
Restart=on-failure
RestartSec=30
```

!!! info
    - We are configuring a backup that will:
        - Run once per day
        - Restart up to 5 times on failure
        - Restart after 30s
    - You may also save those in other places - see [Where do I put my
    systemd unit
    files](https://unix.stackexchange.com/questions/224992/where-do-i-put-my-systemd-unit-file)
    - If you are configuring multiple backups, give each file a unique name.
    - Make sure `/usr/bin/python` is valid for your system, or update it accordingly.


Now, set your `config.yaml` file and an `env` file on the paths
specified above. For example:

```
# file:~/.dailybkup/config.yaml
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
# file:~/.dailybkup/env
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
