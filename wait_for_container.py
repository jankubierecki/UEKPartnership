#!/usr/bin/env python3
import sys
import os
import io
from time import sleep

from compose.cli.main import TopLevelCommand, project_from_options
from contextlib import redirect_stdout

print("outside top")


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


    return "asdasd"


def main():
    print("waiting for containers...", sys.argv[1:])

    for container_name in sys.argv[1:]:
        while get_container_id(container_name) == "":
            print("waiting for: ", container_name)
            sleep(1)

    print("all containers are ready")


print("outside")

if __name__ == "__main__":
    print("inside 1")
    main()
    print("inside 2")
