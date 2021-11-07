"""This file contains TelegramAPI class."""
import json
import logging
from typing import Any, Dict, List, Optional, Union, cast

import aiohttp
from aiohttp import web

from repository_telegram_bot.utils import deep_get

logger = logging.getLogger(__name__)


class TelegramAPI:
    """This class helps with Telegram API."""

    def __init__(
        self, telegram_api_endpoint: str, token: str, disable_notification: bool = True
    ) -> None:
        """
        Construct TelegramAPI class.

        :param telegram_api_endpoint:
        :param token:
        :param disable_notification:
        """
        self.telegram_api_endpoint = telegram_api_endpoint
        self.token = token
        self.disable_notification = disable_notification
        self.active = False

    async def command(self, command: str, payload: Dict[str, Any]) -> None:
        """
        Send command to Telegram API.

        :param command:
        :param payload:
        :return:
        """
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            url = f'{self.telegram_api_endpoint}/bot{self.token}/{command}'
            async with session.post(url, json=payload, headers=headers) as response:
                data = await response.json()
                logger.debug(f'Telegram response: {json.dumps(data)}')

    async def set_webhook(self, url_webhook: str) -> None:
        """
        Set webhook.

        :param url_webhook:
        :return:
        """
        await self.command('setWebhook', {'url': url_webhook})
        self.active = True

    async def delete_webhook(self) -> None:
        """
        Delete webhook.

        :return:
        """
        await self.command('setWebhook', {'url': ''})
        self.active = False

    async def send_message(self, **kwargs: Union[str, int, bool]) -> None:
        """
        Send text message.

        :param kwargs:
            chat_id
            text
        :return:
        """
        await self.command('sendMessage', kwargs)

    @staticmethod
    def send_message_as_response(
        **kwargs: Union[
            str, int, bool, Dict[str, str], Dict[str, List[List[Dict[str, str]]]]
        ]
    ) -> web.Response:
        """
        Send text message as response.

        :param kwargs:
        :return:
        """
        return web.json_response({'method': 'sendMessage', **kwargs})

    @staticmethod
    def get_text(data: Dict[str, Any]) -> Optional[str]:
        """
        Return text from Telegram request.

        :param data:
        :return:
        """
        return cast(
            str, deep_get(data, 'message.text') or deep_get(data, 'callback_query.data')
        )

    @staticmethod
    def get_chat_id(data: Dict[str, Any]) -> Optional[int]:
        """
        Return chat id from Telegram request.

        :param data:
        :return:
        """
        chat_id = deep_get(data, 'message.chat.id') or deep_get(
            data, 'callback_query.message.chat.id'
        )
        return cast(int, chat_id)
