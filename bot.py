import os
import asyncio
from pyrogram import Client, filters
import google.generativeai as genai

# Railway o'zgaruvchisidan oladi
SESSION_STRING = os.getenv("SESSION_STRING")

# AGAR RAILWAY VARIABLES ISHLAMASA, API KALITNI SHU YERGA QO'SHTIRNOQ ICHIGA YOZING:
GEMINI_API_KEY = "SESHU_YERGA_GEMINI_KALITINI_QO_YING"

# Gemini AI modelini sozlash
if GEMINI_API_KEY and GEMINI_API_KEY != "SESHU_YERGA_GEMINI_KALITINI_QO_YING":
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None

app = Client(
    "my_userbot",
    session_string=SESSION_STRING
)

@app.on_message(filters.incoming & filters.private)
async def reply_handler(client, message):
    if not message.text:
        return

    text_lower = message.text.lower()

    # Oddiy kalit so'zlarni tekshirish
    if text_lower == "salom":
        await message.reply_text("Assalomu alaykum! Men Azamatxo'janing sun'iy intellekt yordamchisiman. Hozirda u biroz band bo'lishi mumkin. Sizga qanday yordam bera olaman?")
        return
    elif text_lower in ["rahmat", "raxmat"]:
        await message.reply_text("Arziydi! Har doim xizmatingizdamiz. 👍")
        return

elif text_lower in ["Assalomu alaykum"]:
        await message.reply_text("Vaalayum Assalom! yaxshimisiz")
        return

    elif text_lower in ["qalesiz"]:
        await message.reply_text("Qichuu😎")
        return

    elif text_lower in ["Assalomu alaykum"]:
        await message.reply_text("Vaalayum assalom!")
        return

    elif text_lower in ["assalomu alaykum"]:
        await message.reply_text("Vaalaykum assalom!")
        return

    elif text_lower in ["qanday"]:
        await message.reply_text("Qichuu😎")
        return

    elif text_lower in ["Azamat"]:
        await message.reply_text("Labbay?😊")
        return

    elif text_lower in ["salomat boling"]:
        await message.reply_text("Siz ham!🤝")
        return
        
    elif text_lower in ["rahmat", "raxmat"]:
        await message.reply_text("Arziydi, salomat bo'ling!🤝 👍")
        return

    elif text_lower in ["nima gap"]:
        await message.reply_text("Tinch, ozindachi?")
        return

    elif text_lower in ["chit bormi"]:
        await message.reply_text("kaneshna, @chit_oyinlarim shu kanalimda bor")
        return

    elif text_lower in ["yaxshimisiz"]:
        await message.reply_text("Yashi rahmat🤗")
        return

    elif "narx" in text_lower or "qancha" in text_lower:
        await message.reply_text("Xizmatlar va mahsulotlar narxi haqida hozir Azamatxo'janing o'zlari aloqaga chiqib batafsil ma'lumot beradilar.")
        return

    elif "prashivka qilasizmi" in text_lower or "qancha" in text_lower:
        await message.reply_text("Ha albatta, Xizmatlar va mahsulotlar narxi haqida hozir Azamatxo'janing o'zlari aloqaga chiqib batafsil ma'lumot beradilar.Lekin prashivka qilgandan keyin telefon samalyot boladi ishlashi🔥")
        return

    # Agar kalit so'z bo'lmasa va Gemini sozlangan bo'lsa
    if model:
        try:
            await client.send_chat_action(message.chat.id, "typing")
            response = model.generate_content(message.text)
            await message.reply_text(response.text)
        except Exception as e:
            print(f"Gemini Error: {e}")
            await message.reply_text("Xabaringiz qabul qilindi, tez orada javob beramiz!")
    else:
        await message.reply_text("Xabaringiz qabul qilindi, tez orada javob beramiz!")

if __name__ == "__main__":
    print("🤖 Bot qayta start oldi...")
    app.run()