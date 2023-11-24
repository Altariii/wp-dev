from ..utils import console

def bye() -> None:
    print("\n" + console.colors.BOLD + console.colors.RED + " Bye! " + console.colors.ENDC)
    quit()