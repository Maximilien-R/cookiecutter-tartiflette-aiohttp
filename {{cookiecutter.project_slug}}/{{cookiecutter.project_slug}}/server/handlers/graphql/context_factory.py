from typing import Any, Dict

from aiohttp import web

__all__ = ("context_factory",)


def context_factory(request: web.Request) -> Dict[str, Any]:
    """Generate and return a context for each GraphQL request.

    :param request: incoming aiohttp request
    :type request: web.Request
    :return: dictionary forwarded as GraphQL context for each request
    :rtype: Dict[str, Any]
    """
    return {"request": request}
