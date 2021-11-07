"""This file contains independent database models."""
from enum import Enum
from typing import Any, Callable, Generator, List, Optional, Type, Union

from bson import ObjectId
from pydantic import BaseModel, Field


class PydanticObjectId(ObjectId):
    """This class provide pydantic compatible representation of ObjectId."""

    @classmethod
    def __get_validators__(
        cls: Type['PydanticObjectId'],
    ) -> Generator[Callable[[Any], Any], None, None]:
        """
        Return validators.

        :return:
        """
        yield cls.validate

    @classmethod
    def validate(cls: Type['PydanticObjectId'], value: Any) -> Any:
        """
        Validate object.

        :param value:
        :return:
        """
        if not isinstance(value, ObjectId):
            raise TypeError('ObjectId required')
        return value


class ServiceEnum(str, Enum):
    """This enum represents services that repository can relate to."""

    bitbucket = 'bitbucket'
    # github = 'github'
    # gitlab = 'gitlab'


class Repository(BaseModel):
    """This class represents repository object."""

    repository_id: str
    service: ServiceEnum
    name: Optional[str]

    def __hash__(self) -> int:
        """Return hash."""
        return hash(self.repository_id)

    def __eq__(self, other: object) -> bool:
        """Return True if objects are equal."""
        if not isinstance(other, Repository):
            return NotImplemented
        return self.repository_id == other.repository_id


class Chat(BaseModel):
    """This class represents chat object."""

    id: Optional[Union[int, PydanticObjectId]] = Field(None, alias='_id')
    chat_id: int
    repositories: List[Repository] = []

    class Config:
        """Configuration of chat model."""

        allow_population_by_field_name = True

    # def dict(self, *args, **kwargs):
    #     """
    #     Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
    #
    #     """
    #     # https://github.com/samuelcolvin/pydantic/issues/1090#issuecomment-612882291
    #     self.repositories = list(self.repositories)
    #     result = super().dict(*args, **kwargs)
    #     self.repositories = set(self.repositories)
    #     return result
