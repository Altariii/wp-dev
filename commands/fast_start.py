import os

from ..constants.config import LANDO_CONFIG_NAME
from ..utils import console
from ..utils import lando

def fast_start() -> None:
    console.display.clear()
    console.display.banner()
    console.display.description("WP-DEV Project Fast Starter")
    print("")

    project_path = os.getcwd()

    lando_config_file_path = os.path.join(project_path, LANDO_CONFIG_NAME)
    if not os.path.isfile(lando_config_file_path):
        console.display.error("No .lando.yml file has been found for this project. Please, make sure it exists")
        return
    
    console.display.info("Starting lando...")
    lando.start(project_path)
    console.display.success("Lando started successfully")

class FastStartCommand:
    parent_page = "Fast Lando Toolkit"
    submenu_page = False
    key = '1'
    description = 'Starts the Lando Project in the current directory (with no recipe)'
    handler = fast_start
