import json
from typing import Dict, List
from uuid import uuid4

from webhook_telegram_bot.database.models import Chat, Webhook
from webhook_telegram_bot.telegram.commands import Command
from webhook_telegram_bot.telegram.commands.edit_webhooks import (
    edit_webhooks_command_handler,
)
from webhook_telegram_bot.telegram.telegram_api import TelegramAPI

from .utils import get_db_mock, get_template_engine_mock


async def test_edit_webhooks_command_handler_return_list_of_webhooks():
    webhook_id = uuid4().hex
    webhook = Webhook(
        webhook_id=webhook_id, service='bitbucket', repository_name='Test'
    )
    chat = Chat(
        id=1,
        chat_id=1,
        webhooks=[webhook],
    )

    db = get_db_mock(chat)
    telegram_api = TelegramAPI("", "")
    template_engine = get_template_engine_mock()

    resp = await edit_webhooks_command_handler(1, db, telegram_api, template_engine)
    assert resp is not None
    assert resp.status == 200

    data = json.loads(resp.text)
    assert data is not None

    inline_keyboard_row = data['reply_markup']['inline_keyboard']

    assert isinstance(inline_keyboard_row, List)
    assert len(inline_keyboard_row) == 2

    edit_webhook_button = inline_keyboard_row[0][0]
    assert isinstance(edit_webhook_button, Dict)
    assert (
        edit_webhook_button['text'] == f'{webhook.service}: {webhook.repository_name}'
    )
    assert (
        edit_webhook_button['callback_data']
        == f'{Command.EDIT_WEBHOOK}_{webhook.webhook_id}'
    )

    go_back_button = inline_keyboard_row[1][0]
    assert isinstance(go_back_button, Dict)
    assert go_back_button['text'] == '🔙 Back'
    assert go_back_button['callback_data'] == Command.START


async def test_edit_webhooks_command_handler_return_add_webhook_button_if_chat_not_found():
    db = get_db_mock()
    telegram_api = TelegramAPI("", "")
    template_engine = get_template_engine_mock()

    resp = await edit_webhooks_command_handler(1, db, telegram_api, template_engine)
    assert resp is not None
    assert resp.status == 200

    data = json.loads(resp.text)
    assert data is not None

    inline_keyboard_row = data['reply_markup']['inline_keyboard']

    assert isinstance(inline_keyboard_row, List)
    assert len(inline_keyboard_row) == 1

    add_webhook_button = inline_keyboard_row[0][0]
    assert isinstance(add_webhook_button, Dict)
    assert add_webhook_button['text'] == '➕ Add Webhook'
    assert add_webhook_button['callback_data'] == Command.ADD_WEBHOOK
