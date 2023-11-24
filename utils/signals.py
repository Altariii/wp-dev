import signal

from ..commands.exit import bye

def handle_signals() -> None:
    signal.signal(signal.SIGINT, handle_sigint)

def handle_sigint(_, __):
    bye()