#!/usr/bin/env python3
import sys
import os
import io
from time import sleep

from compose.cli.main import TopLevelCommand, project_from_options
from contextlib import redirect_stdout


def get_container_id(container_name):
    options = {
        "--quiet": True,
        "--filter": "status=running",
        "nginx": True,
        "--services": False,
        "SERVICE": [container_name],
    }

    project = project_from_options(os.path.dirname(os.path.abspath(__file__)), options)
    cmd = TopLevelCommand(project)
    result = io.StringIO()

    with redirect_stdout(result):
        cmd.ps(options)

    return result.getvalue()


def main():
    print("Waiting for containers ", sys.argv[1:])

    for container_name in sys.argv[1:]:
        tries_left = 30
        while get_container_id(container_name) == "" and tries_left > 0:
            print("Waiting for: ", container_name)
            tries_left -= 1
            sleep(1)

    print("All containers are ready")


if __name__ == "__main__":
    main()
