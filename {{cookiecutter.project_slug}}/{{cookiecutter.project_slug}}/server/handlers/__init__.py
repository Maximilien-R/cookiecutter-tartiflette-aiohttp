{%- if cookiecutter.add_graphiql_route == "yes" -%}
from .graphiql import handle_graphiql
{% endif -%}
from .graphql import handle_graphql
{%- if cookiecutter.add_health_routes == "yes" %}
from .health import (
    handle_live as handle_health_live,
    handle_ready as handle_health_ready,
)
{%- endif %}

__all__ = (
    "handle_graphql",
    {%- if cookiecutter.add_graphiql_route == "yes" %}
    "handle_graphiql",
    {%- endif %}
    {%- if cookiecutter.add_health_routes == "yes" %}
    "handle_health_live",
    "handle_health_ready",
    {%- endif %}
)
