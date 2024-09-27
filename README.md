## Easy Github Runner configuration for IT EC Machines

### Requirements

To install a new github runner you need to export two environment variables URL and TOKEN.

URL is the url of the github repository. TOKEN should be accessible using the below information.

- This information can be found in you repository by navigating to your runner directory: settings => Runners => New Self Hosted Runner => Select Linux
- You can also reach the same location under: <your-github-url-here>/settings/actions/runners/new?arch=x64&os=linux

Look for token under "Configure" section.

BASH:

```bash
    export URL='<GITHUB URL>'
    export TOKEN='<TOKEN>'
```

TCSH:

```tcsh
    setenv URL '<GITHUB URL>'
    setenv TOKEN '<TOKEN>'
```

To install a new github runner run `make install` on a SLES15 IT EC machine. Once installed it can be run interactively with `make run`.

To daemonize the runner with process monitoring you can run the following:

- `make daemon`
- To check the status of the runner run `make status`
- To check the logs of the runner run `make logs`
- To stop the daemon/runner run `make stop`

To clean the repository and start from scratch run `make clean`
