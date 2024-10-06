from telegram.ext import Updater, MessageHandler, Filters
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
KEYWORDS = ['casino', 'jackpot', '2000$', '1000$', '500$', '300$', '200$', '100$', 'Казино', 'ставка', 'слоты', 'джекпот', 'kазино']

# Function to delete messages containing keywords
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

def main():
    updater = Updater(TOKEN, use_context=True)    
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text | Filters.caption & Filters.chat_type.groups, delete_casino_messages))

    if os.getenv("RENDER_EXTERNAL_HOSTNAME"):
        webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=webhook_url)
        
        from http.server import BaseHTTPRequestHandler, HTTPServer
        
        class HealthCheckHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == "/":
                    self.send_response(200)
                    self.send_header("Content-type", "text/plain")
                    self.end_headers()
                    self.wfile.write(b"Bot is running!")

        # Start HTTP server for health check
        httpd = HTTPServer(("0.0.0.0", PORT), HealthCheckHandler)
        httpd.serve_forever()

    else:
        # Running locally, use polling
        updater.start_polling()

    # Keep running the bot
    updater.idle()

if __name__ == '__main__':
    main()
