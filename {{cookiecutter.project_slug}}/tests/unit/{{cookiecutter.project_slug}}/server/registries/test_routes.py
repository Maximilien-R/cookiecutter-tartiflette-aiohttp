from unittest.mock import Mock

from {{cookiecutter.project_slug}}.server.handlers import (
    handle_graphql,
    {%- if cookiecutter.add_graphiql_route == "yes" %}
    handle_graphiql,
    {%- endif %}
    {%- if cookiecutter.add_health_routes == "yes" %}
    handle_health_live,
    handle_health_ready,
    {%- endif %}
)
from {{cookiecutter.project_slug}}.server.registries import register_routes


{% set nb_get_routes = 1 %}
{%- if cookiecutter.add_graphiql_route == "yes" -%}
{% set nb_get_routes = nb_get_routes + 1 %}
{%- endif -%}
{%- if cookiecutter.add_health_routes == "yes" -%}
{% set nb_get_routes = nb_get_routes + 2 %}
{%- endif -%}

def test_register_routes():
    app_mock = Mock()

    register_routes(app_mock)

    assert app_mock.router.add_get.call_count == {{nb_get_routes}}
    assert app_mock.router.add_post.call_count == 1
    assert app_mock.router.add_get.any_call("/graphql", handle_graphql)
    assert app_mock.router.add_post.any_call("/graphql", handle_graphql)
    {%- if cookiecutter.add_graphiql_route == "yes" %}
    assert app_mock.router.add_get.any_call("/graphiql", handle_graphiql)
    {%- endif %}
    {%- if cookiecutter.add_health_routes == "yes" %}
    assert app_mock.router.add_get.any_call("/health/live", handle_health_live)
    assert app_mock.router.add_get.any_call(
        "/health/ready", handle_health_ready
    )
    {%- endif %}
