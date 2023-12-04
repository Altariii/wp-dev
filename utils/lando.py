import os
import json
import re
import ast

from ..utils import console
from ..constants.config import LANDO_CONFIG_NAME

def start(project_path: str) -> None:
    console.run_command("lando start", project_path)

def restart(project_path: str) -> None:
    console.run_command("lando restart", project_path)

def rebuild(project_path: str) -> None:
    console.run_command("lando rebuild", project_path, input="y")

def stop(project_path: str) -> None:
    console.run_command("lando stop", project_path)

def service_list() -> list[dict]:
    command_output = console.run_command("lando list", os.getcwd(), show_output=False)
    json_string = re.sub(r'(\w+):', r'"\1":', command_output)
    if command_output:
        return json.loads(json_string.replace("'", "\""))
    else:
        return []
    
def info(project_path: str) -> list[dict]:
    command_output = console.run_command("lando info", project_path, show_output=False)
    json_string = re.sub(r'(\w+)(:\s|\n)', r'"\1"\2', command_output)
    json_string = json_string.replace('true', 'True').replace('false', 'False').replace('null', 'None')
    if command_output:
        return ast.literal_eval(json_string)
    else:
        return []
    
def get_running_services() -> list[dict]:
    services_list = service_list()
    running_services = []
    for service in services_list:
        if service['service'] == 'appserver' and service['kind'] == 'app':
            running_services.append(service)

    return running_services

def is_running(service: str, running_services: list[dict] | bool = False) -> bool:
    if not running_services:
        running_services = get_running_services()
    for running_service in running_services:
        if running_service['app'] == service:
            return True
    return False

def get_running_service_path() -> str | None:
    running_services = get_running_services()
    if len(running_services) > 0:
        return running_services[0]['src'][0].replace(LANDO_CONFIG_NAME, '')