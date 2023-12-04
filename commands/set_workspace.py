import os

from ..config.config import workspace, get_config, save_new_config
from ..utils import console

def set_new_workspace() -> None:
    print("")
    current_workspace = workspace()
    if not current_workspace:
        console.display.info("No previous workspace has been found")
    else:
        console.display.warning(f"A previous workspace has been found: {current_workspace}")
        confirm = console.display.request("Are you sure you want to replace the existing workspace? (y/n)")
        if confirm.lower() != 'y':
            console.display.warning("Workspace update aborted")
            return
        
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
        else:
            validated_workspace = True

    config['workspace_path'] = new_workspace
    save_new_config(config)
    console.display.success("New Workspace set successfully")

class SetWorkspaceCommand:
    parent_page = "WP-DEV Configuration"
    submenu_page = False
    key = "1"
    description = "Set or Update the WP-DEV Workspace"
    handler = set_new_workspace