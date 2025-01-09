import time

from ..utils import console

from ..commands.projects import ProjectManagementPage
from ..commands.plugins import PluginManagementPage
from ..commands.config import ConfigPage
from ..commands.exit import ExitCommand, bye

from ..commands.project_management.fast_lando_toolkit import FastLandoToolkitPage
from ..commands.project_management.start import StartCommand
from ..commands.project_management.open_folder import OpenFolderCommand
from ..commands.project_management.make import MakeCommand
from ..commands.project_management.update import UpdateCommand
from ..commands.project_management.destroy import DestroyCommand

from ..commands.project_management.lando_toolkit.fast_start import FastStartCommand
from ..commands.project_management.lando_toolkit.fast_restart import FastRestartCommand
from ..commands.project_management.lando_toolkit.fast_rebuild import FastRebuildCommand
from ..commands.project_management.lando_toolkit.fast_stop import FastStopCommand
from ..commands.project_management.lando_toolkit.fast_show import FastShowCommand
from ..commands.project_management.lando_toolkit.fast_show_mailhog import FastShowMailhogCommand
from ..commands.project_management.lando_toolkit.fast_show_database import FastShowDatabaseCommand
from ..commands.project_management.lando_toolkit.fast_show_logs import FastShowLogsCommand
from ..commands.project_management.lando_toolkit.fast_open_folder import FastOpenFolderCommand

from ..commands.plugin_management.create_plugin import CreatePluginCommand

from ..commands.wpdev_configuration.set_workspace import SetWorkspaceCommand
from ..commands.wpdev_configuration.remove_workspace import RemoveWorkspaceCommand
from ..commands.wpdev_configuration.update_wpdev import UpdateWPDevCommand
from ..commands.wpdev_configuration.manage_git_accounts import ManageGitAccountsPage

from ..commands.wpdev_configuration.git.add_git_account import AddGitAccountCommand
from ..commands.wpdev_configuration.git.update_git_credentials import UpdateGitCredentialsCommand
from ..commands.wpdev_configuration.git.remove_git_account import RemoveGitAccountCommand

class CommandList:
    current_pages = ["Main"]
    commands = [
        ProjectManagementPage,
        PluginManagementPage,
        # FRAMEWORK MANAGEMENT COMMAND
        # WORDPRESS CONFIG PAGE
        # DEVELOPER PAGE
        ConfigPage,
        ExitCommand,

        FastLandoToolkitPage,
        StartCommand,
        OpenFolderCommand,
        MakeCommand,
        # Make from Duplicator (mirar què es pot fer)
        UpdateCommand,
        DestroyCommand,
        # ExportCommand         (exports project into a wp_dev.project.json file, which can be imported from another folder)
        # ImportCommand         (imports a previously exported project)

        CreatePluginCommand, # TODO: (+git integration & readme modification)
        # CreateThemeCommand
        # AddPluginCommand
        # AddThemeCommand
        # CreateProjectRelease (wp dist-archive + readme version update + git commits? + Subversion?)

        # SetupTailwindCSS
        # SetupDaisyUI
        # SetupAlpineJS
        # SetupHikeFlowJS

        # VSCodeOpenerCommand (detects all project dependencies and opens a VSCode)
        # ToggleDebugCommand
        # ExecWPCLICommand
        # AddConstantCommand
        # TogglePluginCommand

        SetWorkspaceCommand,
        RemoveWorkspaceCommand,
        UpdateWPDevCommand,
        ManageGitAccountsPage,

        AddGitAccountCommand,
        UpdateGitCredentialsCommand,
        RemoveGitAccountCommand,

        FastStartCommand,
        FastRestartCommand,
        FastRebuildCommand,
        FastStopCommand,
        FastShowCommand,
        FastShowMailhogCommand,
        FastShowDatabaseCommand,
        FastShowLogsCommand,
        FastOpenFolderCommand
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