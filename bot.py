import os
from pyrogram import Client, filters

SESSION_STRING = os.getenv("SESSION_STRING")

app = Client("my_userbot", session_string=SESSION_STRING)

# filters.private & ~filters.me & ~filters.bot -> Faqat shaxsiy xabarlarga javob beradi, o'zingizga va boshqa BOTLARGA javob bermaydi!
@app.on_message(filters.private & ~filters.me & ~filters.bot) 
async def hello_handler(client, message):
    if not message.text:
        await message.reply_text("Assalomu alaykum! Men Azamatxo'janing yordamchisiman. Sizga qanday yordam bera olaman?")
        return

    t = message.text.lower().strip()

    # 1. Maxsus aniq savol-javoblar
    if t in ["assalomu alaykum", "salom!", "assalomu alaykum!"]:
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

    # 2. Agar yuqoridagilardan mutlaqo boshqa begona gap yozilsa, srazi shu javob chiqadi:
    else:
        await message.reply_text("Xabaringiz qabul qilindi, Azamatxo'ja hozir band edi😊, tez orada javob beramiz! Azamatakam yozadilar🤝")

if __name__ == "__main__":
    app.run()