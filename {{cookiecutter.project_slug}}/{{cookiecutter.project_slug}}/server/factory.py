from aiohttp import web

from {{cookiecutter.project_slug}}.server.registries import (
    {%- if cookiecutter.mysql_version != "None" %}
    register_database_pool,
    {%- endif %}
    register_graphql_engine,
    register_routes,
)

__all__ = ("create_app",)


def create_app() -> web.Application:
    """Create and setup the application to run.

    :return: the application instance to run
    :rtype: web.Application
    """
    app = web.Application()
    app.on_startup.append(register_graphql_engine)
    {%- if cookiecutter.mysql_version != "None" %}
    app.cleanup_ctx.append(register_database_pool)
    {%- endif %}
    register_routes(app)
    return app
