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