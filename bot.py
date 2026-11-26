import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "".join(os.environ.get("BOT_TOKEN", "").split())

app = Flask(__name__)

telegram_app = Application.builder().token(BOT_TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Welcome to my bot!\n\nSend me a video."
    )


async def receive_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Video received!\n\n"
        f"File ID:\n{update.message.video.file_id}"
    )


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(
    MessageHandler(filters.VIDEO, receive_video)
)


@app.route("/")
def home():
    return "Telegram bot is running!"


if __name__ == "__main__":
    import asyncio
    from waitress import serve

    async def main():
        print("Starting Telegram bot...")
        print("Token found:", bool(BOT_TOKEN))
        print("Token length:", len(BOT_TOKEN))

        await telegram_app.initialize()

        print("Telegram connection successful!")

        await telegram_app.start()

        print("Starting web server...")

        serve(
            app,
            host="0.0.0.0",
            port=int(os.environ.get("PORT", 10000))
        )

    asyncio.run(main())
