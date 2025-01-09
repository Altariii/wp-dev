import os

from ..constants.config import WP_CONTENT_NAME, WP_CONTENT_BEDROCK, WP_BEDROCK_CONFIG, WP_DEBUG_FILE, WP_PLUGINS_FOLDER, WP_THEMES_FOLDER

def is_bedrock(project_path: str) -> bool:
    return os.path.exists(os.path.join(project_path, WP_BEDROCK_CONFIG))

def is_plugin(project_path: str, plugin_slug: str) -> str:
    wp_content_path = get_wp_content_path(project_path)
    PLUGINS_FOLDER = os.path.join(wp_content_path, WP_PLUGINS_FOLDER)
    if not os.path.exists(PLUGINS_FOLDER):
        return ''
    PLUGIN_PATH = os.path.join(PLUGINS_FOLDER, plugin_slug)
    if not os.path.isdir(PLUGIN_PATH):
        return ''
    return PLUGIN_PATH

def is_theme(project_path: str, theme_slug: str) -> str:
    wp_content_path = get_wp_content_path(project_path)
    THEMES_FOLDER = os.path.join(wp_content_path, WP_THEMES_FOLDER)
    if not os.path.exists(THEMES_FOLDER):
        return ''
    THEME_PATH = os.path.join(THEMES_FOLDER, theme_slug)
    if not os.path.isdir(THEME_PATH):
        return ''
    return THEME_PATH

def get_wp_content_path(project_path: str) -> str:
    if is_bedrock(project_path):
        return os.path.join(project_path, WP_CONTENT_BEDROCK)
    return os.path.join(project_path, WP_CONTENT_NAME)

def get_logs(project_path: str) -> str:
    log_file_path = get_wp_content_path(project_path)

    if not os.path.exists(log_file_path) or not os.path.isfile(os.path.join(log_file_path, WP_DEBUG_FILE)):
        return ""
    
    logs = ""
    with open(os.path.join(log_file_path, WP_DEBUG_FILE), 'r') as log_file:
        logs = log_file.read()

    return logs.split('\n')[:-1]