import shlex
from typing import Dict, List

from commands.handler import CommandHandler
from context import ClientContext


class Shell:
    """Manages user interaction with the client."""
    done: bool
    context: ClientContext
    handlers: Dict[str, CommandHandler]

    def __init__(self):
        self.done = False
        self.handlers = {}
        self.context = ClientContext()

    def _register_handlers(self):
        handler_list: List[CommandHandler] = []

        for handler in handler_list:
            self.handlers[handler.command_name.lower()] = handler

    def read_command(self, cmd: str):
        cmd = cmd.strip()

        if cmd == "":
            return

        args = shlex.split(cmd)
        cmd_name = args[0].lower()

        if cmd_name == "exit":
            self.done = True
        else:
            if cmd_name in self.handlers:
                handler = self.handlers[cmd_name]
                handler.run(args)
            else:
                print(f"Unknown command: {cmd_name}")

    def loop(self):
        """Handle user input until the program ends."""
        while not self.done:
            self.read_command(input("> "))
