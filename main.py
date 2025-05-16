from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import requests

API_KEY = ""
BOT_TOKEN = ""

GEN_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

async def generate_gemini_reply(user_msg: str) -> str:
    data = {
        "systemInstruction": {
            "parts": [
                {
                    "text": (
                        "Lo asisten asik, goblok tapi pinter yang jawab semua pake bahasa informal, santai, style jokes bapak bapak fesbuk, penuh meme, kadang pake bahasa Jawa dan logat wibu tapi tetep informatif."
                        "Utamakan 35% misuh, tapi sopan dan tetep nyambung. Maks 5-7 kata tiap jawab. Contoh gaya kayak: 'cih mantap', 'hahaa.. kok iso suu badjingann😂', "
                        "'xixi ngakak abiezz..', 'mendink turu cik🗿'. Jangan manggil pak/ndoro/ndan."
                    )
                }
            ]
        },
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": user_msg
                    }
                ]
            }
        ]
    }
    headers = {"Content-Type": "application/json"}

    try:
        resp = requests.post(GEN_URL, headers=headers, json=data)
        resp.raise_for_status()
        result = resp.json()
        if "candidates" in result:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "Maaf cok, respons Gemini gak ada 'contents' nya."
    except Exception as e:
        return f"sorry cok, Gemini error: {e}"

async def reply_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    reply = await generate_gemini_reply(user_msg)
    await update.message.reply_text(reply)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Jangan tekan ini 💩", callback_data='bosan')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Yo!                                       .",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'bosan':
        reply = await generate_gemini_reply("coba sapa gw bro")
        await query.message.reply_text(reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_chat))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot running...")
    app.run_polling()
