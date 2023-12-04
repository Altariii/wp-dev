import os

from ..config.config import workspace
from ..config.recipe_handler import start_with_recipe
from ..constants.config import WP_DEV_CONFIG_NAME, LANDO_CONFIG_NAME
from ..utils import console
from ..utils import lando

def start() -> None:
    console.display.clear()
    console.display.banner()
    console.display.description("WP-DEV Project Starter")
    print("")
    
    current_workspace = workspace()
    project_path = None
    if not current_workspace:
        console.display.warning("No workspace directory has been found in the config.json file")
        console.display.info("Current directory will be used instead")
        confirm = console.display.request("Are you sure you want to continue? (y/n)")
        if confirm.lower() == 'n':
            console.display.warning("Project start aborted")
            return
        
        project_path = os.getcwd()
    else:
        available_projects = os.listdir(current_workspace)
        if len(available_projects) == 0:
            console.display.warning("No projects found in the current workspace")
        else:
            console.display.info("Available projects in workspace:")
        
        running_services = lando.get_running_services()
        for project in available_projects:
            if os.path.isdir(os.path.join(current_workspace, project)):
                if lando.is_running(project, running_services):
                    console.display.success(project)
                else:
                    console.display.statement(project)

        print("")
        project_folder_name = console.display.request("Which project would you like to start?")
        if project_folder_name not in available_projects:
            console.display.warning("The project " + project_folder_name + " has not been found in the workspace")
            confirm = console.display.request("Are you sure you want to continue? (y/n)")
            if confirm.lower() == 'n':
                console.display.warning("Project start aborted")
                return

        project_path = os.path.join(current_workspace, project_folder_name)

    project_config_file_path = os.path.join(project_path, WP_DEV_CONFIG_NAME)
    has_recipe = True
    if not os.path.isfile(project_config_file_path):
        has_recipe = False
        console.display.warning("No WP-DEV config file has been found. Lando will start normally")

    lando_config_file_path = os.path.join(project_path, LANDO_CONFIG_NAME)
    if not os.path.isfile(lando_config_file_path):
        console.display.error("No .lando.yml file has been found for this project. Please, make sure it exists")
        return
    
    if has_recipe:
        start_with_recipe(project_path)
    else:
        console.display.info("Starting lando...")
        lando.start(project_path)
        console.display.success("Lando started successfully")

class StartCommand:
    parent_page = "Project Management"
    submenu_page = False
    key = '2'
    description = 'Starts a Lando Project'
    handler = start
