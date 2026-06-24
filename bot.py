import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReactionTypeEmoji, FSInputFile

# Railway'dagi Variables bo'limidan tokenni avtomatik o'qib oladi
API_TOKEN = os.getenv("BOT_TOKEN")

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

# 📍 Manzilimiz (Rasm + Lokatsiya) - Railway uchun xavfsiz qilingan variant
@dp.message(F.text == "📍 Manzilimiz")
async def process_location(message: types.Message):
    await message.react(reaction=[ReactionTypeEmoji(emoji="🔥")])
    
    caption_text = "📍 Bizning servis Bekobod shahar Tohir va Zuhra savdo kompleksi 1-qavatida 112-dokon."
    
    try:
        # Server papkasidagi manzil.jpg faylini tekshiramiz
        if os.path.exists("manzil.jpg"):
            photo = FSInputFile("manzil.jpg")
            await message.reply_photo(photo=photo, caption=caption_text)
        else:
            await message.reply(f"{caption_text}\n\n(Tizimda rasm fayli topilmadi)")
    except Exception as e:
        # Agar kutilmagan xato bo'lsa, server o'chib qolmaydi, faqat matn yuboradi
        await message.reply(caption_text)
    
    # Bekobod koordinatalari
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
    await message.reply("🤖 AI tizimi faol! Istalgan savolingizni matn shaklida yozib yuboring, 'Bizning servis' nomidan javob beraman.")

# Adminga yozish tugmasi
@dp.message(F.text == "Adminga yozish")
async def process_admin(message: types.Message):
    await message.react(reaction=[ReactionTypeEmoji(emoji="👨‍💻")])
    await message.reply("👨‍💻 Savollar yoki takliflar bo'lsa, adminga yozishingiz mumkin:\n👉 https://t.me/admin_aldilshod")

# Ixtiyoriy matn yozilsa (AI javob beradi)
@dp.message()
async def handle_ai_response(message: types.Message):
    await message.react(reaction=[ReactionTypeEmoji(emoji="👀")])
    user_question = message.text
    ai_prompt_prefix = "Bizning servis ushbu savolga quyidagicha javob beradi: \n\n"
    ai_generated_reply = f"Sizning '{user_question}' bo'yicha so'rovingiz qabul qilindi. Biz sizga eng sifatli yordamni taklif etamiz!"
    await message.reply(f"{ai_prompt_prefix}{ai_generated_reply}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())