import shlex
from typing import Dict, List

from communicator import Communicator
from commands.handler import CommandHandler
from commands.new_user import NewUserCommand
from context import ClientContext


class Shell:
    """Manages user interaction with the client."""
    done: bool
    context: ClientContext
    handlers: Dict[str, CommandHandler]

    def __init__(self, host: str, port: int):
        self.done = False
        self.handlers = {}
        self.context = ClientContext(
            communicator=Communicator(host=host, port=port),
        )
        self._register_handlers()

    def _register_handlers(self):
        handler_list: List[CommandHandler] = [
            NewUserCommand(self.context),
        ]

        for handler in handler_list:
            handler.context = self.context
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
                try:
                    handler.run(args)
                except Exception as ex:
                    print(f"{type(ex).__name__} raised.")
                    print(ex)
            else:
                print(f"Unknown command: {cmd_name}")

    def loop(self):
        """Handle user input until the program ends."""
        while not self.done:
            self.read_command(input("> "))
