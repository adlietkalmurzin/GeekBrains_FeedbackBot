from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from configs.bot_token import token

bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

READYNESS_THRESHOLD = 3
RELEVANT_SCORE_THRESHOLD = 3
admin_password = "1234"


async def main_menu_message(message, message_text: str, user_type: int):
    """
    Отправляет главное меню
    :param message: сообщение от пользователя
    :param message_text: текст сообщения
    :param user_type: 0 - студент, 1 - админ
    """

    if user_type == 0:
        main_students_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Оставить отзыв"]
        main_students_menu.add(*buttons)
        await bot.send_message(message.from_user.id, message_text, reply_markup=main_students_menu)
    elif user_type == 1:
        main_teachers_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["📊Получить аналитику"]
        main_teachers_menu.add(*buttons)
        await bot.send_message(message.from_user.id, message_text, reply_markup=main_teachers_menu)
