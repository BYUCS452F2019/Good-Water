import sys

from shell import Shell


def main(host: str, port=80):
    shell = Shell(
        host=host,
        port=port,
    )
    shell.loop()


if __name__ == "__main__":
    main(*sys.argv[1:])
