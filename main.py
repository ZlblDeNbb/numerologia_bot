from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from datetime import datetime
import os
from dotenv import load_dotenv
from database import DatabaseManager
from models_ai.chatGPT4 import ChatGPT4Model
from models_ai.prompts_ai import NumerologyPrompts
from states import LifePathStates, CompatibilityStates, NumerologyStates

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

gpt_model = ChatGPT4Model()
db_manager = DatabaseManager()


@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer(
        text="👋 Добро пожаловать в нумерологический бот на основе ИИ!\n\n"
              "⚠️ *Внимание!* Этот бот работает на базе искусственного интеллекта и предназначен только для развлекательных целей.\n\n "
             "Вы можете использовать следующие команды:\n"
             "/life_path - 🔮 Узнать своё число жизненного пути\n"
             "/compatibility - ❤️ Определить совместимость по дате рождения\n"
             "/numerology_question - 🤔 Задать вопрос нумерологу\n"
             "/help - Получить помощь по боту\n"
    )

@dp.message(Command('help'))
async def help_command(message: types.Message):
    await message.answer(
        text="📚 *Доступные команды:*\n"
             "/start - Перезапуск бота\n"
             "/life_path - 🔮 Узнать своё число жизненного пути\n"
             "/compatibility - ❤️ Проверить совместимость\n"
             "/numerology_question - 🤔 Задать вопрос нумерологу\n\n"
             "Нажмите на любую команду, чтобы начать!"
    )


@dp.message(Command('life_path'))
async def life_path_handler(message: types.Message, state: FSMContext):
    await message.answer("Введите свою дату рождения в формате ДД.ММ.ГГГГ для расчёта числа жизненного пути.")
    await state.set_state(LifePathStates.WAITING_FOR_BIRTHDATE)


@dp.message(LifePathStates.WAITING_FOR_BIRTHDATE)
async def process_life_path_date(message: types.Message, state: FSMContext):
    date_text = message.text.strip()

    processing_message = await message.answer("Подождите, запрос обрабатывается...")

    try:
        date_obj = datetime.strptime(date_text, "%d.%m.%Y")
    except ValueError:
        await message.reply("Пожалуйста, введите дату рождения в правильном формате: ДД.ММ.ГГГГ.")
        await processing_message.delete()  # Удаление сообщения об обработке
        return

    if date_obj.year < 1950 or date_obj > datetime.now():
        await message.reply("Пожалуйста, введите реальную дату рождения.")
        await processing_message.delete()  # Удаление сообщения об обработке
        return

    prompt = NumerologyPrompts.get_life_path_prompt(date_text)
    response = gpt_model.get_response(date_text, prompt)
    db_manager.add_query(message.from_user.id, "life_path", date_text, response)
    await message.reply(f"Ваше число жизненного пути: {response}")
    await message.answer("Вы вернулись на стартовое меню.")  # Убираем кнопки
    await processing_message.delete()
    await state.clear()  # Состояние очищается после обработки


@dp.message(Command('compatibility'))
async def compatibility_handler(message: types.Message, state: FSMContext):
    await message.answer("Введите две даты рождения в формате ДД.ММ.ГГГГ и ДД.ММ.ГГГГ для расчёта совместимости.")
    await state.set_state(CompatibilityStates.WAITING_FOR_DATES)


@dp.message(CompatibilityStates.WAITING_FOR_DATES)
async def process_compatibility_dates(message: types.Message, state: FSMContext):

    dates_text = message.text.strip().split(" и ")
    processing_message = await message.answer("Подождите, запрос обрабатывается...")

    if len(dates_text) != 2:
        await message.reply("Пожалуйста, введите ровно две даты, разделённые 'и', в формате ДД.ММ.ГГГГ.")
        await processing_message.delete()  # Удаление сообщения об обработке
        return

    date_objects = []

    for date_text in dates_text:
        date_text = date_text.strip()  # Убираем лишние пробелы

        try:
            date_obj = datetime.strptime(date_text, "%d.%m.%Y")

            if date_obj.year < 1900 or date_obj > datetime.now():
                await message.reply(f"Дата {date_text} выходит за пределы допустимого диапазона (с 1900 года).")
                await processing_message.delete()  # Удаление сообщения об обработке
                return

            date_objects.append(date_obj)
        except ValueError:
            await message.reply(f"Дата {date_text} не соответствует формату ДД.ММ.ГГГГ. Пожалуйста, исправьте ввод.")
            await processing_message.delete()  # Удаление сообщения об обработке
            return

    if len(date_objects) == 2:
        date1, date2 = dates_text[0], dates_text[1]
        prompt = NumerologyPrompts.get_compatibility_prompt(date1, date2)
        response = gpt_model.get_response(f"{date1} и {date2}", prompt)

        db_manager.add_query(message.from_user.id, "compatibility", message.text, response)
        await message.reply(f"Результаты совместимости: {response}")

        await message.answer("Вы вернулись на стартовое меню.")  # Убираем кнопки

    await processing_message.delete()
    await state.clear()


@dp.message(Command('numerology_question'))
async def numerology_question_handler(message: types.Message, state: FSMContext):
    await message.reply("Задайте свой вопрос нумерологу:")
    await state.set_state(NumerologyStates.WAITING_FOR_QUESTION)


@dp.message(NumerologyStates.WAITING_FOR_QUESTION)
async def process_numerology_question(message: types.Message, state: FSMContext):
    processing_message = await message.answer("Подождите, запрос обрабатывается...")
    prompt = NumerologyPrompts.numerology_assistant_prompt
    response = gpt_model.get_response(message.text, prompt)
    db_manager.add_query(message.from_user.id, "numerology_question", message.text, response)
    await message.reply(response)
    await message.answer("Вы вернулись на стартовое меню.")  # Убираем кнопки
    await processing_message.delete()
    await state.clear()  # Состояние очищается после обработки


@dp.message()
async def generic_question_handler(message: types.Message, state: FSMContext):
    if await state.get_state() is None:
        await message.reply("Пожалуйста, выберите команду с помощью меню.")


if __name__ == "__main__":
    import asyncio

    async def main():
        await dp.start_polling(bot)  # Передаем bot в метод start_polling

    asyncio.run(main())
