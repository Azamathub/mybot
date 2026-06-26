import os
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
import google.generativeai as genai

# ====================================================================
# YAONGILANGAN SHAXSIY SOZLAMALARINGIZ (Aynan siz saytdan olgan kodlar)
# ====================================================================
API_ID = 39604699  # Sizning shaxsiy API ID raqamingiz
API_HASH = "ce4fd11ec88dbc10f9718f3a9ddef419"  # Sizning shaxsiy API HASH kodingiz

# Gemini AI kaliti (bunga tegmang, turaversin)
GEMINI_API_KEY = "AIzaSyCCXqmHS7eRukRyLIH3ftVDorVIMEj-dH4"

# Botdan olgan o'sha uzun ko'k kodni (SESSION) Railway Variables bo'limiga 
# SESSION_STRING nomi bilan qo'shasiz, kod uni avtomatik o'qiydi:
SESSION_STRING = os.environ.get("SESSION_STRING")

# Gemini AI-ni sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

if not SESSION_STRING:
    print("XATOLIK: Railway panelida SESSION_STRING o'zgaruvchisi kiritilmagan!")
    exit(1)

# Telegram mijozini ishga tushirish
app = Client("gemini_userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# Sizning tayyor shablonlaringiz
TAYYOR_JAVOBLAR = {
    "Assalomu Alaykum":"Vaalayum Assalom Sogliqingiz yaxshimi🤗", "assalomaleykum": "voleykumassalom", "ismiz nima": "Azamat Abduraimov", "salom": "Salom! Men hozir biroz bandman, lekin tez orada xabaringizni o'qiyman. Ungacha savolingizni qoldirishingiz mumkin. 😊",
    "narxi qancha": "Xizmatlarimiz va narxlarimiz haqida batafsil ma'lumotni kanalda ko'rishingiz mumkin.",
    "manzil": "Bizning manzil: Yer shari🗿.",
    "rahmat": "Arziydi, doimo xizmatingizdamiz! 👍", "🤝": "🤝", "prashivka qilib berasizmi": "ha albatta asosan redmining asta ishlaydigan madelarini qilsak udar samalyotdek iishlaydigan boladi ayniqsa redmi 9A🔥"
}

@app.on_message(filters.private & ~filters.me & ~filters.bot)
async def auto_responder(client, message):
    text = message.text
    if not text:
        return

    text_lower = text.lower().strip()
    tanlangan_javob = None

    # Tayyor javoblarni tekshirish
    for kalit_soz, javob in TAYYOR_JAVOBLAR.items():
        if kalit_soz in text_lower:
            tanlangan_javob = javob
            break

    # Agar kalit so'z topilmasa -> Gemini AI javob beradi
    if not tanlangan_javob:
        try:
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            await asyncio.sleep(3)

            prompt = f"Siz aqlli yordamchisiz. Quyidagi xabarga o'zbek tilida, juda qisqa, samimiy va lo'nda javob bering. Xabar: {text}"
            response = model.generate_content(prompt)
            tanlangan_javob = response.text
        except Exception as e:
            print(f"Gemini Error: {e}")
            return

    if tanlangan_javob:
        await message.reply_text(tanlangan_javob)

if __name__ == "__main__":
    print("Userbot muvaffaqiyatli ishga tushdi...")
    app.run()