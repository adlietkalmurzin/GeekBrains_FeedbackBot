import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types

from configs.bot_configs import bot, main_menu_message, dp

from configs.models.checking_for_information.checking_for_information import is_informative
from configs.models.assessment_emotionality.assessment_emotionality import assessment_emotionality
from configs.models.identify_object.identify_object import identify_object


async def get_analytics(message: types.Message):
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.add("🏠Вернуться в главное меню")
    menu.add("Выгрузить таблицу")
    await message.answer("📊Получить аналитику", reply_markup=back_menu)