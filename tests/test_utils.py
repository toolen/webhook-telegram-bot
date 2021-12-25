from webhook_telegram_bot.utils import deep_get


def test_deep_get():
    a = {'b': {'c': 'test'}}
    assert deep_get(a, 'b') == {'c': 'test'}
    assert deep_get(a, 'b.c') == 'test'
    assert deep_get(a, 'b.c.d') is None
    assert deep_get(None, 'b') is None
