from aiohttp.test_utils import make_mocked_request

from {{cookiecutter.project_slug}}.server.handlers.graphql.context_factory import context_factory


def test_context_factory():
    request = make_mocked_request("GET", "/graphql")
    context = context_factory(request)
    assert context == {"request": request}
