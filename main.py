import logging
import asyncio
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command  
from sendMes import startBot 

API_TOKEN = '7989933734:AAFAH6CtvANDrSGSFIe1wqLCPpBLKJDFcV0'

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(Command("start")) 
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я ваш асинхронный бот. Используйте /help для получения помощи.")

@dp.message(Command("help")) 
async def send_help(message: types.Message):
    await message.reply("Доступные команды:\n/start - Приветствие\n/help - Список команд\n/send - отправка запросов")

@dp.message(Command("send")) 
async def send_request(message: types.Message):
    answer = await startBot()
    await message.reply(str(answer))

async def main() -> None:

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
