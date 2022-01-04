from typing import List
from unittest.mock import Mock
from uuid import uuid4

import pytest
from bson import ObjectId
from first import first
from pydantic import ValidationError

from webhook_telegram_bot.database.models import Chat, Webhook


def test_create_chat_model_with_repository():
    webhook_id = uuid4().hex
    chat_id = 1
    webhook = Webhook(webhook_id=webhook_id, service='bitbucket')
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
    webhook = Webhook(webhook_id=webhook_id, service='bitbucket')
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
    webhook = Webhook(webhook_id=webhook_id, service='bitbucket')
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
    webhook = Webhook(webhook_id=webhook_id, service='bitbucket')
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
    webhook = Webhook(webhook_id=webhook_id, service='bitbucket')
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


def test_chat_id_validation():
    Chat(chat_id=1, webhooks=[])
    # Chat(chat_id=ObjectId(b'foo-bar-buzz'), webhooks=[])
    with pytest.raises(ValidationError):
        Chat(chat_id=Mock(), webhooks=[])


def test_webhook_equality():
    webhook_a = Webhook(webhook_id=uuid4().hex, service='bitbucket')
    webhook_b = Webhook(webhook_id=uuid4().hex, service='bitbucket')
    assert webhook_a == webhook_a
    assert webhook_a != webhook_b
    assert webhook_a != Mock()


def test_get_webhook_by_id():
    webhook_b_id = uuid4().hex
    webhook_a = Webhook(webhook_id=uuid4().hex, service='bitbucket')
    webhook_b = Webhook(webhook_id=webhook_b_id, service='bitbucket')
    chat = Chat(chat_id=1, webhooks=[webhook_a, webhook_b])

    webhook = chat.get_webhook_by_id(webhook_b_id)

    assert webhook != webhook_a
    assert webhook == webhook_b


def test_get_webhook_by_id_returns_none():
    chat = Chat(chat_id=1, webhooks=[])

    webhook = chat.get_webhook_by_id(uuid4().hex)

    assert webhook is None


def test_set_webhook_repository_name():
    webhook_a = Webhook(webhook_id=uuid4().hex, service='bitbucket')
    webhook_b = Webhook(webhook_id=uuid4().hex, service='bitbucket')
    chat = Chat(chat_id=1, webhooks=[webhook_a, webhook_b])

    repository_name = uuid4().hex
    chat.set_webhook_repository_name(webhook_b.webhook_id, repository_name)

    webhook = chat.get_webhook_by_id(webhook_b.webhook_id)
    assert webhook.repository_name == repository_name


def test_delete_webhook_by_id():
    webhook_a = Webhook(webhook_id=uuid4().hex, service='bitbucket')
    webhook_b = Webhook(webhook_id=uuid4().hex, service='bitbucket')
    chat = Chat(chat_id=1, webhooks=[webhook_a, webhook_b])

    chat.delete_webhook_by_id(webhook_b.webhook_id)

    assert len(chat.webhooks) == 1
    assert chat.webhooks[0].webhook_id == webhook_a.webhook_id
