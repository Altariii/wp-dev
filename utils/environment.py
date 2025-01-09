import json
import yaml
from typing import Any, Dict

from ..constants.environment import *
from ..constants.config import BEDROCK_BOILERPLATE
from ..constants.config import WP_DEFAULT_DB_NAME, WP_DEFAULT_DB_USER, WP_DEFAULT_DB_PASS, WP_DEFAULT_DB_HOST, WP_DEFAULT_DB_CHARSET
from ..utils import console, lando

def generate_yml(config: Dict[str, Any], indent: int = 2) -> str:
    def represent_dict(dumper, data):
        return dumper.represent_mapping('tag:yaml.org,2002:map', data.items())

    def represent_str(dumper, data):
        if '\n' in data:
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)

    yaml.add_representer(dict, represent_dict)
    yaml.add_representer(str, represent_str)

    class IndentDumper(yaml.Dumper):
        def increase_indent(self, flow=False, indentless=False):
            return super().increase_indent(flow, False)

    return yaml.dump(config, Dumper=IndentDumper, default_flow_style=False, indent=indent)

def generate_env(config: Dict[str, Any]) -> str:
    env_file = ''
    for key, value in config.items():
        escaped_value = str(value).replace('"', '\\"')
        env_file += f'{key}="{escaped_value}"\n'

    return env_file[:-1]

def generate_json(config: Dict[str, Any], indent: int = 4) -> str:
    return json.dumps(config, indent=indent)

def store_file(file_name: str, content: str, path: str) -> bool:
    final_path = path[:-1] if path[-1] == '/' else path

    try:
        with open(f'{final_path}/{file_name}', 'w', encoding='utf-8') as file:
            file.write(content)
            return True
    except IOError as e:
        print(e)
        return False

def create(
        project_name: str,
        project_slug: str,
        workspace: str,
        admin_username: str,
        admin_password: str,
        admin_email: str,
        php_version: str = DEFAULT_PHP_VERSION,
        wp_version: str = DEFAULT_WP_VERSION,
        use_bedrock: bool = DEFAULT_BEDROCK,
        wp_lang: str = DEFAULT_WP_LANG,
        wp_debug: str = DEFAULT_DEBUG
) -> None:
    if use_bedrock:
        create_bedrock(
            project_name,
            project_slug,
            workspace,
            admin_username,
            admin_password,
            admin_email,
            php_version,
            wp_version,
            wp_lang,
            wp_debug
        )
    else:
        create_native(
            project_name,
            project_slug,
            workspace,
            admin_username,
            admin_password,
            admin_email,
            php_version,
            wp_version,
            wp_lang,
            wp_debug
        )

def create_bedrock(
        project_name: str,
        project_slug: str,
        workspace: str,
        admin_username: str = DEFAULT_ADMIN_USERNAME,
        admin_password: str = DEFAULT_ADMIN_PASSWORD,
        admin_email: str = DEFAULT_ADMIN_EMAIL,
        php_version: str = DEFAULT_PHP_VERSION,
        wp_version: str = DEFAULT_WP_VERSION,
        wp_lang: str = DEFAULT_WP_LANG,
        wp_debug: str = DEFAULT_DEBUG
) -> None:
    
    yml_file = generate_yml({
        "name": project_slug,
        "recipe": "wordpress",
        "proxy": {
            "theme": ["localhost:3000"]
        },
        "config": {
            "php": php_version,
            "via": "nginx",
            "webroot": "web",
            "database": "mariadb",
            "xdebug": True
        },
        "services": {
            "theme": {
                "type": "node",
                "services": {
                    "ports": ["3000:3000"]
                }
            },
            "pma": {
                "type": "phpmyadmin",
                "host": ["database"]
            },
            "mailhog": {
                "type": "mailhog",
                "hogfrom": ["appserver"],
                "portforward": True
            },
        },
        "tooling": {
            "yarn": {
                "service": "theme"
            }
        }
    })
    wpdev_config = DEFAULT_WPDEV_CONFIG
    wpdev_config['bedrock'] = True
    json_file = generate_json(wpdev_config)

    console.run_command(f"mkdir {project_slug}", path=workspace)
    store_file('.lando.yml', yml_file, path=f"{workspace}/{project_slug}")
    store_file('wp_dev.config.json', json_file, path=f"{workspace}/{project_slug}")
    lando.start(f"{workspace}/{project_slug}")
    
    console.run_command("mkdir temp", path=f"{workspace}/{project_slug}")
    lando.composer.create_project(BEDROCK_BOILERPLATE, '.', f"{workspace}/{project_slug}/temp")
    console.run_command("mv temp/* temp/.[!.]* .", path=f"{workspace}/{project_slug}", shell=True)
    console.run_command("rm -rf temp", path=f"{workspace}/{project_slug}")
    
    lando.composer.require(f'roots/wordpress:{wp_version}', f"{workspace}/{project_slug}")
    lando.composer.install(f'{workspace}/{project_slug}')
    
    env_file = generate_env({
        "DB_NAME": "wordpress",
        "DB_USER": "wordpress",
        "DB_PASSWORD": "wordpress",
        "DB_HOST": "database",
        "WP_ENV": "development",
        "WP_HOME": f"https://{project_slug}.lndo.site",
        "WP_SITEURL": "${WP_HOME}/wp"
    })
    store_file('.env', env_file, path=f"{workspace}/{project_slug}")

    if wp_debug:
        console.run_commands([
            "sed -i -e \"s/Config::define('WP_DEBUG_LOG', false);/Config::define('WP_DEBUG_LOG', true);/\" ./config/application.php",
            "sed -i -e \"s/Config::define('SCRIPT_DEBUG', false);/Config::define('WP_DEBUG', true);/\" ./config/application.php"
        ], path=f"{workspace}/{project_slug}", shell=True)

    lando.wp.install_core(
        url             = f'{project_slug}.lndo.site',
        title           = project_name,
        admin_username  = admin_username,
        admin_password  = admin_password,
        admin_email     = admin_email,
        project_path    = f'{workspace}/{project_slug}'
    )
    lando.wp.install_core_language(wp_lang, f"{workspace}/{project_slug}")
    lando.wp.switch_installed_language(wp_lang, f"{workspace}/{project_slug}")
    lando.wp.update_option('permalink_structure', '"/%postname%/"', f"{workspace}/{project_slug}")
    lando.wp.uninstall_all_plugins(f"{workspace}/{project_slug}")

