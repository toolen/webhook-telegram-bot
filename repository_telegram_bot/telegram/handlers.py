"""This file contains Telegram handlers."""
import json
import logging
import uuid

from aiohttp import web
from aiohttp.web_request import Request

from repository_telegram_bot.bitbucket.constants import BITBUCKET_WEBHOOK_ROUTE
from repository_telegram_bot.helpers import (
    get_config_value,
    get_database,
    get_telegram_api,
    get_template_engine,
)

logger = logging.getLogger(__name__)


async def telegram_request_handler(request: Request) -> web.Response:
    """
    Handle Telegram requests.

    :param request:
    :return:
    """
    data = await request.json()

    logger.debug(f'Request from Telegram: {json.dumps(data)}')

    app = request.app
    telegram_api = get_telegram_api(app)
    redis_pool = get_database(app)
    template_engine = get_template_engine(app)

    text = telegram_api.get_text(data)
    chat_id = telegram_api.get_chat_id(data)

    if text == '/start' and chat_id:
        telegram_webhook_host = get_config_value(app, 'TELEGRAM_WEBHOOK_HOST')
        repository_id = uuid.uuid4().hex
        webhook_url = (
            f'{telegram_webhook_host}{BITBUCKET_WEBHOOK_ROUTE}/{repository_id}'
        )

        template = template_engine.get_template('start.html')
        text = template.render(webhook_url=webhook_url)

        await redis_pool.set(repository_id, chat_id)
        return telegram_api.send_message_as_response(
            chat_id=chat_id, text=text, parse_mode='HTML', disable_notification=True
        )
    else:
        return web.Response()
