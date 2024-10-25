import logging
import asyncio
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sendMes import startBot


API_TOKEN = '7989933734:AAFAH6CtvANDrSGSFIe1wqLCPpBLKJDFcV0'

def start_keyBoard():
    button1 = KeyboardButton(text='Rock Dog')
    button2 = KeyboardButton(text='Party Zoo')
    button_rows = [button1, button2]
    keyboard = ReplyKeyboardMarkup(keyboard = [button_rows])
    return keyboard

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer("Выберите опцию:", reply_markup=start_keyBoard())

@dp.message(Command("help"))
async def send_help(message: types.Message):
    await message.reply("Доступные команды:\n/start - Приветствие\n/help - Список команд\n/send - отправка запросов")

@dp.message(lambda message: message.text in ["Rock Dog", "Party Zoo"])
async def handle_button_click(message: types.Message):
    answer = await startBot(message.text) 
    await message.reply(str(answer))

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())