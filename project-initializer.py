import argparse
import subprocess
import json
from time import sleep
from os.path import exists, abspath
from os import mkdir, getcwd, linesep, environ

PROJECT_DEFAULT_COMMANDS = ['lando start']
THEME_DEFAULT_COMMANDS = ['yarn build']
PLUGIN_DEFAULT_COMMANDS = []

DEFAULT_PROJECT_NAME = 'new-project'
DEFAULT_LANDO_CONFIG = {
    "recipe": "wordpress",
    "config": {
        "php": "8.1",
        "webroot": ".",
        "env": "dev",
        "xdebug": "true"
    },
    "services": {
        "pma": {
            "type": "phpmyadmin",
            "host": "database"
        },
        "mailhog": {
            "type": "mailhog",
            "hogfrom": "appserver",
            "portforward": "true"
        }
    }
}
PAGE_DEFAULT_TITLE = "Prueba"
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin"
DEFAULT_ADMIN_EMAIL = "admin@admin.com"

parser = argparse.ArgumentParser()
parser.add_argument("-start", "--start_recipe", help="Starts an existing project with the specified recipe")
parser.add_argument("-make", "--make_recipe", help="Makes a new project with the specified recipe")
parser.add_argument("-fast-make", "--fast_make", help="Makes a new project with username and password equal to 'admin' in the current directory")
parser.add_argument("-plubo-make", "--plubo_make", help="Makes a new project with a Sage theme with Plubo and a new Plubo plugin")
parser.add_argument("-make-recipe", "--make_new_recipe", help="Makes a new recipe for a new project for the current directory")
parser.add_argument("-make-start-recipe", "--make_start_recipe", help="Makes a new recipe for an existing project in the current directory")
parser.add_argument("-make-plugin", "--make_plugin", help="Makes a new plugin in the current lando project")
parser.add_argument("-make-theme", "--make_theme", help="Makes a new theme in the current lando project")
parser.add_argument("-add-plugin", "--add_plugin", help="Adds a Git plugin to the current lando project")
parser.add_argument("-add-theme", "--add_theme", help="Adds a Git theme to the current lando project")
parser.add_argument("-activate-plugin", "--activate_plugin", help="Activates a plugin in the current lando project")
parser.add_argument("-activate-theme", "--activate_theme", help="Activates a theme in the current lando project")
parser.add_argument("-no-post", "--no_post_commands", action="store_true", help="Doesn't execute the post commands")
parser.add_argument("-fast-start", "--fast_start", action="store_true", help="Starts the lando project in the current directory")
parser.add_argument("-configure-wp", "--configure_wp", action="store_true", help="Configures a new lando WordPress project")
# TODO: REORGANITZAR PROJECTE
# TODO: FIX ENV
# TODO: AFEGIR COMANDA -deactivate-plugin x
# TODO: AFEGIR COMANDA -deactivate-theme x
# TODO: AFEGIR COMANDA -update-tw-prefix QUE PER DEFECTE AGAFI LES VARIABLES DE TAILWIND I LES CANVII PEL NOU PREFIX, CANVIANT EL TW.CONFIG.
#           AFEGIR FLAG PER NO ACTUALITZAR EL TW.CONFIG.
#           AFEGIR FLAG PER NO AGAFAR EL PREFIX DE TW.CONFIG
# TODO: AFEGIR UNA CONSTANT WORKSPACE PATH
#           SI ESTÀ A TRUE, PER TOTS ELS PROJECTES NOUS CREA UNA CARPETA I ELS FICA AL WORKSPACE PATH
#           SI ESTÀ A TRUE, ES POT UTILITZAR UN NOU FLAG -start-project PROJECT_NAME I DIRECTAMENT PREPARA UN LANDO START
# TODO: AFEGIR COMANDA -build x QUE AGAFI LES COMANDES DE BUILD DEL RECIPE (S'HAURAN D'AFEGIR) I FA UN BUILD DEL PROJECTE
# TODO: CANVIAR CONFIGURACIO NOMBRE DE LA ENTRADA ALS COMMANDS DE MAKE
# TODO: AFEGIR COMANDA -add-constant x y PER AFEGIR UNA CONSTANT AL WP-CONFIG.PHP
# TODO: A LES COMANDES add-plugin i add-theme AFEGIR OPCIÓ DE POGUER FICAR PLUGINS I THEMES DEL REPO DE WORDPRESS 
# TODO: FLAG TO CHANGE PHP VERSION
# TODO: FLAG TO OPEN BROWSER WITH LANDO SITE
# TODO: FLAG TO OPEN LANDO DB && FLAG TO OPEN LANDO MAILHOG
# TODO: FLAG TO START A PROJECT (LANDO START + GIT PULLS + BUILDS)
# TODO: FLAG TO ENABLE DEBUG
# TODO: CHANGE NAME & ALIAS TO wp-dev
# TODO: FLAG TO ADD ENV VAR
# TODO: FLAG TO ADD AUTH VAR
# TODO: FLAG TO UPDATE CURRENT DIR REPOSITORIES
# TODO: FLAG TO MAKE GIT PLUGIN
# TODO: FLAG TO MAKE GIT THEME
# TODO: FLAG TO ADD CONSTANT TO WP-CONFIG
# TODO: MAYBE ADD COMMANDS TO MODIFY RECIPE FROM TERMINAL
# TODO: BASIC DOCUMENTATION
args = parser.parse_args()

