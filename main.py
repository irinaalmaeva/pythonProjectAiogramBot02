import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile
from aiogram.types import Message
from googletrans import Translator


# Настройка логирования
logging.basicConfig(level=logging.INFO)

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Настраиваем переводчик
translator = Translator()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Отправь мне фотографию, текст или скажи что-нибудь.")


# Обработчик фотографий
@dp.message(F.photo)
async def handle_photo(message: Message):
    photo = message.photo[-1]  # Получаем фото наивысшего качества
    photo_id = photo.file_id
    photo_file = await bot.download(photo_id)

    # Генерация пути для сохранения изображения
    photo_path = os.path.join('img', f"{photo_id}.jpg")

    with open(photo_path, 'wb') as f:
        f.write(photo_file.read())

    await message.answer("Фото сохранено!")

# Обработчик текстовых сообщений с переводом
@dp.message(F.text)  # Фильтр для текстовых сообщений
async def handle_text(message: types.Message):
    try:
        # Пытаемся перевести текст на английский
        translated_text = translator.translate(message.text, dest='en').text
        await message.answer(f"Перевод на английский: {translated_text}")
    except Exception as e:
        # Обработка всех исключений
        await message.answer(f"Произошла ошибка при переводе: {e}")


@dp.message(F.voice)  # Фильтр для голосовых сообщений
async def handle_voice(message: types.Message):
    voice = message.voice  # Получаем голосовое сообщение
    voice_id = voice.file_id
    voice_file = await bot.download(voice_id)

    # Генерация пути для сохранения голосового сообщения
    voice_path = os.path.join('voice', f"{voice_id}.ogg")

    with open(voice_path, 'wb') as f:
        f.write(voice_file.read())

    await message.answer("Голосовое сообщение сохранено!")


# Обработчик команды отправки голосового сообщения
@dp.message(Command("send_voice"))
async def send_voice(message: types.Message):
    voice_file = FSInputFile('path_to_voice_file.ogg')  # Замените 'path_to_voice_file.ogg' на путь к вашему файлу
    await message.answer_voice(voice_file)


# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())