def create_native(
    project_name: str,
    project_slug: str,
    workspace: str,
    admin_username: str = DEFAULT_ADMIN_USERNAME,
    admin_password: str = DEFAULT_ADMIN_PASSWORD,
    admin_email: str = DEFAULT_ADMIN_EMAIL,
    php_version: str = DEFAULT_PHP_VERSION,
    wp_version: str = DEFAULT_WP_VERSION,
    wp_lang: str = DEFAULT_WP_LANG,
    wp_debug: str = DEFAULT_DEBUG
) -> None:
    yml_file = generate_yml({
        "name": project_slug,
        "recipe": "wordpress",
        "config": {
            "php": php_version,
            "webroot": ".",
            "env": "dev",
            "xdebug": True
        },
        "services": {
            "pma": {
                "type": "phpmyadmin",
                "host": ["database"]
            },
            "mailhog": {
                "type": "mailhog",
                "hogfrom": ["appserver"],
                "portforward": True
            },
        },
    })
    json_file = generate_json(DEFAULT_WPDEV_CONFIG)

    console.run_command(f"mkdir {project_slug}", path=workspace)
    store_file('wp_dev.config.json', json_file, path=f"{workspace}/{project_slug}")
    store_file('.lando.yml', yml_file, path=f"{workspace}/{project_slug}")
    lando.start(f"{workspace}/{project_slug}")

    lando.wp.download_core(version=wp_version, locale=wp_lang, project_path=f"{workspace}/{project_slug}")

    PHP_COMMANDS = [
        "define( 'WP_DEBUG', true )",
        "define( 'WP_DEBUG_LOG', true )",
        "define( 'WP_DEBUG_DISPLAY', false )",
        "@ini_set( 'display_errors', 0 )"
    ] if wp_debug else []

    lando.wp.create_config_file(
        db_name = WP_DEFAULT_DB_NAME,
        db_user = WP_DEFAULT_DB_USER,
        db_password = WP_DEFAULT_DB_PASS,
        db_host = WP_DEFAULT_DB_HOST,
        db_charset = WP_DEFAULT_DB_CHARSET,
        php_commands = PHP_COMMANDS,
        project_path = f"{workspace}/{project_slug}"
    )
    lando.wp.install_core(
        url             = f'{project_slug}.lndo.site',
        title           = project_name,
        admin_username  = admin_username,
        admin_password  = admin_password,
        admin_email     = admin_email,
        project_path    = f'{workspace}/{project_slug}'
    )
    lando.wp.update_option('permalink_structure', '"/%postname%/"', f"{workspace}/{project_slug}")
    lando.wp.uninstall_all_plugins(f"{workspace}/{project_slug}")