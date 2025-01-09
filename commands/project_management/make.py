import webbrowser

from ...utils import console
from ...utils import environment
from ...utils.parsing import create_slug

from ...config import config
from ...constants.environment import *

def make() -> None:
    console.display.clear()
    console.display.banner()
    console.display.description("WP-DEV Project Maker")
    print("")

    # SELECT A PROJECT NAME
    project_name = ""
    project_name_confirmed = False
    while not project_name_confirmed:
        project_name = console.display.request("Input the new project name")
        project_slug = create_slug(project_name)
        confirm = console.display.request("Your project name is now configured to " + project_name + " (" + project_slug + "). Is that correct? (y/n)")
        if confirm == 'y':
            project_name_confirmed = True
    console.display.info("Project name selected: " + project_name + " (" + project_slug + ")")
    
    # SELECT A PROJECT WORKSPACE
    print("")
    selected_workspace = 0
    workspace_confirmed = False
    workspaces = config.workspaces()
    console.display.info("Available Workspaces:")
    for index, workspace in enumerate(workspaces):
        print("[" + str(index) + "] " + workspace)
    while not workspace_confirmed:
        selected_workspace = int(console.display.request("Select a valid workspace (0 default)", '0'))
        if selected_workspace < 0 or selected_workspace >= len(workspace):
            console.display.error("Invalid workspace selected. Please select a valid index.")
            continue
        workspace_confirmed = True
    console.display.info("Workspace selected: " + workspaces[selected_workspace])

    # SET UP THE ADMIN ACCOUNT
    print("")
    username = console.display.request("Input the project admin username (" + DEFAULT_ADMIN_USERNAME + " default)", DEFAULT_ADMIN_USERNAME)
    password = console.display.request("Input the project admin password (" + DEFAULT_ADMIN_PASSWORD + " default)", DEFAULT_ADMIN_PASSWORD)
    email = console.display.request("Input the project admin email (" + DEFAULT_ADMIN_EMAIL + " default)", DEFAULT_ADMIN_EMAIL)
    console.display.info("Admin credentials set")

    # SET UP EXTRA CONFIG
    print("")
    setup_extra_config = console.display.request("Do you want to continue with the advanced settings? (y/n)", 'n')
    
    print("")
    if setup_extra_config == 'n':
        environment.create(project_name, project_slug, workspaces[selected_workspace], username, password, email)
    else:
        php_version = console.display.request("Which PHP Version do you want to use? (" + DEFAULT_PHP_VERSION + " default)", DEFAULT_PHP_VERSION)
        wp_version = console.display.request("Which WordPress Version do you want to use? (" + DEFAULT_WP_VERSION + " default)", DEFAULT_WP_VERSION)
        using_bedrock = console.display.request("Do you want to use Bedrock? (y/n) (" + ('y' if DEFAULT_BEDROCK else 'n') + " default)", 'y' if DEFAULT_BEDROCK else 'n')
        wp_lang = console.display.request("Which WordPress language do you want to use? (" + DEFAULT_WP_LANG + " default)", DEFAULT_WP_LANG)
        wp_debug = console.display.request("Would you like to activate debugging? (y/n) (" + ('y' if DEFAULT_DEBUG else 'n') + " default)", 'y' if DEFAULT_DEBUG else 'n')

        print("")
        environment.create(project_name, project_slug, workspaces[selected_workspace], username, password, email, php_version, wp_version, using_bedrock.lower() == 'y', wp_lang, wp_debug.lower() == 'y')

    console.display.info(f"Project set up successfully on https://{project_slug}.lndo.site")
    open_site = console.display.request("Do you want to open the site? (y/n)", 'n')

    if open_site == 'y':
        webbrowser.open(f"https://{project_slug}.lndo.site")

class MakeCommand:
    parent_page = "Project Management"
    submenu_page = False
    key = '4'
    description = 'Sets up a new WP-DEV project'
    handler = make