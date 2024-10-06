from telegram.ext import Updater, MessageHandler, Filters
import os
from flask import Flask
import threading

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
KEYWORDS = ['casino', 'jackpot', '2000$', '1000$', '500$', '300$', '200$', '100$', 'Казино', 'ставка', 'слоты', 'джекпот', 'kазино']

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!", 200

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

def run_flask():
    app.run(host='0.0.0.0', port=PORT)

def main():
    updater = Updater(TOKEN, use_context=True)    
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text | Filters.caption & Filters.chat_type.groups, delete_casino_messages))

    if os.getenv("RENDER_EXTERNAL_HOSTNAME"):
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}")
    else:
        updater.start_polling()

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    updater.idle()

if __name__ == '__main__':
    main()