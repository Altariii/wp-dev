from ..utils import console

def bye() -> None:
    print("\n" + console.colors.BOLD + console.colors.RED + " Bye! " + console.colors.ENDC)
    quit()

class ExitCommand:
    parent_page = 'Main'
    submenu_page = False
    key = '0'
    description = 'Exit WP-DEV :('
    handler = bye