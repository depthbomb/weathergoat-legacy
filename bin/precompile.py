from sys import exit
from os import getenv
from pathlib import Path
from py_compile import compile

if not getenv("IN_DOCKER", False):
    print("This script should only be ran while in the Docker container")
    print("If you REALLY know what you are doing and want to run this script outside of Docker, then set the environment variable IN_DOCKER")
    exit(1)

root = Path(".").resolve()
files_to_compile = [root / "main.py"]

[files_to_compile.append(file) for file in (root / "src").glob("**/*.py")]
[compile(str(file), str(file.with_suffix(".pyc")), optimize=2) for file in files_to_compile]
[file.unlink(missing_ok=True) for file in files_to_compile]
