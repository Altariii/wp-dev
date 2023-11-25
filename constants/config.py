import os

# GITHUB
GITHUB_URL          = 'https://github.com/Altariii/wp-dev'
GITHUB_CONFIG_URL   = 'https://raw.githubusercontent.com/Altariii/wp-dev/main/config/config.json'

# FILE PATHS
WP_DEV_PATH         = os.path.dirname(os.path.abspath(__file__)).replace('constants', '')[:-1]
CONFIG_FILE_PATH    = './wp-dev/config/config.json'