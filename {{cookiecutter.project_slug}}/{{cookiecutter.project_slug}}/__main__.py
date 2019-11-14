import sys

import uvloop

from {{cookiecutter.project_slug}}.server import run_app
from {{cookiecutter.project_slug}}.utils import configure_logging

if __name__ == "__main__":
    configure_logging()
    uvloop.install()
    sys.exit(run_app())