def usage(error):
    if error == "args":
        print("You need to pass one argument to run this program")
    elif error == "recipe_path":
        print("Invalid path to recipe or invalid recipe format")
    elif error == "project_directory":
        print("You need to specify a project directory")
    elif error == "plugin_directory":
        print("You need to specify the plugin directory")
    elif error == "lando_directory":
        print("This directory doesn't contain a lando.yml file")
    exit(1)

def run_command(command, path=".", input="", environ=environ):
    subprocess.run([word for word in command.split()], cwd=path, input=input.encode(), env=environ)

def write_lando_file(lando_file, lando_config):
    if 'recipe' in lando_config.keys():
        lando_file.write("recipe: " + lando_config['recipe'] + '\n')
    if 'proxy' in lando_config.keys():
        lando_file.write("proxy:\n")
        if 'theme' in lando_config['proxy'].keys():
            lando_file.write("  theme:\n")
            lando_file.write("    - " + lando_config['proxy']['theme'] + '\n')
    if 'config' in lando_config.keys():
        lando_file.write("config:\n")
        if 'php' in lando_config['config'].keys():
            lando_file.write("  php: '" + lando_config['config']['php'] + "'\n")
        if 'via' in lando_config['config'].keys():
            lando_file.write("  via: " + lando_config['config']['via'] + '\n')
        if 'webroot' in lando_config['config'].keys():
            lando_file.write("  webroot: " + lando_config['config']['webroot'] + '\n')
        if 'env' in lando_config['config'].keys():
            lando_file.write("  env: " + lando_config['config']['env'] + '\n')
        if 'database' in lando_config['config'].keys():
            lando_file.write("  database: " + lando_config['config']['database'] + '\n')
        if 'xdebug' in lando_config['config'].keys():
            lando_file.write("  xdebug: " + lando_config['config']['xdebug'] + '\n')
    if 'services' in lando_config.keys():
        lando_file.write("services:\n")
        if 'theme' in lando_config['services'].keys():
            lando_file.write("  theme:\n")
            if 'type' in lando_config['services']['theme'].keys():
                lando_file.write("    type: " + lando_config['services']['theme']['type'] + '\n')
            if 'services' in lando_config['services']['theme'].keys():
                lando_file.write("    services:\n")
                if 'ports' in lando_config['services']['theme']['services'].keys():
                    lando_file.write("      ports:\n")
                    lando_file.write("        - " + lando_config['services']['theme']['services']['ports'] + '\n')
        if 'pma' in lando_config['services'].keys():
            lando_file.write('  pma:\n')
            if 'type' in lando_config['services']['pma'].keys():
                lando_file.write("    type: " + lando_config['services']['pma']['type'] + '\n')
            if 'host' in lando_config['services']['pma'].keys():
                lando_file.write("    host:\n")
                lando_file.write("      - " + lando_config['services']['pma']['host'] + '\n')
        if 'mailhog' in lando_config['services'].keys():
            lando_file.write("  mailhog:\n")
            if 'type' in lando_config['services']['mailhog'].keys():
                lando_file.write("    type: " + lando_config['services']['mailhog']['type'] + '\n')
            if 'hogfrom' in lando_config['services']['mailhog'].keys():
                lando_file.write("    hogfrom:\n")
                lando_file.write("      - " + lando_config['services']['mailhog']['hogfrom'] + '\n')
            if 'portforward' in lando_config['services']['mailhog'].keys():
                lando_file.write("    portforward: " + lando_config['services']['mailhog']['portforward'] + '\n')
        if 'appserver' in lando_config['services'].keys():
            lando_file.write("  appserver:\n")
            if 'type' in lando_config['services']['appserver'].keys():
                lando_file.write("    type: " + lando_config['services']['appserver']['type'] + '\n')
    if 'tooling' in lando_config.keys():
        lando_file.write("tooling:\n")
        if 'yarn' in lando_config['tooling'].keys():
            lando_file.write("  yarn:\n")
            if 'service' in lando_config['tooling']['yarn']:
                lando_file.write("    service: " + lando_config['tooling']['yarn']['service'])

