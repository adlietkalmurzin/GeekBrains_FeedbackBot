import datetime

from aiogram import types

from analytics.analytics import get_all_pn_plot, get_specifically_pn_plot, get_all_obj_all_rew_plot, \
    plot_positive_or_negative_reviews_ratio
from configs.bot_configs import bot, main_menu_message, dp
from database.db_session import get_table


async def get_analytics(message: types.Message):
    table_send_menu = types.InlineKeyboardMarkup(resize_keyboard=True)
    table_send_menu.add(types.InlineKeyboardButton("Выгрузить таблицу", callback_data="get_table"))
    table_send_menu.add(types.InlineKeyboardButton("Выгрузить графики", callback_data="get_graph"))
    table_send_menu.add(
        types.InlineKeyboardButton("🏠Вернуться в главное меню", callback_data="back_after_get_table_main_menu"))
    await message.answer("Чтобы получить таблицу с аналитикой, нажмите кнопку ниже", reply_markup=table_send_menu)


@dp.callback_query_handler(text="get_table")
async def send_analytics(call: types.CallbackQuery):
    doc = types.InputFile(get_table(), f'{datetime.datetime.now().date()} отчет.xlsx')
    return await bot.send_document(call.message.chat.id, doc)


@dp.callback_query_handler(text="get_graph")
async def send_graphs(call: types.CallbackQuery):
    docs = types.MediaGroup()
    docs_1 = types.MediaGroup()
    all_pl = types.InputFile(get_all_pn_plot(), 'Отзывы от времени.png')
    all_pl_percent = types.InputFile(get_all_pn_plot(True), 'Отзывы от времени по процентам.png')
    obj_0 = types.InputFile(get_specifically_pn_plot(0), 'Положительные и отрицательные. Вебинар.png')
    obj_0_percent = types.InputFile(get_specifically_pn_plot(0, True),
                                    'Положительные и отрицательные. Вебинар по процентам.png')
    obj_1 = types.InputFile(get_specifically_pn_plot(1), 'Положительные и отрицательные. Программа.png')
    obj_1_percent = types.InputFile(get_specifically_pn_plot(1, True),
                                    'Положительные и отрицательные. Программа по процентам.png')
    obj_2 = types.InputFile(get_specifically_pn_plot(2), 'Положительные и отрицательные. Препод.png')
    obj_2_percent = types.InputFile(get_specifically_pn_plot(2, True),
                                    'Положительные и отрицательные. Препод по процентам.png')
    all_rew = types.InputFile(get_all_obj_all_rew_plot(), "Все по чему то там.png")
    all_rew_percent = types.InputFile(get_all_obj_all_rew_plot(True), "Все по чему то там по процентам.png")
    ratio = types.InputFile(plot_positive_or_negative_reviews_ratio(), 'чтото.png')
    ratio_percent = types.InputFile(plot_positive_or_negative_reviews_ratio(True), 'чтото по процентам.png')
    docs.attach_document(all_pl)
    docs.attach_document(all_pl_percent)
    docs.attach_document(obj_0)
    docs.attach_document(obj_0_percent)
    docs.attach_document(obj_1)
    docs.attach_document(obj_1_percent)
    docs.attach_document(obj_2)
    docs.attach_document(obj_2_percent)
    docs.attach_document(all_rew)
    docs.attach_document(all_rew_percent)
    docs_1.attach_document(ratio)
    docs_1.attach_document(ratio_percent)
    await bot.send_media_group(call.message.chat.id, media=docs)
    return await bot.send_media_group(call.message.chat.id, media=docs_1)


@dp.callback_query_handler(text="back_after_get_table_main_menu")
async def back_after_get_table_main_menu(call: types.CallbackQuery):
    await call.message.delete()
    await main_menu_message(call, "Вы вернулись в главное меню", 1)
