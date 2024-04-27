import datetime

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types

from configs.bot_configs import bot, main_menu_message, dp

from configs.models.checking_for_information.checking_for_information import is_informative
from configs.models.assessment_emotionality.assessment_emotionality import assessment_emotionality
from configs.models.identify_object.identify_object import identify_object
from database.db_session import get_table


async def get_analytics(message: types.Message):
    table_send_menu = types.InlineKeyboardMarkup(resize_keyboard=True)
    table_send_menu.add(types.InlineKeyboardButton("Выгрузить таблицу", callback_data="get_table"))
    table_send_menu.add(
        types.InlineKeyboardButton("🏠Вернуться в главное меню", callback_data="back_after_get_table_main_menu"))
    await message.answer("Чтобы получить таблицу с аналитикой, нажмите кнопку ниже", reply_markup=table_send_menu)


@dp.callback_query_handler(text="get_table")
async def send_analytics(call: types.CallbackQuery):
    doc = types.InputFile(get_table(), f'{datetime.datetime.now().date()} отчет.xlsx')
    return await bot.send_document(call.message.chat.id, doc)


@dp.callback_query_handler(text="back_after_get_table_main_menu")
async def back_after_get_table_main_menu(call: types.CallbackQuery):
    await call.message.delete()
    await main_menu_message(call, "Вы вернулись в главное меню", 1)
