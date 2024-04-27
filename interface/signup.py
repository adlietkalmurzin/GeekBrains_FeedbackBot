import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from configs.bot_configs import dp, main_menu_message, admin_password
from database.db_session import send_user_to_base


class SignUpAdmin(StatesGroup):
    password = State()
    name = State()


class SignUpStudent(StatesGroup):
    name = State()


async def admin_password_waiting(message: types.Message, state: FSMContext):
    await message.answer("🔐<b>Подтвердите, что вы админ.</b>\n\n"
                         "Введите пароль:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(SignUpAdmin.password)


@dp.message_handler(state=SignUpAdmin.password)
async def handle_teacher_password(message: types.Message, state: FSMContext):
    if message.text == admin_password:
        await sign_up_admin(message, state)
    else:
        await admin_password_waiting(message, state)
        await message.answer("❌<b>Неправильный пароль.</b> Попробуйте ещё раз.")


async def sign_up_admin(message: types.Message, state: FSMContext):
    await message.answer('✅<b>Пароль введён верно.</b>\n\n'
                         '👤Введите вашу <b>Фамилию и Имя</b> через пробел\n'
                         'Пример корректных данных: <b>Иванов Иван</b>')
    await state.set_state(SignUpAdmin.name)


@dp.message_handler(state=SignUpAdmin.name)
async def admin_su(message: types.Message, state: FSMContext):
    if len(message.text.split()) != 2:
        await message.answer(
            '❌<b>Фамилия или имя введены неверно.</b> Пример корректных данных: <b>Иванов Иван</b>')
    else:
        first_name, last_name = message.text.split()
        send_user_to_base(message.from_user.id, first_name, last_name, 1)

        await main_menu_message(message, f'👋Здравствуйте, {first_name} {last_name},\n Вы успешно зарегистрировались', 1)
        await state.finish()


async def sign_up_student(message: types.Message, state: FSMContext):
    await message.answer('👤Введите вашу <b>Фамилию и Имя</b> через пробел\n'
                         'Пример корректных данных: <b>Иванов Иван</b>', reply_markup=ReplyKeyboardRemove())
    await state.set_state(SignUpStudent.name)


@dp.message_handler(state=SignUpStudent.name)
async def student_su(message: types.Message, state: FSMContext):
    if len(message.text.split()) != 2:
        await message.answer(
            '❌<b>Фамилия или имя введены неверно.</b> Пример корректных данных: <b>Иванов Иван</b>')
    else:
        first_name, last_name = message.text.split()
        send_user_to_base(message.from_user.id, first_name, last_name, 0)
        await main_menu_message(message, f'👏Здравствуйте, {first_name} {last_name},\n Вы успешно зарегистрировались', 0)
        await state.finish()
