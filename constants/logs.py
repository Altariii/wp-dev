from ..utils import console

# LOG ERRORS
PHP_NOTICE = 'PHP Notice:'
PHP_WARNING = 'PHP Warning:'
PHP_DEPRECATED = 'PHP Deprecated:'
PHP_FATAL_ERROR = 'PHP Fatal error:'

WP_DB_ERROR = 'WordPress database error'

PLUBO_LOG_ERROR = 'LOG:'

# LOG COLORS
LOG_FORMATS = {
    PHP_NOTICE: console.colors.YELLOW,
    PHP_WARNING: console.colors.YELLOW_BG,
    PHP_DEPRECATED: console.colors.YELLOW,
    PHP_FATAL_ERROR: console.colors.RED,
    WP_DB_ERROR: console.colors.RED,
    PLUBO_LOG_ERROR: console.colors.CYAN
}