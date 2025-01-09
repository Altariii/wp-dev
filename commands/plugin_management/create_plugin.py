import os, functools

from ...utils import console
from ...utils import lando
from ...utils.wordpress import get_wp_content_path
from ...utils import parsing

from ...constants.config import DEFAULT_PLUGIN_BOILERPLATE, WP_PLUGINS_FOLDER, DEFAULT_COMPOSER_NAME_PREFIX
from ...constants.updater import NPM_FILE, COMPOSER_FILE

from ...config.config import workspaces

def create_plugin() -> None:
    console.display.clear()
    console.display.banner()
    console.display.description("WP-DEV Plugin Creator")
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

    # CREATE PLUGIN
    plugin_name = ""
    plugin_name_confirmed = False
    while not plugin_name_confirmed:
        plugin_name = console.display.request("Input the new plugin name")
        PLUGIN_SLUG = parsing.create_slug(plugin_name)
        confirm = console.display.request("Your plugin name is now configured to " + plugin_name + " (" + PLUGIN_SLUG + "). Is that correct? (y/n)")
        if confirm == 'y':
            plugin_name_confirmed = True
    console.display.info("Plugin name selected: " + plugin_name + " (" + PLUGIN_SLUG + ")")

    console.display.info("Creating plugin...")
    WP_CONTENT_PATH = get_wp_content_path(project_path)
    PLUGINS_PATH = os.path.join(WP_CONTENT_PATH, WP_PLUGINS_FOLDER)
    NEW_PLUGIN_PATH = os.path.join(PLUGINS_PATH, PLUGIN_SLUG)
    
    lando.composer.create_project(DEFAULT_PLUGIN_BOILERPLATE, PLUGIN_SLUG, PLUGINS_PATH)

    # Remove illegal characters && fix Plubo json files
    parsing.fix_json_file(os.path.join(NEW_PLUGIN_PATH, NPM_FILE), modify_func=lambda data: data.update(name=PLUGIN_SLUG))
    parsing.fix_json_file(os.path.join(NEW_PLUGIN_PATH, COMPOSER_FILE), modify_func=lambda data: data.update(name=f'{DEFAULT_COMPOSER_NAME_PREFIX}/{PLUGIN_SLUG}', autoload={
        "psr-4": {
            f"{parsing.pascal_case(plugin_name)}\\": ""
        },
        "files": [
            "Utils/plubo.php"
        ]
    }))

    lando.composer.update(NEW_PLUGIN_PATH)
    console.run_command('yarn', NEW_PLUGIN_PATH)
    lando.wp.activate_plugin(PLUGIN_SLUG, project_path)

    console.display.success("New plugin created successfully")

    # TODO: Add option to modify plugin readme, like npm init does

    # TODO: GitLab Integration
        # git init
        # call the glab API to choose the desired project group (or make a new one)
        # create the new project through the glab API
        # git remote add origin git@gitlab.com:Customers/Test.git
        # git add .
        # git commit -m 'Initial commit'
        # git push -u origin main 

    # TODO: Modify the gitlab utils to list & select groups

class CreatePluginCommand:
    parent_page = 'Plugin Management'
    submenu_page = False
    key = '1'
    description = 'Creates a new plugin using the Plubo boilerplate'
    handler = create_plugin