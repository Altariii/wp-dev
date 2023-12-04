import json
import os

from ..commands.exit import bye
from ..constants.config import WP_DEV_CONFIG_NAME
from ..utils import console
from ..utils import lando

# PRE_START_COMMANDS
# POST_START_COMMANDS
# PRE_MAKE_COMMANDS
# POST_MAKE_COMMANDS
# CONSTANTS
# IS_BEDROCK
# THEMES_DIRECTORY
# PLUGINS_DIRECTORY
# AUTO_UPDATE
# THEMES
# PLUGINS

def start_with_recipe(project_path: str) -> None:
    recipe = None
    recipe_path = os.path.join(project_path, WP_DEV_CONFIG_NAME)
    console.display.info("Reading recipe file...")
    with open(recipe_path) as recipe_file:
        recipe = json.load(recipe_file)
    console.display.success("Recipe file loaded")

    print("")
    if "pre_start_commands" not in recipe or len(recipe["pre_start_commands"]) == 0:
        console.display.info("No pre-start commands defined. Skipping...")
    else:
        console.display.info("Running pre-start commands...")
        execute_commands(recipe["pre_start_commands"], project_path)

    print("")
    if "auto_update" in recipe and recipe["auto_update"]:
        if "themes_directory" not in recipe or not recipe["themes_directory"]:
            console.display.info("No themes directory defined. Skipping theme updates...")
        else:
            console.display.info("Updating themes...")
            update_themes(recipe['themes_directory'], project_path)

        print("")
        if "plugins_directory" not in recipe or not recipe["plugins_directory"]:
            console.display.info("No plugins directory defined. Skipping plugin updates...")
        else:
            console.display.info("Updating plugins...")
            update_plugins(recipe['plugins_directory'], project_path)

    print("")
    console.display.info("Starting lando...")
    lando.start(project_path)
    console.display.success("Lando started successfully")

    print("")
    if "post_start_commands" not in recipe or len(recipe["post_start_commands"]) == 0:
        console.display.info("No post-start commands defined. Skipping...")
    else:
        console.display.info("Running post-start commands...")
        execute_commands(recipe["post_start_commands"], project_path)
    
def execute_commands(commands: list[str], project_path: str) -> None:
    pre_start_commands_exception = False
    try:
        for command in commands:
            console.display.statement("Running command:" + console.colors.CYAN + ' ' + command + console.colors.ENDC)
            console.run_command(command, project_path)
    except Exception as e:
        pre_start_commands_exception = str(e)
    if not pre_start_commands_exception:
        console.display.success("Commands executed successfully")
    else:
        console.display.error("Errors have been produced during commands execution:", pre_start_commands_exception)
        confirm = console.display.request("Are you sure you want to continue? (y/n)")
        if confirm.lower() == 'n':
            bye()

def update_themes(themes_dir: str, project_path: str) -> None:
    themes_directory = os.path.join(project_path, themes_dir)
    if not os.path.exists(themes_directory):
        console.display.error("The themes directory: " + themes_directory + " could not be found. Please, make sure it exists.")
    else:
        themes = os.listdir(themes_directory)
        for theme in themes:
            theme_folder = os.path.join(themes_directory, theme)
            if os.path.exists(os.path.join(theme_folder, '.git')):
                console.display.statement("Updating " + theme + '...')
                try:
                    console.run_commands(["git pull", "yarn", "yarn build", "lando composer update"], theme_folder, show_output=False)
                except Exception as e:
                    console.display.warning("Theme", theme, "could not be updated. Please, update manually.")

def update_plugins(plugins_dir: str, project_path: str) -> None:
    plugins_directory = os.path.join(project_path, plugins_dir)
    if not os.path.exists(plugins_directory):
        console.display.error("The plugins directory: " + plugins_directory + " could not be found. Please, make sure it exists.")
    else:
        plugins = os.listdir(plugins_directory)
        for plugin in plugins:
            plugin_folder = os.path.join(plugins_directory, plugin)
            if os.path.exists(os.path.join(plugin_folder, '.git')):
                console.display.statement("Updating " + plugin + '...')
                try:
                    console.run_commands(["git pull", "yarn", "yarn build", "lando composer update"], plugin_folder, show_output=False)
                except Exception as e:
                    console.display.warning("Plugin", plugin, "could not be updated. Please, update manually.")