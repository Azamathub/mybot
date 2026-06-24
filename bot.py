import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReactionTypeEmoji, FSInputFile
import google.generativeai as genai

# Railway Variables bo'limidan token va kalitlarni o'qiymiz
API_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

# Gemini AI ni sozlash
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash") # Tezkor va aqlli model

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Pastki klaviatura tugmalari
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🕒 Ish vaqtimiz"),
                KeyboardButton(text="📍 Manzilimiz")
            ],
            [
                KeyboardButton(text="💰 Xizmat narxlari")
            ],
            [
                KeyboardButton(text="🤖 Sun'iy Intellekt (AI)")
            ],
            [
                KeyboardButton(text="Adminga yozish")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Kerakli bo'limni tanlang..."
    )
    return keyboard

# /start buyrug'i
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.react(reaction=[ReactionTypeEmoji(emoji="👍")])
    await message.reply(
        "👋 Assalomu alaykum! Bizning servis botimizga xush kelibsiz.\n\n"
        "Quyidagi tugmalardan foydalanib kerakli ma'lumotni olishingiz mumkin:",
        reply_markup=get_main_keyboard()
    )

# 🕒 Ish vaqti
@dp.message(F.text == "🕒 Ish vaqtimiz")
async def process_time(message: types.Message):
    await message.react(reaction=[ReactionTypeEmoji(emoji="⚡")])
    await message.reply("Ish vaqtimiz: 09:00 dan 18:00 gacha. Juma kuni dam, boshqa kunlari xizmatingizdamiz!")

# 📍 Manzilimiz (Rasm + Lokatsiya)
@dp.message(F.text == "📍 Manzilimiz")
async def process_location(message: types.Message):
    await message.react(reaction=[ReactionTypeEmoji(emoji="🔥")])
    caption_text = "📍 Bizning servis Bekobod shahar Tohir va Zuhra savdo kompleksi 1-qavatida 112-dokon."
    
    try:
        if os.path.exists("manzil.jpg"):
            photo = FSInputFile("manzil.jpg")
            await message.reply_photo(photo=photo, caption=caption_text)
        else:
            await message.reply(caption_text)
    except Exception:
        await message.reply(caption_text)
    
    latitude = 40.2140770   
    longitude = 69.2654280  
    await message.reply_location(latitude=latitude, longitude=longitude)

# 💰 Xizmat narxlari
@dp.message(F.text == "💰 Xizmat narxlari")
async def process_price(message: types.Message):
    await message.react(reaction=[ReactionTypeEmoji(emoji="✍")])
    await message.reply("Xizmat ko'rsatish narxlari qurilma va muammo murakkabligiga qarab farq qiladi. Diagnostika 50ming so'm!")

# 🤖 AI haqida ma'lumot
@dp.message(F.text == "🤖 Sun'iy Intellekt (AI)")
async def process_ai_info(message: types.Message):
    await message.react(reaction=[ReactionTypeEmoji(emoji="🤔")])
    await message.reply("🤖 Haqiqiy AI tizimi faol! Istalgan savolingizni biron bir tugmani bosmasdan, to'g'ridan-to'g'ri matn shaklida yozib yuboring, Gemini AI sizga javob beradi.")

# Adminga yozish tugmasi
@dp.message(F.text == "Adminga yozish")
async def process_admin(message: types.Message):
    await message.react(reaction=[ReactionTypeEmoji(emoji="👨‍💻")])
    await message.reply("👨‍💻 Savollar yoki takliflar bo'lsa, adminga yozishingiz mumkin:\n👉 https://t.me/admin_aldilshod")

# HAQIQIY GEMINI AI: Agar ixtiyoriy boshqa matn yozilsa, Gemini javob beradi
@dp.message()
async def handle_ai_response(message: types.Message):
    await message.react(reaction=[ReactionTypeEmoji(emoji="👀")])
    user_question = message.text
    
    try:
        # Sun'iy intellektga kontekst beramiz, u o'zini servis yordamchisi deb bilsin
        prompt = f"Siz 'Bizning servis' nomli texnik xizmat ko'rsatish markazining aqlli yordamchisiz. Quyidagi savolga o'zbek tilida qisqa, aniq va xushmuomala javob bering:\n\nSavol: {user_question}"
        
        # Gemini modelidan javob olish
        response = model.generate_content(prompt)
        await message.reply(response.text)
        
    except Exception as e:
        logging.error(f"Gemini xatolik: {e}")
        await message.reply("🤖 AI tizimida vaqtincha uzilish bo'ldi. Sal keyinroq qayta urunib ko'ring.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())