import uvloop

from {{cookiecutter.project_slug}}.utils import (
    configure_logging,
    {%- if cookiecutter.add_sentry == "yes" %}
    configure_sentry,
    {%- endif %}
)

configure_logging()
{%- if cookiecutter.add_sentry == "yes" %}
configure_sentry()
{%- endif %}
uvloop.install()