if not args.start_recipe and not args.make_recipe and not args.fast_make and not args.plubo_make and not args.fast_start and not args.make_new_recipe and not args.make_start_recipe and not args.configure_wp and not args.make_plugin and not args.make_theme and not args.add_plugin and not args.add_theme and not args.activate_plugin and not args.activate_theme:
    usage('args')

if args.start_recipe:
    if not exists(args.start_recipe) or '.start-recipe.' not in args.start_recipe:
        usage('recipe_path')
    with open(args.start_recipe, 'r') as recipe_file:
        recipe = json.load(recipe_file)
    if not 'project_directory' in recipe.keys():
        usage('project_directory')
    
    if 'project_start_commands' in recipe.keys():
        for command in recipe['project_start_commands']:
                run_command(command, recipe['project_directory'])
    else:
        for command in PROJECT_DEFAULT_COMMANDS:
                run_command(command, recipe['project_directory'])
    
    if 'theme_git_directory' in recipe.keys():
        run_command("git pull", recipe['project_directory'] + recipe['theme_git_directory'])
    if 'theme_directory' in recipe.keys():
        if 'theme_start_commands' in recipe.keys():
            for command in recipe['theme_start_commands']:
                run_command(command,recipe['project_directory'] + recipe['theme_directory'])
        else:
            for command in THEME_DEFAULT_COMMANDS:
                run_command(command,recipe['project_directory'] + recipe['theme_directory'])

    if 'plugins' in recipe.keys():
        for plugin in recipe['plugins']:
            if not 'plugin_directory' in plugin.keys():
                usage('plugin_directory')
            if 'git_directory' in plugin.keys():
                run_command('git pull', recipe['project_directory'] + plugin['git_directory'])
            if 'plugin_start_commands' in plugin.keys():
                for command in plugin['plugin_start_commands']:
                    run_command(command, recipe['project_directory'] + plugin['plugin_directory'])
            else:
                for command in PLUGIN_DEFAULT_COMMANDS:
                    run_command(command, recipe['project_directory'] + plugin['plugin_directory'])

    if 'post_commands' in recipe.keys() and not args.no_post_commands:
        for command in recipe['post_commands']:
            run_command(command, recipe['project_directory'])
    print("Project started successfully")
    exit(1)

