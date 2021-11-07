"""This file contains BaseDatabaseWrapper implementations for MongoDB."""
from typing import Dict, List, Optional, Union

from motor.core import AgnosticClient
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)
from pymongo.results import InsertOneResult

from repository_telegram_bot.database.backends.base import BaseDatabaseWrapper
from repository_telegram_bot.database.exceptions import ChatNotFound
from repository_telegram_bot.database.models import Chat

Document = Dict[str, Union[int, str, List[Dict[str, str]]]]


class DatabaseWrapper(BaseDatabaseWrapper):
    """This class implements BaseDatabaseWrapper for MongoDB."""

    def __init__(self, url: str):
        """Construct DatabaseWrapper class."""
        self.client: AgnosticClient = AsyncIOMotorClient(url)
        self.db: AsyncIOMotorDatabase = self.client.get_default_database()
        self.closed = False

    def close(self) -> None:
        """Close database connection."""
        self.client.close()
        self.closed = True

    def get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        """Return collection by name."""
        return self.db[collection_name]

    async def drop_database(self) -> None:
        """Drop database."""
        await self.client.drop_database(self.db.name)

    # async def get_or_create_chat(self, chat: Chat) -> Tuple[Chat, bool]:
    #     created = False
    #     document_filter = {'chat_id': chat.chat_id}
    #     collection: AsyncIOMotorCollection = self.get_collection('chats')
    #     document: Optional[Dict] = await collection.find_one(document_filter)
    #     repository_as_dict = first(chat.repositories).dict()
    #     if document:
    #         if not document['repositories']:
    #             document['repositories'] = []
    #         document['repositories'].append(repository_as_dict)
    #         await collection.update_one(document_filter, document)
    #     else:
    #         chat_as_dict = chat.dict()
    #         insert_one_result: InsertOneResult = await collection.insert_one(chat_as_dict)
    #         chat_as_dict.update({'_id': insert_one_result.inserted_id})
    #         document = chat_as_dict
    #         created = True
    #     chat = Chat.parse_obj(document)
    #     return chat, created

    async def get_chat_by_chat_id(self, chat_id: int) -> Chat:
        """Return chat object by id."""
        document_filter = {'chat_id': chat_id}
        collection: AsyncIOMotorCollection = self.get_collection('chats')
        document: Optional[Document] = await collection.find_one(document_filter)
        if document:
            chat = Chat.parse_obj(document)
            return chat
        else:
            raise ChatNotFound()

    async def get_chat_by_repository_id(self, repository_id: str) -> Chat:
        """Return chat object by repository id."""
        document_filter = {'repositories.repository_id': repository_id}
        collection: AsyncIOMotorCollection = self.get_collection('chats')
        document: Optional[Document] = await collection.find_one(document_filter)
        if document:
            chat = Chat.parse_obj(document)
            return chat
        else:
            raise ChatNotFound()

    async def save_chat(self, chat: Chat) -> Chat:
        """Save chat object to database."""
        collection: AsyncIOMotorCollection = self.get_collection('chats')
        chat_as_dict = chat.dict()
        if chat.id:
            del chat_as_dict['id']
            await collection.update_one({'chat_id': chat.chat_id}, chat_as_dict)
        else:
            insert_one_result: InsertOneResult = await collection.insert_one(
                chat_as_dict
            )
            chat.id = insert_one_result.inserted_id
        return chat

    # async def save_chat(self, chat: Chat) -> Chat:
    #     collection: AsyncIOMotorCollection = self.get_collection('chats')
    #     document = chat.dict()
    #     _id = document.get('_id')
    #     if _id:
    #         result: UpdateResult = await collection.replace_one({'_id': _id}, document)
    #     else:
    #         result: InsertOneResult = await collection.insert_one(document)
    #         chat.id = result.inserted_id
    #     return chat
