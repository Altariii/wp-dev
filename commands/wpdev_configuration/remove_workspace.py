from ...config import config
from ...utils import console

def remove_workspace() -> None:
    console.display.clear()
    console.display.banner()
    console.display.description("WP-DEV Workspace Remover")
    print("")

    workspaces = config.workspaces()
    if not workspaces:
        console.display.error("No previous workspaces have been found. Aborting.")
        return
    
    console.display.info("Current Workspaces:")
    print("")
    for index, workspace in enumerate(workspaces):
        print('[' + str(index) + '] ' + workspace)
    print("")

    workspace_to_delete = int(console.display.request("Select the number of the workspace to delete"))
    if workspace_to_delete < 0 or len(workspaces) <= workspace_to_delete:
        console.display.error("Invalid Workspace Number. Please, select a number from 0 and " + str(len(workspaces)))
        return
    
    confirm = console.display.request("Are you sure you want to remove this workspace? " + workspaces[workspace_to_delete] + ' (y/n)')
    if confirm.lower() == 'n':
        console.display.info("Workspace removal aborted")
        return
    
    del workspaces[workspace_to_delete]
    new_config = config.get_config()
    new_config["workspaces"] = workspaces
    config.save_new_config(new_config)

    console.display.success("Workspace removed successfully")
    return

class RemoveWorkspaceCommand:
    parent_page = "WP-DEV Configuration"
    submenu_page = False
    key = "2"
    description = "Remove a WP-DEV Workspace"
    handler = remove_workspace