import time

from ..utils import console

from ..commands.fast_lando_toolkit import FastLandoToolkitPage
from ..commands.fast_start import FastStartCommand
from ..commands.fast_restart import FastRestartCommand
from ..commands.fast_rebuild import FastRebuildCommand
from ..commands.fast_stop import FastStopCommand
from ..commands.fast_show import FastShowCommand
from ..commands.fast_show_mailhog import FastShowMailhogCommand
from ..commands.fast_show_database import FastShowDatabaseCommand
from ..commands.fast_show_logs import FastShowLogsCommand

from ..commands.project_management import ProjectManagementPage
from ..commands.config import ConfigPage
from ..commands.exit import ExitCommand, bye

from ..commands.start import StartCommand

from ..commands.set_workspace import SetWorkspaceCommand

class CommandList:
    current_pages = ["Main"]
    commands = [
        ProjectManagementPage,
        # PLUGIN MANAGEMENT PAGE
        # WORDPRESS CONFIG PAGE
        # DEVELOPER PAGE
        ConfigPage,
        ExitCommand,

        FastLandoToolkitPage,
        StartCommand,
        # PrepareCommand
        # MakeCommand
        # UpdateCommand
        # DestroyCommand

        # CreatePluginCommand
        # CreateThemeCommand
        # AddPluginCommand
        # AddThemeCommand
        # CreateProjectRelease (wp dist-archive)

        # VSCodeOpenerCommand
        # ToggleDebugCommand
        # ManageUsersCommand
        # ManageUserRolesCommand
        # AddConstantCommand
        # TogglePluginCommand

        # UpdateTailwindPrefixCommand

        SetWorkspaceCommand,
        # ManageGitAccountsCommand
        # UpdateWPDevCommand

        FastStartCommand,
        FastRestartCommand,
        FastRebuildCommand,
        FastStopCommand,
        FastShowCommand,
        FastShowMailhogCommand,
        FastShowDatabaseCommand,
        FastShowLogsCommand
    ]
    command_menus = {'Main': []}

    def __init__(self) -> None:
        for command in self.commands:
            if command.parent_page not in self.command_menus:
                self.command_menus[command.parent_page] = [command]
            else:
                self.command_menus[command.parent_page].append(command)

    def display_current_options(self) -> None:
        console.display.clear()
        console.display.banner()
        console.display.description(f"{self.current_pages[-1]} Menu")
        
        print(" Input    Description")
        print("=======  ==============================")
        for command in self.command_menus[self.current_pages[-1]]:
            print(f"  [{command.key}]     {command.description}")
        if len(self.current_pages) > 1:
            print(f"  [<]     Back to {self.current_pages[-2]} Menu")
        print("")

    def exec_command(self, key: str) -> None:
        if key == '<' and len(self.current_pages) > 1:
            self.current_pages.pop(-1)
            return
        
        for command in self.command_menus[self.current_pages[-1]]:
            if command.key == key:
                if command.handler is not None:
                    command.handler()
                    time.sleep(2)
                if command.submenu_page:
                    self.current_pages.append(command.submenu_page)
                return
            
        console.display.error("Invalid Input!")
        bye()
            
    def choice(self) -> None:
        self.display_current_options()

        action = console.display.request("Enter your desired option")

        self.exec_command(action)
        self.choice()