import os
import requests
from pyrogram import Client, filters

SESSION_STRING = os.getenv("SESSION_STRING")
GEMINI_API_KEY = "AIzaSyCCXqmHS7eRukRyLIH3ftVDorVIMEj-dH4"

app = Client("my_userbot", session_string=SESSION_STRING)

def ask_gemini(t):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    try:
        r = requests.post(url, json={"contents": [{"parts": [{"text": t}]}]}, headers={"Content-Type": "application/json"}, timeout=15)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return None

@app.on_message(filters.incoming & filters.private)
async def hello_handler(client, message):
    # 1. Agar stiker, rasm yoki ovozli xabar kelsa (matn bo'lmasa)
    if not message.text:
        await message.reply_text("Assalomu alaykum! Men Azamatxo'janing sun'iy intellekt yordamchisiman. Hozirda u biroz band bo'lishi mumkin. Sizga qanday yordam bera olaman?")
        return

    t = message.text.lower().strip()

    # 2. Salomlashish so'zlari
    if t in ["salom", "assalomu alaykum", "salom!", "assalomu alaykum!"]:
        await message.reply_text("Assalomu alaykum! Men Azamatxo'janing sun'iy intellekt yordamchisiman. Hozirda u biroz band bo'lishi mumkin. Sizga qanday yordam bera olaman?")
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
    elif t in ["rahmat", "raxmat", "rahmat!"]:
        await message.reply_text("Arziydi! Har doim xizmatingizdamiz. 👍")
        return

    # 3. Qolgan barcha savollar uchun Gemini AI
    await client.send_chat_action(message.chat.id, "typing")
    javob = ask_gemini(message.text)
    
    if javob:
        await message.reply_text(javob)
    else:
        await message.reply_text("Xabaringiz qabul qilindi, tez orada javob beramiz!")

if __name__ == "__main__":
    app.run()