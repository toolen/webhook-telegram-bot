"""This file contains Bitbucket request handlers."""
import json
import logging
from typing import Optional, cast

from aiohttp import web
from aiohttp.web_request import Request

from repository_telegram_bot.bitbucket.services import BitbucketEventProcessor
from repository_telegram_bot.database.exceptions import ChatNotFound
from repository_telegram_bot.database.models import Chat, Repository
from repository_telegram_bot.helpers import (
    get_database,
    get_telegram_api,
    get_template_engine,
)
from repository_telegram_bot.utils import deep_get

logger = logging.getLogger(__name__)


async def bitbucket_webhook_handler(request: Request) -> web.Response:
    """
    Process webhook request.

    :param request:
    :return:
    """
    repository_id = request.match_info.get('repository_id')
    event_key: Optional[str] = request.headers.get('X-Event-Key')
    if repository_id and event_key:
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
            chat: Chat = await db.get_chat_by_repository_id(repository_id)
            repository: Optional[Repository] = chat.get_repository_by_id(repository_id)
            if repository and not repository.name:
                # TODO rewrite
                repository_name = cast(str, deep_get(data, 'repository.name'))
                chat.set_repository_name(repository.repository_id, repository_name)
                await db.save_chat(chat)

            await telegram_api.send_message(
                chat_id=chat.chat_id,
                text=text,
                parse_mode='HTML',
                disable_web_page_preview=True,
                disable_notification=True,
            )
        except ChatNotFound:
            logger.error(f'Couldn\'t find chat by repository_id={repository_id}')

    return web.Response()


async def bitbucket_debug_template_handler(request: Request) -> web.Response:
    """
    Debug templates.

    :param request:
    :return:
    """
    app = request.app
    template_engine = get_template_engine(app)
    template_name = request.match_info.get('template_name')
    template = template_engine.get_template(f'bitbucket/{template_name}.html')
    text = template.render(
        {
            'repository_name': 'btb-test-repo',
            'actor_display_name': 'Dmitrii Zakharov',
            'action': 'push',
            'number_of_commits': 1,
            'branch_name': 'ch/new-branch',
            'branch_href': '#',
            'is_created': True,
        }
    )
    return web.Response(text=text)
