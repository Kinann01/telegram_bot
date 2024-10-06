from telegram.ext import Updater, MessageHandler, Filters
from flask import Flask, request
import threading
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
KEYWORDS = ['casino', 'jackpot', '2000$', '1000$', '500$', '300$', '200$', '100$', 'Казино', 'ставка', 'слоты', 'джекпот', 'kазино']

def delete_casino_messages(update, context):
    if update.message is not None:
        message_text = update.message.text or update.message.caption
        if message_text:
            message_text = message_text.lower()
            if any(keyword in message_text for keyword in KEYWORDS):
                try:
                    update.message.delete()
                except Exception as e:
                    pass

PORT = int(os.getenv("PORT", "5000"))

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive", 200

def run_bot():
    updater = Updater(TOKEN, use_context=True)    
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text | Filters.caption & Filters.chat_type.groups, delete_casino_messages))

    if os.getenv("RENDER_EXTERNAL_HOSTNAME"):
        webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=webhook_url)
    else:
        updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    app.run(host="0.0.0.0", port=PORT)
