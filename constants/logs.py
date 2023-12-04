from ..utils import console

# LOG ERRORS
PHP_NOTICE = 'PHP Notice:'
PHP_WARNING = 'PHP Warning:'

WP_DB_ERROR = 'WordPress database error'

# LOG COLORS
LOG_FORMATS = {
    PHP_NOTICE: console.colors.YELLOW,
    PHP_WARNING: console.colors.YELLOW_BG,
    WP_DB_ERROR: console.colors.RED
}