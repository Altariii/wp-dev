import argparse

from ..config import config
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

    """.format(config.version(), console.colors.RED, console.colors.ENDC, console.colors.BOLD, config.GITHUB_URL)
    )
    bye()

def version() -> None:
    print("\n\n")
    console.display.info("WP-DEV Version: " + config.version())
    bye()

def update() -> None:
    # TODO: CONTINUE