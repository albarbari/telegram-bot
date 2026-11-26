import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ["BOT_TOKEN"]

app = Flask(__name__)
telegram_app = Application.builder().token(BOT_TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Welcome to my bot!\n\n"
        "Send me a video."
    )


async def receive_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video

    await update.message.reply_text(
        "✅ Video received!\n\n"
        "File ID:\n" + video.file_id
    )


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(
    MessageHandler(filters.VIDEO, receive_video)
)


@app.route("/", methods=["GET"])
def home():
    return "Telegram bot is running!"


@app.route("/webhook", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return "OK"


if __name__ == "__main__":
    import asyncio

    async def main():
        await telegram_app.initialize()
        await telegram_app.start()

        from waitress import serve
        serve(
            app,
            host="0.0.0.0",
            port=int(os.environ.get("PORT", 10000))
        )

    asyncio.run(main())
