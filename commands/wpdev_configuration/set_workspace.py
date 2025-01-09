import os

from ...config.config import workspaces, get_config, save_new_config
from ...utils import console

def set_new_workspace() -> None:
    console.display.clear()
    console.display.banner()
    console.display.description("WP-DEV Workspace Adder")
    print("")

    current_workspaces = workspaces()
    if not current_workspaces:
        console.display.info("No previous workspaces have been found")
    else:
        console.display.info("Current Workspaces:")
        print("")
        for workspace in current_workspaces:
            console.display.statement(workspace)
        print("")
        
    config = get_config()
    validated_workspace = False
    new_workspace = ''
    while not validated_workspace:
        new_workspace = console.display.request("Add your workspace directory absolute path")
        if not os.path.exists(new_workspace):
            console.display.warning("The given workspace directory has not been found")
            confirm = console.display.request("Are you sure this is the correct path? You can try again with a different path. (y/n)")
            if confirm.lower() == 'y':
                validated_workspace = True
        elif new_workspace in config['workspaces']:
            console.display.info("Given workspace is already saved.")
            return
        else:
            validated_workspace = True

    config['workspaces'].append(new_workspace)
    save_new_config(config)
    console.display.success("New Workspace set successfully")

class SetWorkspaceCommand:
    parent_page = "WP-DEV Configuration"
    submenu_page = False
    key = "1"
    description = "Add a WP-DEV Workspace"
    handler = set_new_workspace