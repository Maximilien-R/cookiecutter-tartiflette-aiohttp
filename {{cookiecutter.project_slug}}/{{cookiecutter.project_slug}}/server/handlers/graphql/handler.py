from typing import Any, Dict, Optional

from aiohttp import web
from aiohttp.http_exceptions import HttpBadRequest, HttpProcessingError

from {{cookiecutter.project_slug}}.server.handlers.graphql.context_factory import context_factory
from {{cookiecutter.project_slug}}.server.handlers.graphql.errors import format_error
from {{cookiecutter.project_slug}}.server.handlers.graphql.request_parsers import (
    extract_graphql_params,
)

__all__ = ("handle_graphql",)


def _prepare_response(
    result: Dict[str, Any],
    status: int = 200,
    headers: Optional[Dict[str, Any]] = None,
) -> "aiohttp.web.Response":
    """
    Formats and returns a GraphQL response.
    :param result: result of the GraphQL engine
    :param status: HTTP status code of the response
    :param headers: headers to forward on the response
    :type result: Dict[str, Any]
    :type status: int
    :type headers: Optional[Dict[str, Any]]
    :return: a GraphQL response
    :rtype: aiohttp.web.Response
    """
    response = {"data": result.get("data")}

    errors = result.get("errors")
    if errors is not None:
        response["errors"] = errors

    extensions = result.get("extensions")
    if extensions is not None:
        response["extensions"] = extensions

    return web.json_response(response, status=status, headers=headers)


async def handle_graphql(
    request: "aiohttp.web.Request",
) -> "aiohttp.web.Response":
    """
    GraphQL service response handler.
    :param request: incoming aiohttp request
    :type request: aiohttp.web.Request
    :return: a GraphQL response
    :rtype: aiohttp.web.Response
    :raise HttpBadRequest: if none query was provided
    """
    try:
        query, variables, operation_name = await extract_graphql_params(
            request
        )
        if not query:
            raise HttpBadRequest("Must provide query string.")
        return _prepare_response(
            await request.app["graphql_engine"].execute(
                query,
                operation_name=operation_name,
                variables=variables,
                context=context_factory(request),
            )
        )
    except Exception as e:  # pylint: disable=broad-except
        return _prepare_response(
            {"errors": [format_error(e)]},
            status=(
                e.code  # pylint: disable=no-member
                if isinstance(e, HttpProcessingError)
                and e.code  # pylint: disable=no-member
                else 500
            ),
        )
