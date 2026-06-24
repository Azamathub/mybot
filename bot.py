import logging
import asyncio
import os
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReactionTypeEmoji

API_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_USERNAME = 'aldilshod'
GEMINI_KEY = os.getenv('GEMINI_KEY')

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🕒 Ish vaqtimiz"), KeyboardButton(text="📍 Manzilimiz")],
            [KeyboardButton(text="💰 Xizmat narxlari")],
            [KeyboardButton(text="🤖 Sun'iy Intellekt (AI)")],
            [KeyboardButton(text="Adminga yozish")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Kerakli bo'limni tanlang..."
    )
    return keyboard

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.react(reaction=[ReactionTypeEmoji(emoji="👍")])
    await message.reply(
        "👋 Assalomu alaykum! Bizning servis botimizga xush kelibsiz.\n\n"
        "Quyidagi tugmalardan foydalanib kerakli ma'lumotni olishingiz mumkin:",
        reply_markup=get_main_keyboard()
    )

@dp.message(F.text == "🕒 Ish vaqtimiz")
async def process_time(message: types.Message):
    await message.react(reaction=[ReactionTypeEmoji(emoji="⚡")])
    await message.reply("Ish vaqtimiz: 09:00 dan 18:00 gacha. Juma kuni dam, boshqa kunlari xizmatingizdamiz!")

@dp.message(F.text == "📍 Manzilimiz")
async def process_location(message: types.Message):
    await message.react(reaction=[ReactionTypeEmoji(emoji="🔥")])
    await bot.send_photo(
        chat_id=message.chat.id,
        photo="BU_YERGA_FILE_ID",
        caption="📍 Bekobod shahar Tohir va Zuhra savdo kompleksi 1-qavatida 112-dokon."
    )
    await message.reply_location(latitude=40.2140770, longitude=69.2654280)

@dp.message(F.text == "💰 Xizmat narxlari")
async def process_price(message: types.Message):
    await message.react(reaction=[ReactionTypeEmoji(emoji="✍")])
    await message.reply("Xizmat ko'rsatish narxlari qurilma va muammo murakkabligiga qarab farq qiladi. Diagnostika 50ming so'm!")

@dp.message(F.text == "🤖 Sun'iy Intellekt (AI)")
async def process_ai_info(message: types.Message):
    await message.react(reaction=[ReactionTypeEmoji(emoji="🤔")])
    await message.reply("🤖 AI tizimi faol! Istalgan savolingizni matn shaklida yozib yuboring!")

@dp.message(F.text == "Adminga yozish")
async def process_admin(message: types.Message):
    await message.react(reaction=[ReactionTypeEmoji(emoji="👨‍💻")])
    await message.reply(f"👨‍💻 Adminga yozish:\n👉 https://t.me/{ADMIN_USERNAME}")

@dp.message(F.photo)
async def get_photo_id(message: types.Message):
    file_id = message.photo[-1].file_id
    await message.reply(f"Rasm file_id: `{file_id}`")

@dp.message()
async def handle_ai_response(message: types.Message):
    await message.react(reaction=[ReactionTypeEmoji(emoji="👀")])
    user_question = message.text
    try:
        prompt = f"Siz Bekobod shahridagi telefon va kompyuter servisi botisiz. Mijozlarga o'zbek tilida qisqa va foydali javob bering. Savol: {user_question}"
        response = model.generate_content(prompt)
        ai_reply = response.text
    except Exception as e:
        ai_reply = "Hozirda AI javob bera olmayapti. Iltimos adminga murojaat qiling."
    await message.reply(ai_reply)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())