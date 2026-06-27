import os
import requests
from pyrogram import Client, filters

# Railway muhitidan sessiyani o'qiydi
SESSION_STRING = os.getenv("SESSION_STRING")

# Haqiqiy Gemini API kalitingiz
GEMINI_API_KEY = "AIzaSyCCXqmHS7eRukRyLIH3ftVDorVIMEj-dH4"

app = Client(
    "my_userbot",
    session_string=SESSION_STRING
)

def ask_gemini(prompt_text):
    """To'g'ridan-to'g'ri Gemini API'ga xavfsiz so'rov yuborish"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=12)
        if response.status_code == 200:
            data = response.json()
            return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"Gemini API Error: {e}")
    return None

# filter.incoming va private ichiga stiker, matn, audio — hammasini qabul qilishni qo'shdik
@app.on_message(filters.incoming & filters.private)
async def reply_handler(client, message):
    # 1. Agar odam birinchi marta stiker, rasm yoki audio tashlasa (ya'ni matn yozmasa)
    if not message.text:
        await message.reply_text("Assalomu alaykum! Men Azamatxo'janing sun'iy intellekt yordamchisiman. Hozirda u biroz band bo'lishi mumkin. Sizga qanday yordam bera olaman?")
        return

    text_lower = message.text.lower().strip()

    # 2. Maxsus matnli kalit so'zlar tekshiruvi
    if text_lower in ["salom", "assalomu alaykum", "assalomu alaykum!", "salom!"]:
        await message.reply_text("Assalomu alaykum! Men Azamatxo'janing sun'iy intellekt yordamchisiman. Hozirda u biroz band bo'lishi mumkin. Sizga qanday yordam bera olaman?")
        return
    elif text_lower in ["rahmat", "raxmat", "rahmat!"]:
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

    # 3. Agar oddiy matn yozsa va u kalit so'z bo'lmasa, Gemini ishlaydi
    await client.send_chat_action(message.chat.id, "typing")
    ai_response = ask_gemini(message.text)

    if ai_response:
        await message.reply_text(ai_response)
    else:
        # Gemini javob bermay qolsa, o'sha sizda ishlagan eski xavfsiz matn qaytadi
        await message.reply_text("Xabaringiz qabul qilindi, tez orada javob beramiz!")

if __name__ == "__main__":
    print("🤖 Bot yangi funksiyalar bilan ishga tushishga tayyor...")
    app.run()