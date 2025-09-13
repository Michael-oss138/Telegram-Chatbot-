import httpx
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

TOKEN = "your token"
PROXY_URL = "proxy"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    print(f"[{user.username}] {text}")

def main():

    client = httpx.AsyncClient(proxies=PROXY_URL)

    request = HTTPXRequest(httpx_client=client)

    app = Application.builder().token(TOKEN).request(request).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
