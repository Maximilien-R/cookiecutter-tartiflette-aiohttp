from unittest.mock import Mock

from {{cookiecutter.project_slug}}.server.handlers import (
    handle_graphql,
    {%- if cookiecutter.add_health_routes == "yes" %}
    handle_health_live,
    handle_health_ready,
    {%- endif %}
)
from {{cookiecutter.project_slug}}.server.registries import register_routes


def test_register_routes():
    app_mock = Mock()

    register_routes(app_mock)

    {%- if cookiecutter.add_health_routes == "yes" %}
    assert app_mock.router.add_get.call_count == 3
    {%- else %}
    assert app_mock.router.add_get.call_count == 1
    {%- endif %}
    assert app_mock.router.add_post.call_count == 1
    assert app_mock.router.add_get.any_call("/graphql", handle_graphql)
    assert app_mock.router.add_post.any_call("/graphql", handle_graphql)
    {%- if cookiecutter.add_health_routes == "yes" %}
    assert app_mock.router.add_get.any_call("/health/live", handle_health_live)
    assert app_mock.router.add_get.any_call(
        "/health/ready", handle_health_ready
    )
    {%- endif %}
