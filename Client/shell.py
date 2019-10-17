import shlex


class Shell:
    done: bool

    def __init__(self):
        self.done = False

    def read_command(self, cmd: str):
        cmd = cmd.strip()
        args = shlex.split(cmd)

        if args == ["exit"]:
            self.done = True

    def loop(self):
        while not self.done:
            self.read_command(input())