if args.make_recipe:
    if not exists(args.make_recipe) or '.recipe.' not in args.make_recipe:
        usage('recipe_path')
    with open(args.make_recipe, 'r') as recipe_file:
        recipe = json.load(recipe_file)
    if not 'project_directory' in recipe.keys():
        usage('project_directory')
    
    try:
        mkdir(recipe['project_directory'])
    except OSError:
        pass

    with open(recipe['project_directory'] + '/.lando.yml', 'w') as lando_file:
        if 'yarn_project_filename' in recipe.keys():
            lando_file.write("name: " + recipe['yarn_project_filename'] + '\n')
        else:
            lando_file.write("name: " + DEFAULT_PROJECT_NAME + '\n')
        
        if 'lando_config' in recipe.keys():
            write_lando_file(lando_file, recipe['lando_config'])
        else:
            write_lando_file(lando_file, DEFAULT_LANDO_CONFIG)

    if 'env_vars' in recipe.keys():
        with open(recipe['project_directory'] + '/.env', 'w') as env_file:
            for var, value in recipe['env_vars'].items():
                env_file.write(var.upper() + '=' + value + '\n')
            env_file.truncate(env_file.tell() - len(linesep))

    if 'auth_vars' in recipe.keys():
        with open(recipe['project_directory'] + '/auth.json', 'w') as json_file:
            json_file.write(json.dumps(recipe['auth_vars'], indent=4))

    run_command('lando rebuild', recipe['project_directory'], input="y")
    env_vars = environ
    env_vars['WP_CLI_CACHE_DIR'] = "/dev/null"
    run_command('lando wp core download --locale=es_ES --force', recipe['project_directory'], environ=env_vars)
    
    sleep(5)

    config_command = "lando wp config create --dbname=wordpress --dbuser=wordpress --dbpass=wordpress --dbhost=database --dbcharset=utf8mb4"
    if 'debug_enabled' in recipe.keys() and recipe['debug_enabled'] == '1':
        config_command += " --extra-php"
    run_command(config_command, recipe['project_directory'], input="define( 'WP_DEBUG', true );\ndefine( 'WP_DEBUG_LOG', true );\ndefine( 'WP_DEBUG_DISPLAY', false );\n@ini_set( 'display_errors', 0 );\n")

    selected_page_title = PAGE_DEFAULT_TITLE
    if 'page_title' in recipe.keys():
        selected_page_title = recipe['page_title']
    page_url = DEFAULT_PROJECT_NAME
    if 'yarn_project_filename' in recipe.keys():
        page_url = recipe['yarn_project_filename']
    selected_admin_username = DEFAULT_ADMIN_USERNAME
    if 'admin_username' in recipe.keys():
        selected_admin_username = recipe['admin_username']
    selected_admin_password = DEFAULT_ADMIN_PASSWORD
    if 'admin_password' in recipe.keys():
        selected_admin_password = recipe['admin_password']
    selected_admin_email = DEFAULT_ADMIN_EMAIL
    if 'admin_email' in recipe.keys():
        selected_admin_email = recipe['admin_email']

    run_command('lando wp core install --url=' + page_url + '.lndo.site' + ' --title=' + selected_page_title + ' --admin_user=' + selected_admin_username + ' --admin_password=' + selected_admin_password + ' --admin_email=' + selected_admin_email, recipe['project_directory'])
    
    if 'git_themes' in recipe.keys():
        for theme in recipe['git_themes']:
            run_command('git clone ' + theme, recipe['project_directory'] + '/wp-content/themes/')
    if 'store_plugins' in recipe.keys():
        for plugin in recipe['store_plugins']:
            run_command('lando wp plugin install ' + plugin + ' --activate', recipe['project_directory'])
    if 'git_plugins' in recipe.keys():
        for plugin in recipe['git_plugins']:
            run_command('git clone ' + plugin, recipe['project_directory'] + '/wp-content/plugins/')

    if 'post_commands' in recipe.keys() and not args.no_post_commands:
        for command in recipe['post_commands']:
            run_command(command, recipe['project_directory'])

    print("PROJECT CREATED SUCCESSFULLY")
    run_command('lando info', recipe['project_directory'])

