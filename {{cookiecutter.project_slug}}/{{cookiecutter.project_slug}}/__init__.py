import uvloop

from {{cookiecutter.project_slug}}.utils import configure_logging

configure_logging()
uvloop.install()
