import sqlite3
import csv
from datetime import datetime
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler
from telegram.utils.request import Request

TOKEN = "your bot token"
PROXY_URL = "proxy"


DB_FILE = "messages.db"
CSV_FILE = "messages.csv"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            text TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_message(username, text):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (username, text, timestamp) VALUES (?, ?, ?)", 
                   (username, text, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def export_to_csv():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages")
    rows = cursor.fetchall()
    conn.close()

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "username", "text", "timestamp"])
        writer.writerows(rows)

def handle_message(update: Update, context: CallbackContext):
    user = update.message.from_user
    text = update.message.text
    print(f"[{user.username}] {text}")

    save_message(user.username, text)

def export_command(update: Update, context: CallbackContext):
    print("export command triggered")
    export_to_csv()
    with open(CSV_FILE, "rb") as f:
        update.message.reply_document(f, filename=CSV_FILE)

def main():
    init_db()  

    updater = Updater(
        token=TOKEN,
        use_context=True,
    )

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(CommandHandler("export", export_command))

    print("Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
