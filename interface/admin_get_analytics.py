import datetime

from aiogram import types

from configs.bot_configs import bot, main_menu_message, dp
from database.db_session import get_table, get_plots


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
    plot_names = ['Отзывы от времени.png', 'Отзывы от времени по процентам.png',
                  'Положительные и отрицательные. Вебинар.png',
                  'Положительные и отрицательные. Вебинар по процентам.png',
                  'Положительные и отрицательные. Программа.png'
        , 'Положительные и отрицательные. Программа по процентам.png', 'Положительные и отрицательные. Препод.png',
                  'Положительные и отрицательные. Препод по процентам.png', "Отриц.png",
                  "Отриц по процентам.png", "Положительные.png", "Положительные по процентами.png", 'чтото.png',
                  'чтото по процентам.png']

    docs = types.MediaGroup()
    docs_1 = types.MediaGroup()
    for k, plot in enumerate(get_plots()):
        doc = types.InputFile(plot, plot_names[k])
        if k <= 9:
            docs.attach_document(doc)
        else:
            docs_1.attach_document(doc)
    await bot.send_media_group(call.message.chat.id, media=docs)
    return await bot.send_media_group(call.message.chat.id, media=docs_1)


@dp.callback_query_handler(text="back_after_get_table_main_menu")
async def back_after_get_table_main_menu(call: types.CallbackQuery):
    await call.message.delete()
    await main_menu_message(call, "Вы вернулись в главное меню", 1)
