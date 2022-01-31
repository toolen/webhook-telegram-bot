from webhook_telegram_bot.plugins.bitbucket.services import (
    BitbucketEventProcessor,
    PullRequestEventProcessor,
    RepositoryEventProcessor,
    UnknownEventProcessor,
)


def test_bitbucket_event_processor_detects_event():
    event_processor = BitbucketEventProcessor('repo:action', {})

    assert event_processor._is_repository_event()
    assert not event_processor._is_pull_request_event()


def test_bitbucket_event_processor_returns_event_processor():
    event_processor = BitbucketEventProcessor('repo:action', {})
    concrete_event_processor = event_processor.get_event_processor()
    assert isinstance(concrete_event_processor, RepositoryEventProcessor)

    event_processor = BitbucketEventProcessor('pullrequest:action', {})
    concrete_event_processor = event_processor.get_event_processor()
    assert isinstance(concrete_event_processor, PullRequestEventProcessor)

    event_processor = BitbucketEventProcessor('foobar:action', {})
    concrete_event_processor = event_processor.get_event_processor()
    assert isinstance(concrete_event_processor, UnknownEventProcessor)
