from aiohttp import web

__all__ = ("handle_ready",)


async def handle_ready(request: web.Request) -> web.Response:
    """Ready service response handler.

    :param request: incoming aiohttp request
    :type request: web.Request
    :return: a 200 status "OK" response
    :rtype: web.Response
    """
    # pylint: disable=unused-argument
    return web.Response(text="OK")
