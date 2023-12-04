import os
import webbrowser

from ..constants.config import LANDO_CONFIG_NAME
from ..utils import console
from ..utils import lando

def fast_show_database() -> None:
    console.display.clear()
    console.display.banner()
    console.display.description("WP-DEV Project Lando Database")
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
    
    lando_info = lando.info(project_path)
    if not lando_info:
        console.display.error("Lando info could not be obtained.")
        return
    
    database_url = ""
    for service in lando_info:
        if service['service'] != 'pma':
            continue

        database_url = service['urls'][-1]
        break
    
    confirm = console.display.request("Do you want to open it on browser? (y/n)")
    if confirm.lower() == 'y':
        webbrowser.open(database_url)
        pass
    else:
        console.display.info("Your current project PMA URL is: " + database_url)

class FastShowDatabaseCommand:
    parent_page = "Fast Lando Toolkit"
    submenu_page = False
    key = '7'
    description = 'Shows the Lando Project PMA'
    handler = fast_show_database