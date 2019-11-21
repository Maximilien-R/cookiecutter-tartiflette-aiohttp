from tartiflette import Engine
{% if cookiecutter.add_sentry == "yes" %}
from {{cookiecutter.project_slug}}.utils import sentry_error_coercer
{% endif %}
__all__ = ("register_graphql_engine",)

_GRAPHQL_ENGINE: "Engine" = Engine(
    "{{cookiecutter.project_slug}}/graphql/sdl/",
    modules=[
        "{{cookiecutter.project_slug}}.graphql.directives",
        "{{cookiecutter.project_slug}}.graphql.resolvers",
        "{{cookiecutter.project_slug}}.graphql.scalars",
    ],
    {%- if cookiecutter.add_sentry == "yes" %}
    error_coercer=sentry_error_coercer,
    {%- endif %}
)


async def register_graphql_engine(app: "aiohttp.web.Application") -> None:
    """
    Creates a GraphQL engine and register it into the application.
    :param app: application to which register the GraphQL engine
    :type app: aiohttp.web.Application
    """
    await _GRAPHQL_ENGINE.cook()
    app["graphql_engine"] = _GRAPHQL_ENGINE
