import os, functools

from ...utils import console
from ...utils import lando
from ...utils import docker
from ...utils import updater
from ...config.config import workspaces

def destroy() -> None:
    console.display.clear()
    console.display.banner()
    console.display.description("WP-DEV Project Destroyer")
    print("")

    # SELECT A PROJECT
    current_workspaces = workspaces()
    project_path = None
    if not current_workspaces:
        console.display.warning("No workspace directories have been found in the config.json file")
        console.display.info("Current directory will be used instead")
        confirm = console.display.request("Are you sure you want to continue? (y/n)")
        if confirm.lower() == 'n':
            console.display.warning("Project destruction aborted")
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
        project_folder_name = console.display.request("Which project would you like to destroy?")
        if project_folder_name not in available_projects:
            console.display.warning("The project " + project_folder_name + " has not been found in the workspace")
            confirm = console.display.request("Are you sure you want to continue? (y/n)")
            if confirm.lower() == 'n':
                console.display.warning("Project destruction aborted")
                return

        for workspace in current_workspaces:
            if os.path.isdir(os.path.join(workspace, project_folder_name)):
                project_path = os.path.join(workspace, project_folder_name)
                continue

    project_dependencies = updater.discover_project_dependencies(project_path)
    if len(project_dependencies) > 0:
        console.display.warning(console.colors.BOLD + ' ' + str(len(project_dependencies)) + console.colors.ENDC + ' dependencies have been found on this project:\n' + ', '.join(project_dependencies))
        confirm = console.display.request(console.colors.BOLD + console.colors.YELLOW + f'Are you sure you want to destroy {project_folder_name}? (y/n)' + console.colors.ENDC)
        if confirm.lower() != 'y':
            console.display.warning("Project destruction aborted")
            return
    
    project_name = console.display.request('Write the project name')
    if (project_name != project_folder_name):
        console.display.warning("Project destruction aborted")
        return
    
    lando.destroy(project_path)

    console.display.success(f"Project {project_name} has been destroyed")
    
    # print("")
    # docker.remove_project(project_name)
    # console.display.success("Docker project removed successfully")

    print("")
    confirm = console.display.request(f"Do you want to remove the project folder from your workspace? (y/n)")
    if confirm.lower() == 'y':
        console.run_command(f'rm -rf {project_folder_name}', path=workspace, shell=True)
        console.display.success("Project folder removed successfully")

class DestroyCommand:
    parent_page = 'Project Management'
    submenu_page = False
    key = '6'
    description = 'Destroys an existing WP-DEV project'
    handler = destroy