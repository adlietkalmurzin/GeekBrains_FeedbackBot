from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types

from configs.bot_configs import bot, main_menu_message, dp, READYNESS_THRESHOLD, RELEVANT_SCORE_THRESHOLD

from configs.models.checking_for_information.checking_for_information import is_informative
from configs.models.assessment_emotionality.assessment_emotionality import assessment_emotionality
from configs.models.identify_object.identify_object import identify_object
from database.db_session import send_to_base


coef = {
    'question1': 1,
    'question2': 1,
    'question3': 1,
    'question4': 1,
    'question5': 1
}


class Feedback(StatesGroup):
    readiness = State()
    question1 = State()
    question2 = State()
    question3 = State()
    question4 = State()
    question5 = State()


async def leave_review(message: [types.Message, types.CallbackQuery], state: FSMContext):
    back_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_menu.add("🏠Вернуться в главное меню")

    if isinstance(message, types.Message):
        await message.answer("На шкале от 1 до 10,насколько вы готовы поделиться вашим мнением о вебинаре?",
                             reply_markup=back_menu)
    elif isinstance(message, types.CallbackQuery):
        await message.message.answer("<b>1/5</b>\nНа шкале от 1 до 10,насколько вы готовы поделиться вашим мнением о вебинаре?",
                                     reply_markup=back_menu)
    await state.set_state(Feedback.readiness)


@dp.message_handler(state=Feedback.readiness)
async def handle_evaluation(message: types.Message, state: FSMContext):
    if message.text == "🏠Вернуться в главное меню":
        await state.finish()
        await main_menu_message(message, "✅Вы вернулись в главное меню\n"
                                         "Заполнение формы отменено", 0)
    else:
        try:
            readiness = int(message.text)
            if readiness < 1 or readiness > 10:
                raise ValueError
            await message.answer(f"<b>1/5</b>\nО каком вебинаре Вы хотите рассказать?")
            await state.update_data(readiness=readiness)
            await state.set_state(Feedback.question1)
        except ValueError:
            await message.answer("❌Пожалуйста, введите число от 1 до 10")
            return


@dp.message_handler(state=Feedback.question1)
async def get_question1(message: types.Message, state: FSMContext):
    if message.text == "🏠Вернуться в главное меню":
        await state.finish()
        await main_menu_message(message, "✅Вы вернулись в главное меню\n"
                                         "Заполнение отзыва отменено", 0)
    else:
        question1_answer = message.text
        await message.answer("<b>2/5</b>\nЧто вам больше всего понравилось в теме вебинара и почему?")
        await state.update_data(question1=question1_answer)
        await state.set_state(Feedback.question2)


@dp.message_handler(state=Feedback.question2)
async def get_question2(message: types.Message, state: FSMContext):
    if message.text == "🏠Вернуться в главное меню":
        await state.finish()
        await main_menu_message(message, "✅Вы вернулись в главное меню\n"
                                         "Заполнение отзыва отменено", 0)
    else:
        question2_answer = message.text
        await message.answer(
            "<b>3/5</b>\nБыли ли моменты в вебинаре, которые вызвали затруднения в понимании материала? Можете описать их?")
        await state.update_data(question2=question2_answer)
        await state.set_state(Feedback.question3)


@dp.message_handler(state=Feedback.question3)
async def get_question3(message: types.Message, state: FSMContext):
    if message.text == "🏠Вернуться в главное меню":
        await state.finish()
        await main_menu_message(message, "✅Вы вернулись в главное меню\n"
                                         "Заполнение отзыва отменено", 0)
    else:
        question3_answer = message.text
        await message.answer(
            "<b>4/5</b>\nКакие аспекты вебинара, по вашему мнению, нуждаются в улучшении и какие конкретные изменения вы бы предложили?")
        await state.update_data(question3=question3_answer)
        await state.set_state(Feedback.question4)


@dp.message_handler(state=Feedback.question4)
async def get_question4(message: types.Message, state: FSMContext):
    if message.text == "🏠Вернуться в главное меню":
        await state.finish()
        await main_menu_message(message, "✅Вы вернулись в главное меню\n"
                                         "Заполнение отзыва отменено", 0)
    else:
        question4_answer = message.text
        await message.answer(
            "<b>5/5</b>\nЕсть ли темы или вопросы, которые вы бы хотели изучить более подробно в следующих занятиях?")
        await state.update_data(question4=question4_answer)
        await state.set_state(Feedback.question5)


