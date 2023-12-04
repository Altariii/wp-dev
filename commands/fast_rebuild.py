import os

from ..constants.config import LANDO_CONFIG_NAME
from ..utils import console
from ..utils import lando

def fast_rebuild() -> None:
    console.display.clear()
    console.display.banner()
    console.display.description("WP-DEV Project Fast Re-builder")
    print("")

    project_path = lando.get_running_service_path()
    if project_path:
        console.display.info("Found running project: " + project_path)
    else:
        console.display.warning("No running lando project found. Trying with current directory")
        project_path = os.getcwd()

    lando_config_file_path = os.path.join(project_path, LANDO_CONFIG_NAME)
    if not os.path.isfile(lando_config_file_path):
        console.display.error("No .lando.yml file has been found for this project. Please, make sure it exists")
        return
    
    console.display.info("Rebuilding lando...")
    lando.rebuild(project_path)
    console.display.success("Lando rebuilt successfully")

class FastRebuildCommand:
    parent_page = "Fast Lando Toolkit"
    submenu_page = False
    key = '3'
    description = 'Rebuilds the current Lando Project'
    handler = fast_rebuild
