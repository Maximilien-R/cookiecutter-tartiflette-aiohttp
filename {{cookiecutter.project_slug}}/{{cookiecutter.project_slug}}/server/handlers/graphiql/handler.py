import os

from aiohttp import web

__all__ = ("handle_graphiql",)

_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


def _get_graphiql_template() -> str:
    """
    Returns the GraphiQL HTML template as string.
    :return: GraphiQL HTML template as string
    :rtype: str
    """
    with open(os.path.join(_TEMPLATE_DIR, "graphiql.html")) as template_file:
        return template_file.read()


async def handle_graphiql(
    request: "aiohttp.web.Request",
) -> "aiohttp.web.Response":
    """
    GraphiQL service response handler.
    :param request: incoming aiohttp request
    :type request: aiohttp.web.Request
    :return: a GraphQL response
    :rtype: aiohttp.web.Response
    """
    # pylint: disable=unused-argument
    return web.Response(
        text=_get_graphiql_template(),
        headers={"Content-Type": "text/html"},
    )
