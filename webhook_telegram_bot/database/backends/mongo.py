"""This file contains BaseDatabaseWrapper implementations for MongoDB."""
from typing import Dict, List, Optional, Union

from motor.core import AgnosticClient
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)
from pymongo.results import InsertOneResult

from webhook_telegram_bot.database.backends.base import BaseDatabaseWrapper
from webhook_telegram_bot.database.exceptions import ChatNotFound
from webhook_telegram_bot.database.models import Chat

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
        """
        Return collection by name.

        :param collection_name:
        :return:
        """
        return self.db[collection_name]

    async def drop_database(self) -> None:
        """Drop database."""
        await self.client.drop_database(self.db.name)

    async def get_chat_by_chat_id(self, chat_id: int) -> Chat:
        """
        Return chat object by id.

        :param chat_id:
        :return:
        """
        document_filter = {'chat_id': chat_id}
        collection: AsyncIOMotorCollection = self.get_collection('chats')
        document: Optional[Document] = await collection.find_one(document_filter)
        if document:
            chat = Chat.parse_obj(document)
            return chat
        else:
            raise ChatNotFound()

    async def get_chat_by_webhook_id(self, webhook_id: str) -> Chat:
        """
        Return chat object by webhook id.

        :param webhook_id:
        :return:
        """
        document_filter = {'webhooks.webhook_id': webhook_id}
        collection: AsyncIOMotorCollection = self.get_collection('chats')
        document: Optional[Document] = await collection.find_one(document_filter)
        if document:
            chat = Chat.parse_obj(document)
            return chat
        else:
            raise ChatNotFound()

    async def save_chat(self, chat: Chat) -> Chat:
        """
        Save chat object to database.

        :param chat:
        :return:
        """
        collection: AsyncIOMotorCollection = self.get_collection('chats')
        chat_as_dict = chat.dict()
        if chat.id:
            del chat_as_dict['id']
            await collection.update_one(
                {'chat_id': chat.chat_id}, {'$set': chat_as_dict}, upsert=True
            )
        else:
            insert_one_result: InsertOneResult = await collection.insert_one(
                chat_as_dict
            )
            chat.id = insert_one_result.inserted_id
        return chat
