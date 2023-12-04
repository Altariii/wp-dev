import os

# GITHUB
GITHUB_URL          = 'https://github.com/Altariii/wp-dev'
GITHUB_CONFIG_URL   = 'https://raw.githubusercontent.com/Altariii/wp-dev/main/config/config.json'

# FILE PATHS
WP_DEV_PATH         = os.path.dirname(os.path.abspath(__file__)).replace('constants', '')[:-1]
CONFIG_FILE_PATH    = WP_DEV_PATH + '/config/config.json'

# FOLDER NAMES
WP_CONTENT_NAME     = 'wp-content'
WP_BEDROCK_CONFIG   = 'config'
WP_CONTENT_BEDROCK  = 'web/app'

# FILE NAMES
WP_DEV_CONFIG_NAME  = 'wp_dev.config.json'
WP_DEBUG_FILE       = 'debug.log'
LANDO_CONFIG_NAME   = '.lando.yml'