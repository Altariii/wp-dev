import os

from ..constants.updater import *
from ..constants.config import WP_THEMES_FOLDER, WP_PLUGINS_FOLDER
from ..utils.wordpress import is_plugin, is_theme, get_wp_content_path
from ..config.recipe_handler import has_recipe, load_recipe
from ..utils import console
from ..utils import lando

def discover_project_dependencies(project_path: str) -> list[str]:
    WP_CONTENT_PATH = get_wp_content_path(project_path)
    THEMES_FOLDER = os.path.join(WP_CONTENT_PATH, WP_THEMES_FOLDER)
    PLUGINS_FOLDER = os.path.join(WP_CONTENT_PATH, WP_PLUGINS_FOLDER)
    dependencies = []

    # Discover themes
    if os.path.isdir(THEMES_FOLDER):
        path_list = os.listdir(THEMES_FOLDER)
        for theme in path_list:
            SUBDIRECTORY = os.path.join(THEMES_FOLDER, theme)
            if os.path.isdir(SUBDIRECTORY) and get_folder_directory(GIT_FOLDER, SUBDIRECTORY):
                dependencies.append(theme)

    if os.path.isdir(PLUGINS_FOLDER):
        path_list = os.listdir(PLUGINS_FOLDER)
        for plugin in path_list:
            SUBDIRECTORY = os.path.join(PLUGINS_FOLDER, plugin)
            if os.path.isdir(SUBDIRECTORY) and get_folder_directory(GIT_FOLDER, SUBDIRECTORY):
                dependencies.append(plugin)

    return dependencies

def update_project_from_recipe(project_path: str) -> None:
    if not has_recipe(project_path): return

    recipe = load_recipe(project_path)
    update_git = recipe['update_git']
    
    for plugin in recipe['plugins']:
        update_project_dependency(project_path, plugin, update_git)
    
    for theme in recipe['themes']:
        update_project_dependency(project_path, theme, update_git)

def update_project_from_auto_detect(project_path: str) -> None:
    dependencies = discover_project_dependencies(project_path)

    for dependency in dependencies:
        update_project_dependency(project_path, dependency, True)

def update_project_dependency(project_path: str, dependency_slug: str, update_git: bool) -> bool:
    DEPENDENCY_PATH = is_theme(project_path, dependency_slug) or is_plugin(project_path, dependency_slug)
    # TODO: Handle case where is_theme && is_plugin (now only theme will be updated)
    if not DEPENDENCY_PATH:
        return False
    
    COMPOSER_DIR_PATHS = get_file_directories(COMPOSER_FILE, DEPENDENCY_PATH)
    for COMPOSER_DIR_PATH in COMPOSER_DIR_PATHS:
        console.display.info("Updating " + dependency_slug + " composer dependencies...")
        lando.composer.update(COMPOSER_DIR_PATH)
    
    YARN_LOCK_DIR_PATHS = get_file_directories(YARN_FILE, DEPENDENCY_PATH)
    NPM_PACKAGE_DIR_PATHS = get_file_directories(NPM_FILE, DEPENDENCY_PATH)
    for YARN_LOCK_DIR_PATH in YARN_LOCK_DIR_PATHS:
        console.display.info("Updating " + dependency_slug + " node dependencies...")
        console.run_commands(['yarn', 'yarn build'], YARN_LOCK_DIR_PATH)

    for NPM_PACKAGE_DIR_PATH in NPM_PACKAGE_DIR_PATHS:
        console.display.info("Updating " + dependency_slug + " node dependencies...")
        console.run_command('npm run build', NPM_PACKAGE_DIR_PATH)

    if update_git:
        GIT_DIRECTORY_PATH = get_folder_directory(GIT_FOLDER, DEPENDENCY_PATH)
        if GIT_DIRECTORY_PATH:
            console.display.info("Pulling last changes from Git")
            console.run_command('git pull', GIT_DIRECTORY_PATH)

    console.display.info(dependency_slug + " updated")
    return True

def get_file_directories(file_name: str, path: str) -> list[str]:
    directories = []
    file_path = os.path.join(path, file_name)
    if os.path.isfile(file_path):
        directories.append(path)
    
    path_list = os.listdir(path)
    for subpath in path_list:
        SUBDIRECTORY = os.path.join(path, subpath)
        if os.path.isdir(SUBDIRECTORY) and subpath not in EXCLUDE_FOLDERS:
            directories += get_file_directories(file_name, SUBDIRECTORY)
    
    return directories

def get_folder_directory(folder_name: str, path: str) -> str:
    folder_path = os.path.join(path, folder_name)
    if os.path.isdir(folder_path):
        return path
    
    path_list = os.listdir(path)
    for subpath in path_list:
        SUBDIRECTORY = os.path.join(path, subpath)
        if os.path.isdir(SUBDIRECTORY) and subpath not in EXCLUDE_FOLDERS:
            folder_path = get_folder_directory(folder_name, SUBDIRECTORY)
            if folder_path:
                return folder_path
            
    return ''