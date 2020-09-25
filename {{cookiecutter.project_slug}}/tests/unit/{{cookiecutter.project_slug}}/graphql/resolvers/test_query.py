from unittest.mock import Mock

import pytest

from {{cookiecutter.project_slug}}.graphql.resolvers import resolve_query_hello


@pytest.mark.asyncio
async def test_resolve_query_hello():
    result = await resolve_query_hello(
        None, {"name": "{{cookiecutter.author_name}}"}, {}, Mock()
    )
    assert result == "Hello {{cookiecutter.author_name}}!"
