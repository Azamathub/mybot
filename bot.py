import os
import requests
from pyrogram import Client, filters

SESSION_STRING = os.getenv("SESSION_STRING")
GEMINI_API_KEY = "AIzaSyCCXqmHS7eRukRyLIH3ftVDorVIMEj-dH4"

app = Client("my_userbot", session_string=SESSION_STRING)

def ask_gemini(text_input):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    try:
        r = requests.post(url, json={"contents": [{"parts": [{"text": text_input}]}]}, headers={"Content-Type": "application/json"}, timeout=15)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"Gemini xatosi: {e}")
        return None

@app.on_message(filters.incoming & filters.private)
async def hello_handler(client, message):
    if not message.text:
        await message.reply_text("Assalomu alaykum! Men Azamatxo'janing sun'iy intellekt yordamchisiman. Hozirda u biroz band bo'lishi mumkin. Sizga qanday yordam bera olaman?")
        return

    t = message.text.lower().strip()

    # MAXSUS JAVOBLAR (Har biridan keyin 'return' qo'ydim!)
    if "assalomu alaykum" in t:
        await message.reply_text("Vaalaykum assalom! Yaxshimisiz? Qanday yordam bera olaman?")
        return # <-- Mana shu 'return' juda muhim!

    elif any(word in t for word in ["qalesiz", "qanday", "nima gap"]):
        await message.reply_text("Qichuu😎 Tinch, o'zingizda nima gaplar?")
        return

    elif "azamat" in t:
        await message.reply_text("Labbay?😊")
        return

    elif any(word in t for word in ["salomat boling", "rahmat", "raxmat"]):
        await message.reply_text("Arziydi, salomat bo'ling!🤝 👍")
        return

    elif "chit bormi" in t:
        await message.reply_text("Kaneshna, @chit_oyinlarim shu kanalimda bor.")
        return

    elif "yaxshimisiz" in t:
        await message.reply_text("Yaxshi, rahmat!🤗")
        return

    elif "narx" in t or "qancha" in t:
        await message.reply_text("Xizmatlar va mahsulotlar narxi haqida hozir Azamatxo'janing o'zlari aloqaga chiqib batafsil ma'lumot beradilar.")
        return

    elif "prashivka" in t:
        await message.reply_text("Ha albatta! Prashivka qilgandan keyin telefon samalyot bo'ladi, ishlashi vapshe bomba bo'ladi🔥. Narxini Azamatxo'ja aytadilar.")
        return

    # AGAR YUQORIDAGILARNING HECH QAYSISI BO'LMASA:
    await client.send_chat_action(message.chat.id, "typing")
    javob = ask_gemini(message.text)
    
    if javob:
        await message.reply_text(javob)
    else:
        await message.reply_text("Xabaringiz qabul qilindi, tez orada javob beramiz!")

if __name__ == "__main__":
    app.run()