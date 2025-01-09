import json
import os

from ..commands.exit import bye
from ..constants.config import WP_DEV_CONFIG_NAME
from ..utils import console

def has_recipe(project_path: str) -> bool:
    project_config_file_path = os.path.join(project_path, WP_DEV_CONFIG_NAME)
    if not os.path.isfile(project_config_file_path):
        return False
    return True

def load_recipe(project_path: str, verbose: bool = True) -> dict | bool:
    recipe = False
    recipe_path = os.path.join(project_path, WP_DEV_CONFIG_NAME)
    if verbose:
        console.display.info("Reading recipe file...")
    with open(recipe_path) as recipe_file:
        recipe = json.load(recipe_file)
    if verbose:
        console.display.success("Recipe file loaded") if recipe else console.display.error("The recipe could not be loaded")
    return recipe
    
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