@dp.message_handler(state=Feedback.question5)
async def get_question5(message: types.Message, state: FSMContext):
    if message.text == "🏠Вернуться в главное меню":
        await state.finish()
        await main_menu_message(message, "✅Вы вернулись в главное меню\n"
                                         "Заполнение отзыва отменено", 0)
    else:
        readiness = (await state.get_data()).get('readiness')
        question1_answer = (await state.get_data()).get('question1')
        question2_answer = (await state.get_data()).get('question2')
        question3_answer = (await state.get_data()).get('question3')
        question4_answer = (await state.get_data()).get('question4')
        question5_answer = message.text
        final_feedback = f'{question1_answer} {question2_answer} {question3_answer} {question4_answer} {question5_answer}'
        q = ['О каком вебинаре Вы хотите рассказать?', 'Что вам больше всего понравилось в теме вебинара и почему?',
            'Были ли моменты в вебинаре, которые вызвали затруднения в понимании материала? Можете описать их?', 
            'Какие аспекты вебинара, по вашему мнению, нуждаются в улучшении и какие конкретные изменения вы бы предложили?',
            'Есть ли темы или вопросы, которые вы бы хотели изучить более подробно в следующих занятиях?']
        is_relevant = is_informative([question1_answer +' ' +question1_answer+' '+q[0], question1_answer +' ' +question2_answer+' '+q[1], question1_answer +' ' +question3_answer+' '+q[2],
                                        question1_answer +' ' +question4_answer+' '+q[3], question1_answer +' ' +question5_answer+' '+q[4]])
        object_ = identify_object([question2_answer, question3_answer, question4_answer, question5_answer, question4_answer, question5_answer,])
        is_positive = assessment_emotionality(final_feedback)
        relevant = 1 if is_relevant[1] > 2.5 else 0
  
        
        if (relevant and readiness>READYNESS_THRESHOLD) or (is_relevant[1]>RELEVANT_SCORE_THRESHOLD and readiness<=READYNESS_THRESHOLD):
            send_to_base(question1_answer, question2_answer, question3_answer, question4_answer, question5_answer, 1, object_, is_positive)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Нет. Удалить отзыв и вернуться в главное меню",
                                                    callback_data="main_menu"))
            keyboard.add(types.InlineKeyboardButton(text="Да. Отправить отзыв", callback_data="send_feedback"))
            final_final_feedback = 'Итоговый отзыв:\n\n' + f'{question1_answer}\n\n{question2_answer}\n\n{question3_answer}\n\n{question4_answer}\n\n{question5_answer}\n\nВсё верно?'
            await message.answer(final_final_feedback, reply_markup=keyboard)
            await state.update_data(question5=question5_answer, is_relevant=relevant, object_=object_, is_positive=is_positive)
        else:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Заполнить отзыв заново", callback_data="fill_feedback"))
            keyboard.add(types.InlineKeyboardButton(text="Вернуться в главное меню", callback_data="main_menu"))
            await message.answer('Ваш отзыв неинформативен', reply_markup=keyboard)


@dp.callback_query_handler(text="main_menu")
async def main_menu(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await main_menu_message(call, "❌Отзыв НЕ сохранён. Вы в главном меню\n", 0)


@dp.callback_query_handler(text="send_feedback")
async def send_feedback(call: types.CallbackQuery, state: FSMContext):
    question1_answer = (await state.get_data()).get('question1')
    question2_answer = (await state.get_data()).get('question2')
    question3_answer = (await state.get_data()).get('question3')
    question4_answer = (await state.get_data()).get('question4')
    question5_answer = (await state.get_data()).get('question5')
    final_feedback = f'{question1_answer} {question2_answer} {question3_answer} {question4_answer} {question5_answer}'

    is_relevant = (await state.get_data()).get('is_relevant')
    is_positive = (await state.get_data()).get('is_positive')
    object_ = (await state.get_data()).get('object_')

    send_to_base(question1_answer, question2_answer, question3_answer, question4_answer, question5_answer, is_relevant, object_, is_positive)

    await call.message.delete()
    await main_menu_message(call, "✅Отзыв сохранён. Вы в главном меню\n", 0)


@dp.callback_query_handler(text="fill_feedback")
async def fill_feedback(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await leave_review(call, state)
