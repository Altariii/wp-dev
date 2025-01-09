import os, functools

from ...config.config import workspaces
from ...config.recipe_handler import has_recipe, load_recipe, execute_commands
from ...constants.config import LANDO_CONFIG_NAME
from ...utils import updater
from ...utils import console
from ...utils import lando

def start_with_recipe(project_path: str) -> None:
    recipe = load_recipe(project_path)

    print("")
    if 'auto_update' in recipe and recipe['auto_update']:
        update_git = False
        if 'update_git' in recipe:
            update_git = recipe['update_git']

        console.display.info("Updating plugins and themes")
        if 'plugins' in recipe and len(recipe['plugins']) > 0:
            for plugin in recipe['plugins']:
                updater.update_project_dependency(project_path, plugin, update_git)
        else:
            console.display.info("No plugins have been found in the recipe")

        if 'themes' in recipe and len(recipe['themes']) > 0:
            for theme in recipe['themes']:
                updater.update_project_dependency(project_path, theme, update_git)
        else:
            console.display.info("No themes have been found in the recipe")

    print("")
    if 'start_commands' not in recipe or len(recipe['start_commands']) == 0:
        console.display.info("No start commands defined. Skipping...")
    else:
        console.display.info("Running start commands")
        execute_commands(recipe['start_commands'], project_path)

    print("")
    console.display.info("Starting lando...")
    lando.start(project_path)
    console.display.success("Lando started successfully")

def start() -> None:
    console.display.clear()
    console.display.banner()
    console.display.description("WP-DEV Project Starter")
    print("")
    
    current_workspaces = workspaces()
    project_path = None
    if not current_workspaces:
        console.display.warning("No workspace directories have been found in the config.json file")
        console.display.info("Current directory will be used instead")
        confirm = console.display.request("Are you sure you want to continue? (y/n)")
        if confirm.lower() == 'n':
            console.display.warning("Project start aborted")
            return
        
        project_path = os.getcwd()
    else:
        available_projects = functools.reduce(lambda a, b: a + b, [os.listdir(workspace) for workspace in current_workspaces])
        if len(available_projects) == 0:
            console.display.warning("No projects found in the current workspaces")
        else:
            console.display.info("Available projects in workspaces:")
        
        running_services = lando.get_running_services()
        for project in available_projects:
            if any([os.path.isdir(os.path.join(workspace, project)) for workspace in current_workspaces]):
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

        for workspace in current_workspaces:
            if os.path.isdir(os.path.join(workspace, project_folder_name)):
                project_path = os.path.join(workspace, project_folder_name)
                continue

    if not has_recipe(project_path):
        console.display.warning("No WP-DEV config file has been found. Lando will start normally")

    lando_config_file_path = os.path.join(project_path, LANDO_CONFIG_NAME)
    if not os.path.isfile(lando_config_file_path):
        console.display.error("No .lando.yml file has been found for this project. Please, make sure it exists")
        return
    
    if has_recipe(project_path):
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
