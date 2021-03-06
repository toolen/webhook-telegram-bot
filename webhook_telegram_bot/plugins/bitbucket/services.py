"""This file contains service classes."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple, Union, cast

from first import first

from webhook_telegram_bot.plugins.bitbucket.constants import (
    BITBUCKET_TEMPLATE_BRANCH_CLOSED,
    BITBUCKET_TEMPLATE_BRANCH_CREATED,
    BITBUCKET_TEMPLATE_BRANCH_UPDATED,
    BITBUCKET_TEMPLATE_PIPELINE_EVENT,
    BITBUCKET_TEMPLATE_PULL_REQUEST_EVENT,
    BITBUCKET_TEMPLATE_UNKNOWN_EVENT,
)
from webhook_telegram_bot.utils import deep_get


class EventProcessor(ABC):
    """This base class for event processors."""

    entity: str
    action: str
    json_data: Dict[str, Any]

    @property
    def actor_display_name(self) -> Optional[str]:
        """
        Return display name of event actor.

        :return: display name of event actor or None
        """
        return cast(str, deep_get(self.json_data, 'actor.display_name'))

    @property
    def repository_name(self) -> Optional[str]:
        """
        Return repository name.

        :return: repository name or None
        """
        return cast(str, deep_get(self.json_data, 'repository.name'))

    @property
    def repository_href(self) -> Optional[str]:
        """
        Return repository href.

        :return: repository href or None
        """
        return cast(str, deep_get(self.json_data, 'repository.links.html.href'))

    @abstractmethod
    def get_template_name_with_context(
        self,
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Return template name with render context.

        :return: tuple of template name and render context
        """
        pass


