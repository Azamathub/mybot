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
    except:
        return None

@app.on_message(filters.private & ~filters.me) 
async def hello_handler(client, message):
    if not message.text:
        await message.reply_text("Assalomu alaykum! Men Azamatxo'janing yordamchisiman. Sizga qanday yordam bera olaman?")
        return

    t = message.text.lower().strip()

    # Maxsus javoblar
    if t in ["assalomu alaykum"]:
        await message.reply_text("Vaalaykum assalom! Yaxshimisiz? Qanday yordam bera olaman?")

        elif t == "salom":
        await message.reply_text("Alik, Men Azamatxo'janing yordamchisiman. Sizga qanday yordam bera olaman?")

    elif t == "qalesiz":
        await message.reply_text("Qichuu😎")
        
    elif t == "qanday":
        await message.reply_text("Qichuu😎")

    elif t == "qayttasan", "qayerdasan", "qattasan":
        await message.reply_text("Dubaida🏖️")
        
    elif t == "nima gap":
        await message.reply_text("Tinch, o'zingizda nima gaplar?")

    elif t in ["ismiz", "isming nima"]:
        await message.reply_text("Azamat Abduraimov")
    
    elif t == "azamat":
        await message.reply_text("Labbay?😊")
    
    elif t in ["rahmat", "raxmat"]:
        await message.reply_text("Arziydi, salomat bo'ling!🤝 👍")
    
    elif t == "chit bormi", "mod bormi":
        await message.reply_text("Kaneshna, @chit_oyinlarim shu kanalimda bor.")

    elif "prashivka" in t:
        await message.reply_text("Ha albatta! Prashivka qilgandan keyin telefon samalyot bo'ladi🔥. Narxini Azamatxo'ja aytadilar.")
    
    elif "narx" in t or "qancha" in t:
        await message.reply_text("Xizmatlar va mahsulotlar narxi haqida hozir Azamatxo'janing o'zlari aloqaga chiqib batafsil ma'lumot beradilar.")

    # Gemini qismi
    else:
        await client.send_chat_action(message.chat.id, "typing")
        javob = ask_gemini(message.text)
        if javob:
            await message.reply_text(javob)
        else:
            await message.reply_text("Xabaringiz qabul qilindi, tez orada javob beramiz! Azamatakam yozadilar🤝")

if __name__ == "__main__":
    app.run()