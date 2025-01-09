import os

# GITHUB
GITHUB_URL                      = 'https://github.com/Altariii/wp-dev'
GITHUB_CONFIG_URL               = 'https://raw.githubusercontent.com/Altariii/wp-dev/main/config/config.json'

# FILE PATHS
WP_DEV_PATH                     = os.path.dirname(os.path.abspath(__file__)).replace('constants', '')[:-1]
CONFIG_FILE_PATH                = WP_DEV_PATH + '/config/config.json'

# FOLDER NAMES
WP_CONTENT_NAME                 = 'wp-content'
WP_BEDROCK_CONFIG               = 'config'
WP_CONTENT_BEDROCK              = 'web/app'
WP_PLUGINS_FOLDER               = 'plugins'
WP_THEMES_FOLDER                = 'themes'

# DEFAULT WP CONFIG
WP_DEFAULT_DB_NAME              = 'wordpress'
WP_DEFAULT_DB_USER              = 'wordpress'
WP_DEFAULT_DB_PASS              = 'wordpress'
WP_DEFAULT_DB_HOST              = 'database'
WP_DEFAULT_DB_CHARSET           = 'utf8mb4'

# FILE NAMES
WP_DEV_CONFIG_NAME              = 'wp_dev.config.json'
WP_DEBUG_FILE                   = 'debug.log'
LANDO_CONFIG_NAME               = '.lando.yml'

# BOILERPLATE NAMES
BEDROCK_BOILERPLATE             = 'roots/bedrock'
DEFAULT_PLUGIN_BOILERPLATE      = 'joanrodas/plubo'

# COMPOSER && NPM CONFIG
DEFAULT_COMPOSER_NAME_PREFIX    = 'sirvelia'