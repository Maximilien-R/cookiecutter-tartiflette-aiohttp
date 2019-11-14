from aiohttp import web

__all__ = ("handle_live",)


async def handle_live(
    request: "aiohttp.web.Request",
) -> "aiohttp.web.Response":
    """
    Live service response handler.
    :param request: incoming aiohttp request
    :type request: aiohttp.web.Request
    :return: a 200 status "OK" response
    :rtype: aiohttp.web.Response
    """
    # pylint: disable=unused-argument
    return web.Response(text="OK")
