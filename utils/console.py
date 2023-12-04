import os
import subprocess

from ..config.config import version

class colors:
    WHITE       = "\033[97m"
    BLACK       = "\033[30m\033[1m"
    YELLOW      = "\033[93m"
    ORANGE      = "\033[38;5;208m"
    BLUE        = "\033[34m"
    LBLUE       = "\033[36m"
    GREEN       = "\033[92m"
    FGREEN      = "\033[32m"
    RED         = "\033[91m"
    MAGENTA     = "\033[35m"
    GREY        = "\033[37m"
    CYAN        = "\033[36m"
    BLACK_BG    = "\033[100m"
    WHITE_BG    = "\033[107m"
    BLUE_BG     = "\033[44m"
    LBLUE_BG    = "\033[106m"
    GREEN_BG    = "\033[42m"
    LGREEN_BG   = "\033[102m"
    YELLOW_BG   = "\033[43m"
    LYELLOW_BG  = "\033[103m"
    VIOLET_BG   = "\033[48;5;129m"
    RED_BG      = "\033[101m"
    BOLD        = "\033[1m"
    ENDC        = "\033[0m"


class display:

    # ? MESSAGE TYPES
    def statement(msg: str) -> None:
        print("[+] " + msg)

    def error(msg: str) -> None:
        print(colors.BOLD + colors.RED + "[x] " + msg + colors.ENDC)

    def warning(msg: str) -> None:
        print(colors.BOLD + colors.YELLOW + "[!] " + colors.ENDC + msg)

    def description(msg: str) -> None:
        print(colors.WHITE_BG + colors.BLACK + colors.BOLD + " [+]  " + msg + "  [+] " + colors.ENDC + "\n")

    def info(msg: str) -> None:
        print(colors.BOLD + colors.LBLUE + "[i] " + colors.ENDC + msg)

    def download_info(msg: str) -> None:
        print(colors.BOLD + colors.FGREEN + '[↓] ' + colors.ENDC + msg)

    def success(msg: str) -> None:
        print(colors.BOLD + colors.FGREEN + "[*] " + colors.ENDC + msg)


    def result(stm: str, msg: str) -> None:
        try: print(colors.BOLD + colors.FGREEN + "[✓] " + stm + colors.ENDC + msg)
        except UnicodeEncodeError:
            print(colors.BOLD + colors.FGREEN + "[>] " + stm + colors.ENDC + msg)

    def request(msg: str) -> str:
        return input("[" + colors.CYAN + "#" + colors.ENDC + "] " + msg + ": ")

    def banner():
        print(colors.BOLD + colors.GREEN + """
__    __    __  ______             _____    ____   __    __
\ \  /  \  / /  |  _  \           |  _  \  | ___|  \ \  / /
 \ \/ /\ \/ /   | |_| |   _____   | | | |  | \      \ \/ /  {0}by {1}@Altariii{2}
  \  /  \  /    |  ___/  |_____|  | |_| |  | /__     \  /   {3}Version {4}{5}{2}
   \/    \/     |_|               |_____/  |____|     \/{6}
""".format(colors.ORANGE, colors.RED, colors.GREEN, colors.YELLOW, colors.CYAN, version(), colors.ENDC))
        print("\n")

    # ? Actions
    def clear() -> None:
        if os.name == 'nt': os.system('cls')
        else: os.system('clear')

def run_command(command: str, path: str, show_output: bool = True, input: str = '') -> str:
    if show_output:
        result = subprocess.run([word for word in command.split()], cwd=path, input=input.encode())
        return ""
    else:
        result = subprocess.run([word for word in command.split()], cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=input.encode())

    stdout_str = result.stdout.decode('utf-8')

    if result.returncode != 0:
        print(f"Command failed with return code {result.returncode}. Error message: {result.stderr.decode('utf-8')}")

    return stdout_str

def run_commands(commands: list[str], path: str, show_output: bool = True, input: str = '') -> None:
    for command in commands:
        run_command(command, path, show_output, input)