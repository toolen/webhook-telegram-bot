"""This file contains independent database models."""
from __future__ import annotations

from typing import Any, Callable, Generator, List, Optional, Type, Union

from bson import ObjectId
from pydantic import BaseModel, Field


class PydanticObjectId(ObjectId):  # type: ignore
    """This class provide pydantic compatible representation of ObjectId."""

    @classmethod
    def __get_validators__(
        cls: Type[PydanticObjectId],
    ) -> Generator[Callable[[Any], Any], None, None]:
        """
        Return validators.

        :return:
        """
        yield cls.validate

    @classmethod
    def validate(cls: Type[PydanticObjectId], value: Any) -> Any:
        """
        Validate object.

        :param value:
        :return:
        """
        if not isinstance(value, ObjectId):
            raise TypeError('ObjectId required')
        return value


class Webhook(BaseModel):
    """This class represents webhook object."""

    webhook_id: str
    service: str
    repository_name: Optional[str]

    def __hash__(self) -> int:
        """Return hash."""
        return hash(self.webhook_id)

    def __eq__(self, other: object) -> bool:
        """Return True if objects are equal."""
        if not isinstance(other, Webhook):
            return NotImplemented
        return self.webhook_id == other.webhook_id


class Chat(BaseModel):
    """This class represents chat object."""

    id: Optional[Union[int, PydanticObjectId]] = Field(None, alias='_id')
    chat_id: int
    webhooks: List[Webhook] = []

    class Config:
        """Configuration of chat model."""

        allow_population_by_field_name = True

    def get_webhook_by_id(self, webhook_id: str) -> Optional[Webhook]:
        """
        Return Webhook object by webhook_id.

        :param webhook_id: chat identification string
        :return: Webhook instance or None
        """
        for webhook in self.webhooks:
            if webhook.webhook_id == webhook_id:
                return webhook
        return None

    def set_webhook_repository_name(self, webhook_id: str, name: str) -> None:
        """
        Set webhook repository_name.

        :param webhook_id: chat identification string
        :param name: repository name
        :return: None
        """
        for webhook in self.webhooks:
            if webhook.webhook_id == webhook_id:
                webhook.repository_name = name

    def delete_webhook_by_id(self, webhook_id: str) -> None:
        """
        Exclude webhook from webhooks list by id.

        :param webhook_id: chat identification string
        :return: None
        """
        self.webhooks = list(
            filter(lambda x: x.webhook_id != webhook_id, self.webhooks)
        )
