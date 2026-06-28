import os
from pyrogram import Client, filters

SESSION_STRING = os.getenv("SESSION_STRING")

app = Client("my_userbot", session_string=SESSION_STRING)

@app.on_message(filters.private & ~filters.me & ~filters.bot) 
async def hello_handler(client, message):
    # 1. Agar stiker, rasm, ovozli xabar kabi matnsiz narsa kelsa — salom beradi
    if not message.text:
        await message.reply_text("Assalomu alaykum! Men Azamatxo'janing yordamchisiman. Sizga qanday yordam bera olaman?")
        return

    t = message.text.lower().strip()

    # 2. Agar shunchaki "salom" deb yozsa ham — o'sha assalomu alaykum matni chiqadi
    if t in ["salom", "salom!"]:
        await message.reply_text("Assalomu alaykum! Men Azamatxo'janing yordamchisiman. Sizga qanday yordam bera olaman?")
        return

    # 3. Qolgan maxsus savol-javoblar (o'zgarishsiz, joyida)
    if t in ["assalomu alaykum", "assalomu alaykum!"]:
        await message.reply_text("Vaalaykum assalom! Yaxshimisiz? Qanday yordam bera olaman?")
    elif t == "qalesiz":
        await message.reply_text("Qichuu😎")
    elif t == "qanday":
        await message.reply_text("Qichuu😎")
    elif t == "nima gap":
        await message.reply_text("Tinch, o'zingizda nima gaplar?")
    elif t == "qayerdasan":
        await message.reply_text("Dubaida🏖️")
    elif t in ["kimsan", "isming nima", "ismiz nima"]:
        await message.reply_text("Azamat Abduraimov")
    elif t in ["chit bormi", "mod bormi"]:
        await message.reply_text("Kaneshna, @chit_oyinlarim shu kanalimda bor.")
    elif t == "azamat":
        await message.reply_text("Labbay?😊")
    elif t in ["rahmat", "raxmat"]:
        await message.reply_text("Arziydi, salomat bo'ling!🤝 👍")
    elif "prashivka" in t:
        await message.reply_text("Ha albatta! Prashivka qilgandan keyin telefon samalyot bo'ladi🔥. Narxini Azamatxo'ja aytadilar.")
    elif "narx" in t or "qancha" in t:
        await message.reply_text("Xizmatlar va mahsulotlar narxi haqida hozir Azamatxo'janing o'zlari aloqaga chiqib batafsil ma'lumot beradilar.")
    
    # 4. Mutlaqo boshqa begona gaplar yozilsa (Nechta, Nega va h.k.) — zaxira matn chiqadi
    else:
        await message.reply_text("Xabaringiz qabul qilindi, Azamatxo'ja hozir band edi😊, tez orada javob beramiz! Azamatakam yozadilar🤝")

if __name__ == "__main__":
    app.run()