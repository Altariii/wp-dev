import os

from ....utils import console
from ....utils import lando

def fast_open_folder() -> None:
    console.display.clear()
    console.display.banner()
    console.display.description("WP-DEV Project Folder")
    print("")

    project_path = lando.get_running_service_path()
    if project_path:
        console.display.info("Found running project: " + project_path)
    else:
        console.display.warning("No running lando project found. Opening current directory")
        project_path = os.getcwd()

    console.run_command('xdg-open .', project_path)
    console.display.success('Project folder opened successfully')

class FastOpenFolderCommand:
    parent_page = "Fast Lando Toolkit"
    submenu_page = False
    key = '9'
    description = 'Opens the current project folder'
    handler = fast_open_folder