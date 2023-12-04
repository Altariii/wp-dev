import argparse

from ..modules import updater

from ..config import config
from ..constants import config as config_constants
from ..utils import console
from ..commands.exit import bye

def define_args():
    parser = argparse.ArgumentParser(prog="wp-dev.py", add_help=False)
    parser.add_argument('-h', '--help', action='store_true')
    parser.add_argument('--version', action='store_true')
    parser.add_argument('--update', action='store_true')
    args = parser.parse_args()

    handle_args(args)

def handle_args(args) -> None:
    
    if args.help:
        help()

    if args.version:
        version()

    if args.update:
        update()

    # TODO: ADD ARGUMENT FOR EACH INSTRUCTIONS, WITH INTERNAL CONFIGURATION AS FLAGS

def help() -> None:
    print(
    """
WP-DEV Version: {0}
GitHub: {4}
Coded By: {1}{3} @Altariii {2}

USAGE:
        python3 wp-dev.py

VERSION & UPDATING:
        --update                    Update WP-DEV (Requires git)
        --version                   Show WP-DEV version and exit

HELP
        -h, --help                  Shows this help message and exit

EXAMPLE USAGE:
        python3 wp-dev.py

    """.format(config.version(), console.colors.RED, console.colors.ENDC, console.colors.BOLD, config_constants.GITHUB_URL)
    )
    bye()

def version() -> None:
    console.display.info("WP-DEV Version: " + config.version())
    bye()

def update() -> None:
    console.display.clear()
    console.display.banner()
    console.display.description("Update Menu")
    console.display.info("Checking for Updates...\n")

    [has_latest_version, current_version, latest_version] = updater.check_last_version()

    if has_latest_version:
        print("")
        console.display.result("WP-DEV is up to date, you're good to go!", "")
    else:
        print("")
        console.display.success("Update Available!")
        update_consent = console.display.request("Do you want to update WP-DEV now? (y/n)")
        if update_consent.lower() == 'y':
            updater.attempt_update(current_version, latest_version)
        else:
            print("")
            console.display.warning("Update Cancelled!")
    bye()