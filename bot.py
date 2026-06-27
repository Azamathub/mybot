import os
import asyncio
from pyrogram import Client, filters
import google.generativeai as genai

SESSION_STRING = os.getenv("SESSION_STRING")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini API sozlash
genai.configure(api_key=GEMINI_API_KEY)

app = Client(
    "my_userbot",
    session_string=SESSION_STRING
)

@app.on_message(filters.incoming & filters.private)
async def reply_keywords(client, message):
    text_lower = message.text.lower() if message.text else ""
    
    if text_lower == "salom":
        await message.reply_text("Assalomu alaykum! Men Azamatxo'janing sun'iy intellekt yordamchisiman. Hozirda u biroz band bo'lishi mumkin. Sizga qanday yordam bera olaman?")
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
        
    elif text_lower in ["rahmat", "raxmat"]:
        await message.reply_text("Arziydi! Har doim xizmatingizdamiz. 👍")
        return

    if message.text:
        try:
            await client.send_chat_action(message.chat.id, "typing")
            
            # Har qanday versiyada 100% ishlaydigan model chaqiruvi
            try:
                model = genai.GenerativeModel("gemini-pro")
                response = model.generate_content(message.text)
                response_text = response.text
            except Exception:
                # Agar eski versiya bo'lsa, zaxira generatsiya usuli
                response = genai.generate_text(prompt=message.text)
                response_text = response.result
            
            if response_text:
                await message.reply_text(response_text)
            else:
                raise Exception("Bo'sh javob qaytdi")
                
        except Exception as e:
            print(f"Gemini xatosi: {e}")
            await message.reply_text("Xabaringiz qabul qilindi, tez orada javob beramiz!")

if __name__ == "__main__":
    print("🤖 Bot ishga tushdi...")
    app.run()