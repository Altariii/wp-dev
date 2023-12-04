import os

from ..constants.config import WP_CONTENT_NAME, WP_CONTENT_BEDROCK, WP_BEDROCK_CONFIG, WP_DEBUG_FILE

def is_bedrock(project_path: str) -> bool:
    return os.path.exists(os.path.join(project_path, WP_BEDROCK_CONFIG))

def get_logs(project_path: str) -> str:
    log_file_path = ""
    if is_bedrock(project_path):
        log_file_path = os.path.join(project_path, WP_CONTENT_BEDROCK)
    else:
        log_file_path = os.path.join(project_path, WP_CONTENT_NAME)

    if not os.path.exists(log_file_path) or not os.path.isfile(os.path.join(log_file_path, WP_DEBUG_FILE)):
        return ""
    
    logs = ""
    with open(os.path.join(log_file_path, WP_DEBUG_FILE), 'r') as log_file:
        logs = log_file.read()

    return logs.split('\n')[:-1]