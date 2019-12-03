from {{cookiecutter.project_slug}}.server.handlers import (
    {%- if cookiecutter.add_graphiql_route == "yes" %}
    handle_graphiql,
    {%- endif %}
    handle_graphql,
    {%- if cookiecutter.add_health_routes == "yes" %}
    handle_health_live,
    handle_health_ready,
    {%- endif %}
)

__all__ = ("register_routes",)


def register_routes(app: "aiohttp.web.Application") -> None:
    """
    Registers routes into the application.
    :param app: application to which register the routes
    :type app: aiohttp.web.Application
    """
    app.router.add_get("/graphql", handle_graphql)
    app.router.add_post("/graphql", handle_graphql)
    {%- if cookiecutter.add_graphiql_route == "yes" %}
    app.router.add_get("/graphiql", handle_graphiql)
    {%- endif %}
    {%- if cookiecutter.add_health_routes == "yes" %}
    app.router.add_get("/health/live", handle_health_live)
    app.router.add_get("/health/ready", handle_health_ready)
    {%- endif %}
