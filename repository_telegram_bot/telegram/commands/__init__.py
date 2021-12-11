from enum import Enum


class Command(str, Enum):
    """This enum represents bot commands."""

    START = '/start'
    ADD_REPOSITORY = '/add_repository'
    ADD_BITBUCKET_REPOSITORY = '/add_bitbucket_repository'
    EDIT_REPOSITORIES = '/edit_repositories'
    EDIT_REPOSITORY = '/edit_repository'
    DELETE_REPOSITORY = '/delete_repository'
