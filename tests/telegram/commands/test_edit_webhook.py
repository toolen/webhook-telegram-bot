import json
from typing import Dict, List
from uuid import uuid4

from webhook_telegram_bot.telegram.commands import Command
from webhook_telegram_bot.telegram.commands.edit_webhook import (
    edit_webhook_command_handler,
)
from webhook_telegram_bot.telegram.telegram_api import TelegramAPI

from .utils import get_template_engine_mock


async def test_edit_webhook_command_handler_return_delete_button():
    webhook_id = uuid4().hex

    telegram_api = TelegramAPI("", "")
    template_engine = get_template_engine_mock()

    resp = await edit_webhook_command_handler(
        1, webhook_id, telegram_api, template_engine
    )
    assert resp is not None
    assert resp.status == 200

    data = json.loads(resp.text)
    assert data is not None

    inline_keyboard_row = data['reply_markup']['inline_keyboard']

    assert isinstance(inline_keyboard_row, List)
    assert len(inline_keyboard_row) == 2

    edit_webhook_button = inline_keyboard_row[0][0]
    assert isinstance(edit_webhook_button, Dict)
    assert edit_webhook_button['text'] == '❌ Delete Webhook'
    assert (
        edit_webhook_button['callback_data'] == f'{Command.DELETE_WEBHOOK}_{webhook_id}'
    )

    go_back_button = inline_keyboard_row[1][0]
    assert isinstance(go_back_button, Dict)
    assert go_back_button['text'] == '🔙 Back'
    assert go_back_button['callback_data'] == Command.EDIT_WEBHOOKS
