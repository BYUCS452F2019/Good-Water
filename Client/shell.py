class Shell:
    done: bool

    def __init__(self):
        self.done = False

    def read_command(self, cmd: str):
        cmd = cmd.strip()

        if cmd == "exit":
            self.done = True

    def loop(self):
        while not self.done:
            self.read_command(input())
