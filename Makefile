.DEFAULT_GOAL:=help
.PHONY: build run install token

SHELL := /bin/bash
NPX := /usr/intel/pkgs/nodejs/19.0.0/bin/npx

export http_proxy=http://proxy-dmz.intel.com:911
export https_proxy=http://proxy-dmz.intel.com:912
export no_proxy=127.0.0.1,localhost,.intel.com

dir_to_add := /usr/intel/pkgs/nodejs/19.0.0/bin/
export PATH := $(dir_to_add):$(PATH)

print-path:
	@echo $(PATH)

activate: 				## Activate Python Environment
	@source ./venv/bin/activate

install: 				## Install a new runner for a respository
	@echo "creating virtual environment..."
	@/usr/intel/pkgs/python3/3.10.8/bin/python3 -m venv venv
	@echo "activating environment..."
	@source ./venv/bin/activate
	@echo "updating pip..."
	@./venv/bin/pip install --upgrade pip
	@source ./venv/bin/activate
	@echo "installing requirements..."
	@./venv/bin/pip install -r requirements.txt
	@echo "installing github runner.."
	@./install.py
	@echo "Runner Installed Successfully, run 'make run' in order to run the runner interactively. You can also run 'make daemon' to run the runner with a daemon manager"

clean: 				## Clean up all the runners and remove them
	make stop
	rm -rf ./actions-runner
	rm -rf runner_stderr.log runner_stdout.log
	rm -rf node_modules 

run:				## Run the runner interactively like normal
	./actions-runner/run.sh

daemon:				## Run the runner with a supervisord daemon manager to monitor process
	${NPX} pm2 start ./actions-runner/run.sh --interpreter bash --output ./runner_stdout.log --error ./runner_sterr.log

status: 			## check the status of the runner
	${NPX} pm2 status

logs: 			## check the logs of the runner
	${NPX} pm2 logs

errlogs: 		## check only the error logs of the runner
	${NPX} pm2 logs --err

outlogs: 		## check only the stdout logs of the runner
	${NPX} pm2 logs --out

stop:				## Stop the runner
	${NPX} pm2 stop ./actions-runner/run.sh

help:						## Show this help.
	@echo "Github Runner Installation Scripts"
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m (default: help)\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
