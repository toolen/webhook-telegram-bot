"""This file contains handlers for common purposes."""
from aiohttp import web
from aiohttp.web_response import Response


async def health_handler(request: web.Request) -> Response:
    """
    Return healthcheck response.

    :return: Response
    """
    return web.json_response({"health": "ok"})
