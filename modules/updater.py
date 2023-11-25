import json
import os
import subprocess
import sys

from ..utils import connection, console
from ..config.config import version
from ..constants import config
from ..constants import connection as connection_constants
from ..commands.exit import bye

def check_last_version() -> [bool, str, str]:
    [response_code, source_code, _, _] = connection.get_source(config.GITHUB_CONFIG_URL)
    if response_code != connection_constants.OK_RESPONSE:
        console.display.error("Could not get the latest version, Error: " + source_code)
        bye()
    GITHUB_CONFIG = json.loads(source_code)
    
    CURRENT_VERSION = version()
    console.display.info("WP-DEV Version: " + CURRENT_VERSION)
    console.display.success("Latest Version: " + GITHUB_CONFIG['version'])

    if CURRENT_VERSION == GITHUB_CONFIG['version']:
        return [True, CURRENT_VERSION, GITHUB_CONFIG['version']]

    return [False, CURRENT_VERSION, GITHUB_CONFIG['version']]

def attempt_update(current_version: str, latest_version: str) -> None:
    print("")
    console.display.download_info("Downloading Update...")
    success = False
    try:
        LOCK_FILE = os.path.join(config.WP_DEV_PATH, '/.git/index.lock')
        if os.path.isfile(LOCK_FILE):
            console.display.statement("Removing index.lock file from .git directory")
            os.remove(LOCK_FILE)

        subprocess.run(f"cd wp-dev/ && git checkout . && git pull {config.GITHUB_URL} HEAD && cd ..", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if version() == latest_version:
            success = True
            
    except:
        console.display.error("Automatic Update Failed! Please, download manually from: " + console.colors.ENDC + config.GITHUB_URL)
    
    if success == True:
        console.display.result("WP-DEV Updated To Latest Version!", "")
    else:
        console.display.warning("WP-DEV Update not successful. Download manually from: " + console.colors.ENDC + config.GITHUB_URL)