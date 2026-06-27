import os
import asyncio
from pyrogram import Client, filters
import google.generativeai as genai

# Railway'dagi Environment Variables (o'zgaruvchilar) bo'limidan ma'lumotlarni o'qiymiz
SESSION_STRING = os.getenv("SESSION_STRING")
# Agar Gemini API kalitini ham Railway'ga qo'shgan bo'lsangiz, uni ham avtomatik oladi
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

# Gemini AI modelini sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Pyrogram mijozini sessiya kaliti orqali ishga tushiramiz
app = Client(
    "my_userbot",
    session_string=SESSION_STRING
)

# 1. Maxsus kalit so'zlar uchun avtomatik javoblar (Kichik harflarda tekshiradi)
@app.on_message(filters.incoming & filters.private)
async def reply_keywords(client, message):
    text_lower = message.text.lower() if message.text else ""
    
    if text_lower == "salom":
        await message.reply_text("Assalomu alaykum! Men Azamatxo'janing sun'iy intellekt yordamchisiman. Hozirda u biroz band bo'lishi mumkin. Sizga qanday yordam bera olaman?")
        return
        
    elif text_lower in ["rahmat", "raxmat"]:
        await message.reply_text("Arziydi! Har doim xizmatingizdamiz. 👍")
        return

    # 2. Agar kelgan xabar oddiy matn bo'lsa va kalit so'zlarga tushmasa, Gemini AI javob beradi
    if message.text:
        try:
            # Kutish vaqtida foydalanuvchiga "yozmoqda..." (typing) holatini ko'rsatish
            await client.send_chat_action(message.chat.id, "typing")
            
            # Gemini AI'dan javob olish
            response = model.generate_content(message.text)
            
            # Sun'iy intellekt javobini yuborish
            await message.reply_text(response.text)
        except Exception as e:
            print(f"Gemini AI xatoligi: {e}")
            # Agar Gemini ulanmagan bo'lsa, zaxira xabar
            await message.reply_text("Xabaringiz qabul qilindi. Tez orada sizga aloqaga chiqishadi!")

if __name__ == "__main__":
    print("🤖 Userbot muvaffaqiyatli ishga tushdi va xabarlarni kutmoqda...")
    app.run()