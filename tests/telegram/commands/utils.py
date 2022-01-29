from unittest.mock import Mock

from webhook_telegram_bot.database.exceptions import ChatNotFound


def get_db_mock(return_value=None):
    async def get_chat_by_chat_id(chat_id):
        if return_value:
            return return_value
        else:
            raise ChatNotFound()

    async def save_chat(chat):
        return chat

    db = Mock()
    db.get_chat_by_chat_id = get_chat_by_chat_id
    db.save_chat = save_chat
    return db
