import os

from ....constants.logs import LOG_FORMATS
from ....utils import console
from ....utils import lando
from ....utils import wordpress

def style_log(log: str, find: str, color: str) -> str:
    if find in log:
        return console.colors.BOLD + color + log[0:log.find(find) + len(find)] + console.colors.ENDC + log[log.find(find) + len(find):]
    else:
        return log
    
def format_log(log: str) -> str:
    styled_log = log
    for [log_name, log_color] in LOG_FORMATS.items():
        styled_log = style_log(styled_log, log_name, log_color)
    return styled_log

def format_logs(logs: list[str]) -> list[str]:
    formatted_logs = []
    for log in logs:
        formatted_logs.append(format_log(log))
    return formatted_logs

def fast_show_logs() -> None:
    console.display.clear()
    console.display.banner()
    console.display.description("WP-DEV Project Lando Logs")
    print("")

    project_path = lando.get_running_service_path()
    if project_path:
        console.display.info("Found running project: " + project_path)
    else:
        console.display.warning("No running lando project found. Trying with current directory")
        project_path = os.getcwd()
    
    wp_logs = wordpress.get_logs(project_path)
    if not wp_logs:
        console.display.error("No logs have been found for this project.")
        return
    
    formatted_logs = format_logs(wp_logs)
    for log in formatted_logs:
        print(log)

    console.display.request("Press any key to finish")

class FastShowLogsCommand:
    parent_page = "Fast Lando Toolkit"
    submenu_page = False
    key = '8'
    description = 'Shows the Lando Project Logs'
    handler = fast_show_logs
