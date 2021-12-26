from uuid import uuid4

import pytest
from first import first
from motor.motor_asyncio import AsyncIOMotorCollection

from webhook_telegram_bot.database.backends.types import DatabaseWrapperImpl
from webhook_telegram_bot.database.exceptions import ChatNotFound
from webhook_telegram_bot.database.models import Chat, Service, Webhook


async def test_get_chat_by_chat_id(db_wrapper: DatabaseWrapperImpl):
    chat_id = 1

    with pytest.raises(ChatNotFound):
        await db_wrapper.get_chat_by_chat_id(chat_id)

    collection: AsyncIOMotorCollection = db_wrapper.get_collection('chats')
    await collection.insert_one({'chat_id': chat_id})

    chat = await db_wrapper.get_chat_by_chat_id(chat_id)
    assert isinstance(chat, Chat)
    assert chat.chat_id == chat_id


async def test_get_chat_by_repository_id(db_wrapper: DatabaseWrapperImpl):
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


async def test_save_chat(db_wrapper: DatabaseWrapperImpl):
    webhook_id = uuid4().hex
    webhook = Webhook(webhook_id=webhook_id, service=Service.BITBUCKET)
    chat_id = 1
    chat = Chat(chat_id=chat_id, webhooks=[webhook])

    chat = await db_wrapper.save_chat(chat)
    assert chat.id is not None
    assert chat.chat_id == chat_id
    assert len(chat.webhooks) == 1
    assert first(chat.webhooks).webhook_id == webhook_id


async def test_update_chat(db_wrapper: DatabaseWrapperImpl):
    webhook_id = uuid4().hex
    webhook = Webhook(webhook_id=webhook_id, service=Service.BITBUCKET)
    chat_id = 1
    chat = Chat(chat_id=chat_id, webhooks=[webhook])

    created_chat = await db_wrapper.save_chat(chat)
    created_chat_id = created_chat.id

    another_webhook_id = uuid4().hex
    another_webhook = Webhook(webhook_id=another_webhook_id, service=Service.BITBUCKET)
    created_chat.webhooks.append(another_webhook)
    updated_chat = await db_wrapper.save_chat(created_chat)

    assert created_chat_id == updated_chat.id
    assert len(updated_chat.webhooks) == 2
