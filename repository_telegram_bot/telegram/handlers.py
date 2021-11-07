"""This file contains Telegram handlers."""
import json
import logging
import uuid
from typing import Optional

from aiohttp import web
from aiohttp.web_request import Request

from repository_telegram_bot.bitbucket.constants import BITBUCKET_WEBHOOK_ROUTE
from repository_telegram_bot.database.exceptions import ChatNotFound
from repository_telegram_bot.database.models import Chat, Repository, ServiceEnum
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
    db = get_database(app)
    template_engine = get_template_engine(app)

    text: Optional[str] = telegram_api.get_text(data)
    chat_id: Optional[int] = telegram_api.get_chat_id(data)

    if not text or not chat_id:
        raise Exception()

    if text == '/start':
        template = template_engine.get_template('start.html')
        text = template.render()
        return telegram_api.send_message_as_response(
            chat_id=chat_id,
            text=text,
            parse_mode='HTML',
            disable_notification=True,
            reply_markup={
                'inline_keyboard': [
                    [{'text': '➕ Add Repository', 'callback_data': '/add_repository'}]
                ]
            },
        )

    elif text == '/add_repository':
        template = template_engine.get_template('select_service.html')
        text = template.render()
        return telegram_api.send_message_as_response(
            chat_id=chat_id,
            text=text,
            parse_mode='HTML',
            disable_notification=True,
            reply_markup={
                'inline_keyboard': [
                    [{'text': 'Bitbucket', 'callback_data': '/bitbucket'}]
                ]
            },
        )

    elif text == '/bitbucket':
        telegram_webhook_host = get_config_value(app, 'TELEGRAM_WEBHOOK_HOST')
        repository_id: str = uuid.uuid4().hex
        repository: Repository = Repository(
            repository_id=repository_id, service=ServiceEnum.bitbucket
        )

        try:
            chat = await db.get_chat_by_chat_id(chat_id)
            chat.repositories.append(repository)
            await db.save_chat(chat)
        except ChatNotFound:
            chat = Chat(chat_id=chat_id, repositories=[repository])
            await db.save_chat(chat)

        template = template_engine.get_template('bitbucket/start.html')
        text = template.render(
            webhook_url=f'{telegram_webhook_host}{BITBUCKET_WEBHOOK_ROUTE}/{repository_id}'
        )
        return telegram_api.send_message_as_response(
            chat_id=chat_id, text=text, parse_mode='HTML', disable_notification=True
        )

    else:
        return web.Response()
