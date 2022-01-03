"""This file contains Bitbucket request handlers."""
import json
import logging
from typing import Optional, cast

from aiohttp import web
from aiohttp.web_request import Request

from webhook_telegram_bot.database.exceptions import ChatNotFound
from webhook_telegram_bot.database.models import Chat, Webhook
from webhook_telegram_bot.helpers import (
    get_database,
    get_telegram_api,
    get_template_engine,
)
from webhook_telegram_bot.plugins.bitbucket.services import BitbucketEventProcessor
from webhook_telegram_bot.utils import deep_get

logger = logging.getLogger(__name__)


async def bitbucket_webhook_handler(request: Request) -> web.Response:
    """
    Process webhook request.

    :param request:
    :return:
    """
    webhook_id = request.match_info.get('webhook_id')
    event_key: Optional[str] = request.headers.get('X-Event-Key')
    if webhook_id and event_key:
        app = request.app
        telegram_api = get_telegram_api(app)
        db = get_database(app)
        template_engine = get_template_engine(app)

        data = await request.json()
        logger.debug(f'{event_key}: {json.dumps(data)}')

        event_processor: BitbucketEventProcessor = BitbucketEventProcessor(
            event_key, data
        )
        template_name, context = event_processor.get_template_name_with_context()

        template = template_engine.get_template(template_name)
        text = template.render(**context)

        try:
            chat: Chat = await db.get_chat_by_webhook_id(webhook_id)
            webhook: Optional[Webhook] = chat.get_webhook_by_id(webhook_id)
            if webhook and not webhook.repository_name:
                # TODO rewrite
                repository_name = cast(
                    str, deep_get(data, 'repository.repository_name')
                )
                chat.set_webhook_repository_name(webhook.webhook_id, repository_name)
                await db.save_chat(chat)

            await telegram_api.send_message(
                chat_id=chat.chat_id,
                text=text,
                parse_mode='HTML',
                disable_web_page_preview=True,
                disable_notification=True,
            )
        except ChatNotFound:
            logger.error(f'Failed to find chat by webhook_id={webhook_id}')

    return web.Response()
