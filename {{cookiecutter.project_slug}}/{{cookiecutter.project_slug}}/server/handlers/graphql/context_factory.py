from typing import Any, Dict

__all__ = ("context_factory",)


def context_factory(request: "aiohttp.web.Request") -> Dict[str, Any]:
    """
    Generates and returns a context which will be forwarded to each GraphQL
    request.
    :param request: incoming aiohttp request
    :type request: aiohttp.web.Request
    :return: dictionary which will be used as GraphQL context for each request
    :rtype: Dict[str, Any]
    """
    return {"request": request}
