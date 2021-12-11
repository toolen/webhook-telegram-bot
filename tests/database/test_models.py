from typing import List
from uuid import uuid4

from bson import ObjectId
from first import first

from repository_telegram_bot.database.models import Chat, Repository, Service


def test_create_chat_model_with_repository():
    repository_id = uuid4().hex
    chat_id = 1
    repository = Repository(repository_id=repository_id, service=Service.BITBUCKET)
    chat = Chat(chat_id=chat_id, repositories=[repository])
    assert isinstance(chat, Chat)
    assert chat.id is None
    assert chat.chat_id == chat_id
    assert isinstance(chat.repositories, List)
    assert len(chat.repositories) == 1
    assert isinstance(first(chat.repositories), Repository)
    assert first(chat.repositories).repository_id == repository_id


def test_serialize_chat_model_with_repository_to_dict():
    repository_id = uuid4().hex
    chat_id = 1
    repository = Repository(repository_id=repository_id, service=Service.BITBUCKET)
    chat = Chat(chat_id=chat_id, repositories=[repository])

    chat_dict = chat.dict()

    assert isinstance(chat_dict, dict)
    assert chat_dict['id'] is None
    assert chat_dict['chat_id'] == chat_id
    assert isinstance(chat_dict['repositories'], list)
    assert len(chat_dict['repositories']) == 1
    assert isinstance(first(chat_dict['repositories']), dict)
    assert first(chat_dict['repositories'])['repository_id'] == repository_id


def test_serialize_chat_model_with_repository_to_json():
    repository_id = uuid4().hex
    chat_id = 1
    repository = Repository(repository_id=repository_id, service=Service.BITBUCKET)
    chat = Chat(chat_id=chat_id, repositories=[repository])

    chat_json = chat.json()

    assert isinstance(chat_json, str)
    assert '"id": null' in chat_json
    assert f'"chat_id": {chat_id}' in chat_json
    assert (
        f'"repositories": [{{"repository_id": "{repository_id}", "service": "bitbucket", "name": null}}]'
        in chat_json
    )


def test_deserialize_chat_model_with_repository_from_mongo_dict():
    repository_id = uuid4().hex
    chat_id = 1
    repository = Repository(repository_id=repository_id, service=Service.BITBUCKET)
    chat = Chat(chat_id=chat_id, repositories=[repository])

    chat_dict = chat.dict()
    chat_dict['_id'] = ObjectId()

    chat_parsed = Chat.parse_obj(chat_dict)

    assert isinstance(chat_parsed, Chat)
    assert chat_parsed.id == chat_dict['_id']
    assert chat_parsed.chat_id == chat_id
    assert isinstance(chat_parsed.repositories, List)
    assert len(chat_parsed.repositories) == 1
    assert isinstance(first(chat_parsed.repositories), Repository)
    assert first(chat_parsed.repositories).repository_id == repository_id


def test_deserialize_chat_model_with_repository_from_rdb_dict():
    repository_id = uuid4().hex
    chat_id = 1
    repository = Repository(repository_id=repository_id, service=Service.BITBUCKET)
    chat = Chat(chat_id=chat_id, repositories=[repository])

    chat_dict = chat.dict()
    chat_dict['id'] = 1

    chat_parsed = Chat.parse_obj(chat_dict)

    assert isinstance(chat_parsed, Chat)
    assert chat_parsed.id == chat_dict['id']
    assert chat_parsed.chat_id == chat_id
    assert isinstance(chat_parsed.repositories, List)
    assert len(chat_parsed.repositories) == 1
    assert isinstance(first(chat_parsed.repositories), Repository)
    assert first(chat_parsed.repositories).repository_id == repository_id
