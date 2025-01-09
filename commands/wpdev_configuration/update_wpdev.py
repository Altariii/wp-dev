from ...modules.argument_handler import update

class UpdateWPDevCommand:
    parent_page = "WP-DEV Configuration"
    submenu_page = False
    key = '3'
    description = 'Check for WP-DEV Updates'
    handler = update