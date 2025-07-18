Automatically turns off the VPS once the bandwidth limit is reached.

### Steps to install:

1) SSH into your Hetzner VPS
2) Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
3) `cd` into the repository & `uv sync` to install the dependencies
4) Get the `HETZNER_API_KEY` and `HETZNER_SERVER_ID` from Hetzner console
    - [`Docs for API Key`](https://docs.hetzner.cloud/reference/cloud#getting-started)
    - Server ID is the part of the URL here:
        `https://console.hetzner.com/projects/PROJECT_ID/servers/SERVER_ID/overview`
5) Install the cronjob using `crontab -e`
6) Add the following line:
```
*/30 * * * * cd /path/to/hetzner-bandwidth-script && /root/.local/bin/uv run main.py >> cron.log 2>&1
```

This runs the script every 30 minutes, based on the VPS's system timezone.

To find the full path to `uv`, use:
```
which uv
```

The shutdown threshold is set to 19TB by default, but you can adjust it in the script.

Log output is written to `cron.log` inside the repository directory.
