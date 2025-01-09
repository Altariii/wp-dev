import os, functools

from ...utils import console
from ...utils import lando
from ...utils import updater
from ...config.recipe_handler import has_recipe
from ...config.config import workspaces

def update() -> None:
    console.display.clear()
    console.display.banner()
    console.display.description("WP-DEV Project Updater")
    print("")

    # SELECT A PROJECT
    current_workspaces = workspaces()
    project_path = None
    if not current_workspaces:
        console.display.warning("No workspace directories have been found in the config.json file")
        console.display.info("Current directory will be used instead")
        confirm = console.display.request("Are you sure you want to continue? (y/n)")
        if confirm.lower() == 'n':
            console.display.warning("Project update aborted")
            return
        
        project_path = os.getcwd()
        project_folder_name = project_path
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
        project_folder_name = console.display.request("Which project would you like to update?")
        if project_folder_name not in available_projects:
            console.display.warning("The project " + project_folder_name + " has not been found in the workspace")
            confirm = console.display.request("Are you sure you want to continue? (y/n)")
            if confirm.lower() == 'n':
                console.display.warning("Project update aborted")
                return

        for workspace in current_workspaces:
            if os.path.isdir(os.path.join(workspace, project_folder_name)):
                project_path = os.path.join(workspace, project_folder_name)
                continue

    # UPDATE PROJECT
    if has_recipe(project_path):
        updater.update_project_from_recipe(project_path)
    else:
        console.display.warning("No WP-DEV config file has been found. Dependencies to update will be auto-detected")
        updater.update_project_from_auto_detect(project_path)
        
    console.display.success(f"{project_folder_name} updated successfully")

class UpdateCommand:
    parent_page = "Project Management"
    submenu_page = False
    key = '5'
    description = 'Updates an existing WP-DEV project'
    handler = update