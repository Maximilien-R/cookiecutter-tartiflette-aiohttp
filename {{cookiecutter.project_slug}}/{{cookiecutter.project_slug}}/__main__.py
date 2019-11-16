import sys

from {{cookiecutter.project_slug}}.server import run_app

if __name__ == "__main__":
    sys.exit(run_app())
