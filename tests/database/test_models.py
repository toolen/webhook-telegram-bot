from typing import List
from uuid import uuid4

from bson import ObjectId
from first import first

from webhook_telegram_bot.database.models import Chat, Service, Webhook


def test_create_chat_model_with_repository():
    webhook_id = uuid4().hex
    chat_id = 1
    webhook = Webhook(webhook_id=webhook_id, service=Service.BITBUCKET)
    chat = Chat(chat_id=chat_id, webhooks=[webhook])
    assert isinstance(chat, Chat)
    assert chat.id is None
    assert chat.chat_id == chat_id
    assert isinstance(chat.webhooks, List)
    assert len(chat.webhooks) == 1
    assert isinstance(first(chat.webhooks), Webhook)
    assert first(chat.webhooks).webhook_id == webhook_id


def test_serialize_chat_model_with_repository_to_dict():
    webhook_id = uuid4().hex
    chat_id = 1
    webhook = Webhook(webhook_id=webhook_id, service=Service.BITBUCKET)
    chat = Chat(chat_id=chat_id, webhooks=[webhook])

    chat_dict = chat.dict()

    assert isinstance(chat_dict, dict)
    assert chat_dict['id'] is None
    assert chat_dict['chat_id'] == chat_id
    assert isinstance(chat_dict['webhooks'], list)
    assert len(chat_dict['webhooks']) == 1
    assert isinstance(first(chat_dict['webhooks']), dict)
    assert first(chat_dict['webhooks'])['webhook_id'] == webhook_id


def test_serialize_chat_model_with_repository_to_json():
    webhook_id = uuid4().hex
    chat_id = 1
    webhook = Webhook(webhook_id=webhook_id, service=Service.BITBUCKET)
    chat = Chat(chat_id=chat_id, webhooks=[webhook])

    chat_json = chat.json()

    assert isinstance(chat_json, str)
    assert '"id": null' in chat_json
    assert f'"chat_id": {chat_id}' in chat_json
    assert (
        f'"webhooks": [{{"webhook_id": "{webhook_id}", "service": "bitbucket", "repository_name": null}}]'
        in chat_json
    )


def test_deserialize_chat_model_with_repository_from_mongo_dict():
    webhook_id = uuid4().hex
    chat_id = 1
    webhook = Webhook(webhook_id=webhook_id, service=Service.BITBUCKET)
    chat = Chat(chat_id=chat_id, webhooks=[webhook])

    chat_dict = chat.dict()
    chat_dict['_id'] = ObjectId()

    chat_parsed = Chat.parse_obj(chat_dict)

    assert isinstance(chat_parsed, Chat)
    assert chat_parsed.id == chat_dict['_id']
    assert chat_parsed.chat_id == chat_id
    assert isinstance(chat_parsed.webhooks, List)
    assert len(chat_parsed.webhooks) == 1
    assert isinstance(first(chat_parsed.webhooks), Webhook)
    assert first(chat_parsed.webhooks).webhook_id == webhook_id


def test_deserialize_chat_model_with_repository_from_rdb_dict():
    webhook_id = uuid4().hex
    chat_id = 1
    webhook = Webhook(webhook_id=webhook_id, service=Service.BITBUCKET)
    chat = Chat(chat_id=chat_id, webhooks=[webhook])

    chat_dict = chat.dict()
    chat_dict['id'] = 1

    chat_parsed = Chat.parse_obj(chat_dict)

    assert isinstance(chat_parsed, Chat)
    assert chat_parsed.id == chat_dict['id']
    assert chat_parsed.chat_id == chat_id
    assert isinstance(chat_parsed.webhooks, List)
    assert len(chat_parsed.webhooks) == 1
    assert isinstance(first(chat_parsed.webhooks), Webhook)
    assert first(chat_parsed.webhooks).webhook_id == webhook_id
