from uuid import uuid4

import pytest
from first import first
from motor.motor_asyncio import AsyncIOMotorCollection

from webhook_telegram_bot.database.backends.mongo import DatabaseWrapper
from webhook_telegram_bot.database.exceptions import ChatNotFound
from webhook_telegram_bot.database.models import Chat, Service, Webhook


async def test_get_chat_by_chat_id(db_wrapper: DatabaseWrapper):
    chat_id = 1

    with pytest.raises(ChatNotFound):
        await db_wrapper.get_chat_by_chat_id(chat_id)

    collection: AsyncIOMotorCollection = db_wrapper.get_collection('chats')
    await collection.insert_one({'chat_id': chat_id})

    chat = await db_wrapper.get_chat_by_chat_id(chat_id)
    assert isinstance(chat, Chat)
    assert chat.chat_id == chat_id


async def test_get_chat_by_repository_id(db_wrapper: DatabaseWrapper):
    chat_id = 1
    webhook_id = uuid4().hex

    with pytest.raises(ChatNotFound):
        await db_wrapper.get_chat_by_webhook_id(webhook_id)

    collection: AsyncIOMotorCollection = db_wrapper.get_collection('chats')
    await collection.insert_one(
        {
            'chat_id': chat_id,
            'webhooks': [{'webhook_id': webhook_id, 'service': Service.BITBUCKET}],
        }
    )

    chat = await db_wrapper.get_chat_by_webhook_id(webhook_id)
    assert isinstance(chat, Chat)
    assert chat.chat_id == chat_id
    assert first(chat.webhooks).webhook_id == webhook_id


async def test_save_chat(db_wrapper: DatabaseWrapper):
    webhook_id = uuid4().hex
    repository = Webhook(webhook_id=webhook_id, service=Service.BITBUCKET)
    chat_id = 1
    chat = Chat(chat_id=chat_id, webhooks=[repository])

    chat = await db_wrapper.save_chat(chat)
    assert chat.id is not None
    assert chat.chat_id == chat_id
    assert len(chat.webhooks) == 1
    assert first(chat.webhooks).webhook_id == webhook_id
