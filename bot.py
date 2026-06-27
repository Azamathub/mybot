import os
import asyncio
from pyrogram import Client, filters
import google.generativeai as genai

# Railway'dagi muhit o'zgaruvchilari
SESSION_STRING = os.getenv("SESSION_STRING")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini modeliga uning xarakteri va qanday javob berishi kerakligini o'rgatamiz (System Instruction)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config={
        "temperature": 0.5, # Javoblar har xil va tabiiy chiqishi uchun (0.1 dan 1.0 gacha)
    }
)

app = Client(
    "my_userbot",
    session_string=SESSION_STRING
)

# Maxsus kalit so'zlar uchun shaxsiy javoblar bazasi
@app.on_message(filters.incoming & filters.private)
async def reply_keywords(client, message):
    text_lower = message.text.lower() if message.text else ""
    
    # 1. O'zingiz xohlagan so'zlarga o'zingiz xohlagan javoblar (Shu yerda matnlarni o'zgartirishingiz mumkin)
    if text_lower == "salom":
        await message.reply_text("Assalomu alaykum! Azamatxo'janing shaxsiy yordamchisiman. Hozir u biroz band. Sizga qanday yordam bera olaman?")
        return

    elif text_lower in ["Assalomu alaykum"]:
        await message.reply_text("Vaalayum Assalom! yxashimisiz")
        return

    elif text_lower in ["qalesiz"]:
        await message.reply_text("Qichuu😎")
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

    # 2. Agar tayyor javob topilmasa, Gemini AI javob beradi
    if message.text:
        try:
            # Spamga tushmaslik uchun majburiy "yozmoqda..." holati va 3 soniya kutish
            await client.send_chat_action(message.chat.id, "typing")
            await asyncio.sleep(3) # Odamga o'xshab 3 soniya o'ylab javob beradi
            
            # Gemini siz istagandek javob berishi uchun so'rov oldiga shart qo'shamiz
            system_prompt = (
                "Sen o'zbek tilida gaplashadigan, aqlli, qisqa va aniq javob beradigan yordamchisan. "
                "Foydalanuvchining ismi Azamatxo'ja. Hozir u bandligi uchun sen uning nomidan xushmuomalalik bilan javob beryapsan. "
                "Uzoq va zerikarli matnlar yozma, silliq va lo'nda javob ber. "
                f"Foydalanuvchi xabari: {message.text}"
            )
            
            response = model.generate_content(system_prompt)
            await message.reply_text(response.text)
            
        except Exception as e:
            print(f"Xatolik: {e}")
            await message.reply_text("Xabaringiz qabul qilindi, tez orada javob beramiz!")

if __name__ == "__main__":
    print("🤖 Xavfsiz va aqlli Userbot ishga tushdi...")
    app.run()