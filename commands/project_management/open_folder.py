import os, functools

from ...config.config import workspaces
from ...utils import console
from ...utils import lando

def open_folder() -> None:
    console.display.clear()
    console.display.banner()
    console.display.description("WP-DEV Project Folder Opener")
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

        project_path = None
        for workspace in current_workspaces:
            if os.path.isdir(os.path.join(workspace, project_folder_name)):
                project_path = os.path.join(workspace, project_folder_name)
                continue

    if project_path:
        console.run_command('xdg-open .', project_path)
        console.display.success('Project folder opened successfully')
    else:
        console.display.error('Project folder could not be opened')

class OpenFolderCommand:
    parent_page = "Project Management"
    submenu_page = False
    key = '3'
    description = 'Opens the folder of an existing Lando Project'
    handler = open_folder