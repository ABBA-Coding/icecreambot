import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.config import Config
from tgbot.db.queries import Database


class ACLMiddleware(BaseMiddleware):
    async def setup_chat(self, data: dict, user: types.User):
        db_api: Database = data['db']
        user_loc = await db_api.get_user(username=user.username,
                                         user_id=user.id,
                                         fullname=user.first_name,
                                         user_lang=user.language_code)
        data['user_lang'], data['status'] = user_loc['user_lang'], False

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(data, message.from_user)

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        await self.setup_chat(data, query.from_user)
