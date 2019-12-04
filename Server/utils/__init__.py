
import os.path


def relative(current: str, path: str) -> str:
    """find the path relative to the current file rather than the cwd"""
    dirname = os.path.dirname(os.path.abspath(current))
    return os.path.join(dirname, path)
