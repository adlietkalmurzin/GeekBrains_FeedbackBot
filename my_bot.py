from aiogram import types

from aiogram.dispatcher import FSMContext
from configs.bot_configs import bot, dp, main_menu_message
from database.db_session import get_user
from interface.signup import admin_password_waiting, sign_up_student, student_password_waiting
from interface.students_feedback import leave_review
from interface.admin_get_analytics import get_analytics


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    result = get_user(message.from_user.id)

    if result:
        first_name, last_name, user_type = result
        await main_menu_message(message, f"👋Здравствуйте, {first_name} {last_name}", int(user_type))
    else:
        await message.answer("👋Здравствуйте\n\n"
                             "❌<b>Вы ещё не зарегистрированы.</b>\n"
                             "Для продолжения работы пройдите регистрацию")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["👨‍🏫Я админ", "👨‍🎓Я студент"]
        keyboard.add(*buttons)
        await message.answer("❔Вы <b>админ</b> или <b>студент</b>?", reply_markup=keyboard)


@dp.message_handler(text=['👨‍🏫Я админ', '👨‍🎓Я студент'])
async def sign_up(message: types.Message, state: FSMContext):
    if message.text == '👨‍🏫Я админ':
        await admin_password_waiting(message, state)
    elif message.text == '👨‍🎓Я студент':
        await student_password_waiting(message, state)


@dp.message_handler(text=['📊Получить аналитику'])
async def get_report(message: types.Message):
    await get_analytics(message)


@dp.message_handler(text="✏️Оставить отзыв")
async def feedback(message: types.Message, state: FSMContext):
    await leave_review(message, state)