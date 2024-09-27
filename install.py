#! ./venv/bin/python

import logging
import os
import shutil
import subprocess
import sys

from dotenv import load_dotenv

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

URL = os.environ.get("URL")
TOKEN = os.environ.get("TOKEN")

if URL.endswith('.git'):
    URL = URL.rstrip('.git')

if URL is None or TOKEN is None:
    logging.error("URL or TOKEN is not set. Please set these environment variables.")
    logging.error(f"URL NOT SET: {URL}") if URL is None else logging.info(f"URL: {URL}")
    logging.error(f"TOKEN NOT SET: {TOKEN}") if TOKEN is None else logging.info(f"TOKEN: {TOKEN}")
    logging.error("Set URL=<your-github-url>")
    logging.error("Set TOKEN=<your-repo-token")
    logging.error("This information can be found in you repository under settings => Runners => New Self Hosted Runner => Select Linux")
    logging.error("Your token can be found under configure at this url: <your-github-url-here>/settings/actions/runners/new?arch=x64&os=linux")
    sys.exit(1)

# Check if directory exists and remove it
if os.path.exists("actions-runner"):
    shutil.rmtree("actions-runner")

logging.info("Creating Directories")
subprocess.run(["mkdir", "actions-runner"], check=True)
os.chdir("actions-runner")  # Use os.chdir

logging.info("Downloading runner tar file...")
subprocess.run(["curl", "-o", "actions-runner-linux-x64-2.319.1.tar.gz", "-L", "https://github.com/actions/runner/releases/download/v2.319.1/actions-runner-linux-x64-2.319.1.tar.gz"], check=True)

logging.info("Validating sha...")
subprocess.run(["echo", "3f6efb7488a183e291fc2c62876e14c9ee732864173734facc85a1bfb1744464  actions-runner-linux-x64-2.319.1.tar.gz", "|", "shasum", "-a", "256", "-c"], check=True)

logging.info("Untarring data...")
subprocess.run(["tar", "-xzf", "./actions-runner-linux-x64-2.319.1.tar.gz"], check=True)

logging.info("Configuring repository")

logging.info("Following information can be found in you repository under settings => Runners => New Self Hosted Runner => Select Linux")
logging.info(f"Your URL is: {URL}")
logging.info(f"Your TOKEN is: {TOKEN}")


try:
    subprocess.run(["./config.sh", "--url", URL, "--token", TOKEN], check=True)
except Exception:
    logging.error("URL or Token invalid. Confirm URL and TOKEN values are correct. Gathering another token may be necessary...")
    logging.error(f"Your URL is: {URL}")
    logging.error(f"Your TOKEN is: {TOKEN}")
    sys.exit(1)

subprocess.run(["npm", "ci"], check=True)