class RepositoryEventProcessor(EventProcessor):
    """This class process repository events."""

    def __init__(self, entity: str, action: str, json_data: Dict[str, Any]) -> None:
        """
        Construct RepositoryEventProcessor class.

        :param entity: subject of webhook event
        :param action: action with subject of webhook event
        :param json_data: JSON of webhook event
        :return: None
        """
        self.entity = entity
        self.action = action
        self.json_data = json_data

    @property
    def changes(self) -> Optional[Dict[str, Any]]:
        """
        Return dict of changes.

        :return: dict of changes or None
        """
        changes = deep_get(self.json_data, 'push.changes') or []
        return first(changes)

    @property
    def branch_name(self) -> Optional[str]:
        """
        Return branch name.

        :return: branch name or None
        """
        return cast(
            str,
            deep_get(self.changes, 'new.name') or deep_get(self.changes, 'old.name'),
        )

    @property
    def branch_href(self) -> Optional[str]:
        """
        Return hyperlink to branch.

        :return: branch href or None
        """
        return cast(
            str,
            deep_get(self.changes, 'links.html.href')
            or deep_get(self.changes, 'old.links.html.href'),
        )

    @property
    def is_created(self) -> Optional[bool]:
        """
        Return True if branch was created.

        :return: True if branch was created, False if not, None if failed to get
        """
        return cast(bool, deep_get(self.changes, 'created'))

    @property
    def is_closed(self) -> Optional[bool]:
        """
        Return True if branch was closed.

        :return: True if branch was closed, False if not, None if failed to get
        """
        return cast(bool, deep_get(self.changes, 'closed'))

    @property
    def pipeline_title(self) -> Optional[str]:
        """
        Return pipeline title.

        :return: pipeline title or None
        """
        return cast(str, deep_get(self.json_data, 'commit_status.name'))

    @property
    def pipeline_state(self) -> Optional[str]:
        """
        Return pipeline state.

        :return: pipeline state: 'STARTED', 'FINISHED', 'FAILED' or None
        """
        state = cast(str, deep_get(self.json_data, 'commit_status.state'))
        if state == 'INPROGRESS':
            return 'STARTED'
        elif state == 'SUCCESSFUL':
            return 'FINISHED'
        else:
            return state

    @property
    def pipeline_href(self) -> Optional[str]:
        """
        Return href to pipeline.

        :return: href to pipeline or None
        """
        return cast(str, deep_get(self.json_data, 'commit_status.url'))

    @property
    def number_of_commits(self) -> Tuple[int, bool]:
        """
        Return a tuple of number of commits and bool determines whether there were more than 5 commits.

        :return: tuple of number of commits and bool determines whether there were more than 5 commits.
        """
        changes = self.changes or {}
        return len(changes.get('commits', [])), cast(
            bool, deep_get(self.changes, 'truncated')
        )

    def get_commit_description(self, commit: Dict[str, Any]) -> Optional[str]:
        """
        Return commit description.

        :param commit: dictionary of information about commit
        :return: commit description
        """
        description = cast(str, deep_get(commit, 'summary.raw'))
        return description.strip() if description else description

    def get_commit_href(self, commit: Dict[str, Any]) -> Optional[str]:
        """
        Return hyperlink to comment.

        :param commit: dictionary of information about commit
        :return: commit href
        """
        return cast(str, deep_get(commit, 'links.html.href'))

    def get_context(self) -> Dict[str, Any]:
        """
        Return render context.

        :return: render context
        """
        number_of_commits, is_number_of_commits_truncated = self.number_of_commits
        return {
            'repository_name': self.repository_name,
            'actor_display_name': self.actor_display_name,
            'action': self.action,
            'number_of_commits': number_of_commits,
            'is_number_of_commits_truncated': is_number_of_commits_truncated,
            'branch_name': self.branch_name,
            'branch_href': self.branch_href,
            'pipeline_title': self.pipeline_title,
            'pipeline_state': self.pipeline_state,
            'pipeline_href': self.pipeline_href,
        }

    def get_template_name_with_context(
        self,
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Return template name with render context.

        :return: tuple of template name with render context.
        """
        context = self.get_context()
        if self.action == 'push':
            template_name = BITBUCKET_TEMPLATE_BRANCH_UPDATED
            if self.is_created:
                template_name = BITBUCKET_TEMPLATE_BRANCH_CREATED
            if self.is_closed:
                template_name = BITBUCKET_TEMPLATE_BRANCH_CLOSED
        elif self.action in ('commit_status_created', 'commit_status_updated'):
            template_name = BITBUCKET_TEMPLATE_PIPELINE_EVENT
        else:
            context['event'] = f'{self.entity}:{self.action}'
            context['webhook_settings_href'] = f'{self.repository_href}/admin/webhooks'
            template_name = BITBUCKET_TEMPLATE_UNKNOWN_EVENT
        return template_name, context


class PullRequestEventProcessor(EventProcessor):
    """This class process pull request events."""

    def __init__(self, entity: str, action: str, json_data: Dict[str, Any]) -> None:
        """
        Construct PullRequestEventProcessor class.

        :param entity: subject of webhook event
        :param action: action with subject of webhook event
        :param json_data: JSON of webhook event
        :return: None
        """
        self.entity = entity
        self.action = action
        self.json_data = json_data

    @property
    def pull_request_id(self) -> Optional[int]:
        """
        Return pull request id.

        :return: pull request id or None
        """
        return cast(int, deep_get(self.json_data, 'pullrequest.id'))

    @property
    def pull_request_title(self) -> Optional[str]:
        """
        Return pull request title.

        :return: pull request title or None
        """
        return cast(str, deep_get(self.json_data, 'pullrequest.title'))

    @property
    def pull_request_href(self) -> Optional[str]:
        """
        Return hyperlink to pull request.

        :return: href to pull request or None
        """
        return cast(str, deep_get(self.json_data, 'pullrequest.links.html.href'))

    def get_context(self) -> Dict[str, Any]:
        """
        Return render context.

        :return: render context
        """
        return {
            'repository_name': self.repository_name,
            'actor_display_name': self.actor_display_name,
            'action': self.action,
            'pull_request_id': self.pull_request_id,
            'pull_request_href': self.pull_request_href,
            'pull_request_title': self.pull_request_title,
        }

    def get_template_name_with_context(
        self,
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Return template name with render context.

        :return: tuple of template name and render context.
        """
        return BITBUCKET_TEMPLATE_PULL_REQUEST_EVENT, self.get_context()


class UnknownEventProcessor(EventProcessor):
    """This class process unknown events."""

    def __init__(self, entity: str, action: str, json_data: Dict[str, Any]) -> None:
        """
        Construct UnknownEventProcessor class.

        :param entity: subject of webhook event
        :param action: action with subject of webhook event
        :param json_data: JSON of webhook event
        :return: None
        """
        self.entity = entity
        self.action = action
        self.json_data = json_data

    def get_template_name_with_context(self) -> Tuple[str, Dict[str, Any]]:
        """
        Return template name with render context.

        :return: tuple of template name and render context
        """
        return BITBUCKET_TEMPLATE_UNKNOWN_EVENT, {
            'repository_name': self.repository_name,
            'event': f'{self.entity}:{self.action}',
        }


class BitbucketEventProcessor:
    """This class process json from Bitbucket hook."""

    def __init__(self, event_key: str, json_data: Dict[str, Any]) -> None:
        """
        Construct BitbucketEventProcessor class.

        :param event_key: subject and action of webhook event delimited by ":"
        :param json_data: JSON of webhook event
        :return: None
        """
        self.entity, self.action = event_key.split(':')
        self.json_data = json_data

    def _is_repository_event(self) -> bool:
        """
        Return True if event come from repository.

        :return: True if event come from repository.
        """
        return self.entity == 'repo'

    def _is_pull_request_event(self) -> bool:
        """
        Return True if event come from pull request.

        :return: True if event come from pull request.
        """
        return self.entity == 'pullrequest'

    def get_event_processor(
        self,
    ) -> Union[
        UnknownEventProcessor, RepositoryEventProcessor, PullRequestEventProcessor
    ]:
        """
        Return event processor instance.

        :return: event processor instance.
        """
        constructor_args = (self.entity, self.action, self.json_data)
        if self._is_repository_event():
            return RepositoryEventProcessor(*constructor_args)
        elif self._is_pull_request_event():
            return PullRequestEventProcessor(*constructor_args)
        else:
            return UnknownEventProcessor(*constructor_args)

    def get_template_name_with_context(
        self,
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Return template name with render context.

        :return: tuple of template name and render context.
        """
        event_processor = self.get_event_processor()
        return event_processor.get_template_name_with_context()