if args.fast_make:

    with open('.lando.yml', 'w') as lando_file:
        lando_file.write("name: " + args.fast_make + '\n')
        write_lando_file(lando_file, DEFAULT_LANDO_CONFIG)
    
    run_command('lando rebuild', input="y")
    env_vars = environ
    env_vars['WP_CLI_CACHE_DIR'] = "/dev/null"
    run_command('lando wp core download --locale=es_ES --force', environ=env_vars)
    
    sleep(5)

    run_command("lando wp config create --dbname=wordpress --dbuser=wordpress --dbpass=wordpress --dbhost=database --dbcharset=utf8mb4 --extra-php", input="define( 'WP_DEBUG', true );\ndefine( 'WP_DEBUG_LOG', true );\ndefine( 'WP_DEBUG_DISPLAY', false );\n@ini_set( 'display_errors', 0 );\n")
    run_command('lando wp core install --url=' + args.fast_make + '.lndo.site' + ' --title=' + PAGE_DEFAULT_TITLE + ' --admin_user=' + DEFAULT_ADMIN_USERNAME + ' --admin_password=' + DEFAULT_ADMIN_PASSWORD + ' --admin_email=' + DEFAULT_ADMIN_EMAIL)
    print("PROJECT CREATED SUCCESSFULLY")
    run_command('lando info')

if args.plubo_make:

    with open('.lando.yml', 'w') as lando_file:
        lando_file.write("name: " + args.plubo_make + '\n')
        write_lando_file(lando_file, DEFAULT_LANDO_CONFIG)

    run_command('lando rebuild', input="y")
    env_vars = environ
    env_vars['WP_CLI_CACHE_DIR'] = "/dev/null"
    run_command('lando wp core download --locale=es_ES --force', environ=env_vars)

    sleep(5)

    run_command("lando wp config create --dbname=wordpress --dbuser=wordpress --dbpass=wordpress --dbhost=database --dbcharset=utf8mb4 --extra-php", input="define( 'WP_DEBUG', true );\ndefine( 'WP_DEBUG_LOG', true );\ndefine( 'WP_DEBUG_DISPLAY', false );\n@ini_set( 'display_errors', 0 );\n")
    run_command('lando wp core install --url=' + args.plubo_make + '.lndo.site' + ' --title=' + PAGE_DEFAULT_TITLE + ' --admin_user=' + DEFAULT_ADMIN_USERNAME + ' --admin_password=' + DEFAULT_ADMIN_PASSWORD + ' --admin_email=' + DEFAULT_ADMIN_EMAIL)
    
    run_command('lando composer create-project joanrodas/plubo ' + args.plubo_make + '-core', './wp-content/plugins/')
    run_command('lando composer create-project roots/sage ' + args.plubo_make, './wp-content/themes/')
    run_command('lando composer require roots/acorn', './wp-content/themes/' + args.plubo_make + '/')
    run_command('yarn', './wp-content/themes/' + args.plubo_make + '/')
    run_command('yarn build', './wp-content/themes/' + args.plubo_make + '/')

    run_command('lando wp plugin activate ' + args.plubo_make + '-core')
    run_command('lando wp theme activate ' + args.plubo_make)
    
    print("PROJECT CREATED SUCCESSFULLY")
    run_command('lando info')

if args.make_new_recipe:
    
    default_recipe = {
        "project_directory": abspath(getcwd()),
        "yarn_project_filename": args.make_new_recipe,
        "env_vars": {},
        "auth_vars": {},
        "debug_enabled": "1",
        "page_title": args.make_new_recipe,
        "admin_username": "admin",
        "admin_password": "admin",
        "admin_email": "admin@admin.admin",
        "git_themes": [],
        "store_plugins": [],
        "git_plugins": [],
        "post_commands": []
    }

    with open('./' + args.make_new_recipe + '.recipe.json', 'w') as json_file:
        json_file.write(json.dumps(default_recipe, indent=4))
    print("RECIPE CREATED SUCCESSFULLY: " + args.make_new_recipe + '.recipe.json')

