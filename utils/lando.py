import os
import json
import re
import ast

from ..utils import console
from ..constants.config import LANDO_CONFIG_NAME

class composer:
    def create_project(boilerplate: str, project_name: str, composer_path: str) -> None:
        console.run_command(f"lando composer create-project {boilerplate} {project_name}", composer_path)

    def install(composer_path: str) -> None:
        console.run_command("lando composer install", composer_path)

    def update(composer_path: str) -> None:
        console.run_command("lando composer update", composer_path)

    def require(dependency: str, composer_path: str) -> None:
        console.run_command("lando composer require " + dependency, composer_path)

class wp:
    def download_core(version = None, locale = None, project_path: str = '') -> None:
        command = 'lando wp core download'
        if version:
            command += f' --version={version}'
        if locale:
            command += f' --locale={locale}'
        console.run_command(command, project_path, shell=True)

    def install_core(url: str = '', title: str = '', admin_username: str = '', admin_password: str = '', admin_email: str = '', project_path: str = '') -> None:
        command = 'lando wp core install'
        if url:
            command += f' --url={url}'
        if title:
            command += f' --title="{title}"'
        if admin_username:
            command += f' --admin_user="{admin_username}"'
        if admin_password:
            command += f' --admin_password="{admin_password}"'
        if admin_email:
            command += f' --admin_email={admin_email}'
        console.run_command(command, project_path, shell=True)

    def install_core_language(language: str, project_path: str) -> None:
        console.run_command(f'lando wp language core install {language}', project_path)

    def switch_installed_language(language: str, project_path: str) -> None:
        console.run_command(f'lando wp site switch-language {language}', project_path)

    def create_config_file(db_name: str = '', db_user: str = '', db_password: str = '', db_host: str = '', db_charset: str = '', php_commands: list[str] = [], project_path: str = '') -> None:
        command = 'lando wp config create'
        if db_name:
            command += f' --dbname={db_name}'
        if db_user:
            command += f' --dbuser={db_user}'
        if db_password:
            command += f' --dbpass={db_password}'
        if db_host:
            command += f' --dbhost={db_host}'
        if db_charset:
            command += f' --dbcharset={db_charset}'
        if len(php_commands) > 0:
            command += f' --extra-php'
        console.run_command(command, input=(';\n'.join(php_commands)) + ';\n', path=project_path, shell=True)

    def update_option(name: str, value, project_path: str) -> None:
        console.run_command(f'lando wp option update {name} {value}', project_path, shell=True)

    def activate_plugin(plugin_slug: str, project_path: str) -> None:
        console.run_command(f'lando wp plugin activate {plugin_slug}', project_path, shell=True)

    def uninstall_all_plugins(project_path: str) -> None:
        console.run_command(f'lando wp plugin uninstall --deactivate --all', project_path, shell=True)

def start(project_path: str) -> None:
    console.run_command("lando start", project_path)

def restart(project_path: str) -> None:
    console.run_command("lando restart", project_path)

def rebuild(project_path: str) -> None:
    console.run_command("lando rebuild", project_path, input="y")

def stop(project_path: str) -> None:
    console.run_command("lando stop", project_path)

def destroy(project_path: str) -> None:
    console.run_command("lando destroy", project_path, input="y")

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
    
def exec_ssh_command(service: str, command: str, show_output: bool = True, shell: bool = False) -> None:
    console.run_command(f'lando ssh {command}', service, show_output=show_output, shell=shell)