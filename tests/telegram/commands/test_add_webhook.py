import json
from typing import Dict, List
from uuid import uuid4

from webhook_telegram_bot.telegram.commands import Command
from webhook_telegram_bot.telegram.commands.add_webhook import (
    add_webhook_command_handler,
)
from webhook_telegram_bot.telegram.telegram_api import TelegramAPI


async def test_add_webhook_command_handler_return_list_services_from_plugins(
    template_engine_mock,
):
    plugin_button_text = uuid4().hex
    plugin_button_command = uuid4().hex
    telegram_api = TelegramAPI("", "")

    resp = await add_webhook_command_handler(
        1,
        telegram_api,
        template_engine_mock,
        [
            [
                {
                    'text': plugin_button_text,
                    'callback_data': plugin_button_command,
                }
            ]
        ],
    )
    assert resp is not None
    assert resp.status == 200

    data = json.loads(resp.text)
    assert data is not None

    inline_keyboard_row = data['reply_markup']['inline_keyboard']

    assert isinstance(inline_keyboard_row, List)
    assert len(inline_keyboard_row) == 2

    service_button = inline_keyboard_row[0][0]
    assert isinstance(service_button, Dict)
    assert service_button['text'] == plugin_button_text
    assert service_button['callback_data'] == plugin_button_command

    go_back_button = inline_keyboard_row[1][0]
    assert isinstance(go_back_button, Dict)
    assert go_back_button['text'] == '🔙 Back'
    assert go_back_button['callback_data'] == Command.START