if args.make_start_recipe:

    default_recipe = {
        "project_directory": abspath(getcwd()),
        "project_start_commands": ["lando start"],
        "theme_directory": "/wp-content/themes/" + args.make_start_recipe + "-theme/",
        "theme_git_directory": "/wp-content/themes/" + args.make_start_recipe + "-theme/",
        "theme_start_commands": ["yarn", "yarn build"],
        "plugins": [
            {
                "plugin_directory": "/wp-content/plugins/" + args.make_start_recipe + "-core/",
                "git_directory": "/wp-content/plugins/" + args.make_start_recipe + "-core/",
                "plugin_start_commands": ["yarn", "yarn build"]
            }
        ],
        "post_commands": []
    }

    with open('./' + args.make_start_recipe + '.start-recipe.json', 'w') as json_file:
        json_file.write(json.dumps(default_recipe, indent=4))
    print("START RECIPE CREATED SUCCESSFULLY: " + args.make_start_recipe + '.start-recipe.json')

if args.fast_start:

    project_name_line = False
    with open('./.lando.yml', 'r') as lando_file:
        for line in lando_file.readlines():
            if line.find("name: ") != -1:
                project_name_line = line
                break

    if project_name_line:
        project_name = project_name_line[project_name_line.find(": ") + 2 : -1]

        run_command('lando start')
        run_command('google-chrome https://' + project_name +  '.lndo.site/')
    else:
        usage("lando_directory")

if args.configure_wp:

    project_name_line = False
    with open('./.lando.yml', 'r') as lando_file:
        for line in lando_file.readlines():
            if line.find("name: ") != -1:
                project_name_line = line
                break

    if project_name_line:
        project_name = project_name_line[project_name_line.find(": ") + 2 : -1]

        run_command("lando wp config create --dbname=wordpress --dbuser=wordpress --dbpass=wordpress --dbhost=database --dbcharset=utf8mb4 --extra-php", input="define( 'WP_DEBUG', true );\ndefine( 'WP_DEBUG_LOG', true );\ndefine( 'WP_DEBUG_DISPLAY', false );\n@ini_set( 'display_errors', 0 );\n")
        run_command('lando wp core install --url=' + project_name + '.lndo.site' + ' --title=' + PAGE_DEFAULT_TITLE + ' --admin_user=' + DEFAULT_ADMIN_USERNAME + ' --admin_password=' + DEFAULT_ADMIN_PASSWORD + ' --admin_email=' + DEFAULT_ADMIN_EMAIL)

    else:
        usage("lando_directory")

if args.make_plugin:

    run_command('lando composer create-project joanrodas/plubo ' + args.make_plugin + '-core', './wp-content/plugins/')
    run_command('lando wp plugin activate ' + args.make_plugin + '-core')

if args.make_theme:
    
    run_command('lando composer create-project roots/sage ' + args.make_theme, './wp-content/themes/')
    run_command('lando composer require roots/acorn', './wp-content/themes/' + args.make_theme + '/')
    run_command('yarn', './wp-content/themes/' + args.make_theme + '/')
    run_command('yarn build', './wp-content/themes/' + args.make_theme + '/')
    run_command('lando wp theme activate ' + args.make_theme)

if args.add_plugin:

    plugin_name = args.add_plugin.split('/')[-1][0:args.add_plugin.split('/')[-1].find('.git')]
    run_command('git clone ' + args.add_plugin, './wp-content/plugins/')
    run_command('lando composer install', './wp-content/plugins/' + plugin_name + '/')
    run_command('lando wp plugin activate ' + plugin_name)

if args.add_theme:
    
    theme_name = args.add_theme.split('/')[-1][0:args.add_theme.split('/')[-1].find('.git')]
    run_command('git clone ' + args.add_theme, './wp-content/themes/')
    run_command('lando composer install', './wp-content/themes/' + theme_name + '/')
    run_command('yarn', './wp-content/themes/' + theme_name + '/')
    run_command('yarn build', './wp-content/themes/' + theme_name + '/')
    run_command('lando wp theme activate ' + theme_name)

if args.activate_plugin:

    run_command('lando wp plugin activate ' + args.activate_plugin)

if args.activate_theme:
    
    run_command('lando wp theme activate ' + args.activate_theme)