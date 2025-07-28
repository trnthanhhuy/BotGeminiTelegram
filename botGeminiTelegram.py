import logging
import requests
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ===== CONFIG =====
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TKOEN_HERE"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

# ===== TẢI TÍNH CÁCH BAN ĐẦU =====
with open("prestart.txt", "r", encoding="utf-8") as f:
    personality_prompt = f.read()

# ===== LOGGING =====
logging.basicConfig(level=logging.INFO)

# ===== GỬI YÊU CẦU TỚI GEMINI =====
def send_gemini_request(messages):
    headers = {
        "Content-Type": "application/json",
    }
    body = {
        "contents": [
            {"role": "user", "parts": [{"text": personality_prompt}]},
            {"role": "user", "parts": [{"text": messages}]}
        ]
    }
    response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(body))
    if response.status_code == 200:
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"☠️ Lỗi gọi API: {response.status_code} - {response.text}"

# ===== HANDLERS =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎉 Bot đã sẵn sàng ")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    chat_id = update.effective_chat.id

    try:
        reply = send_gemini_request(user_input)
    except Exception as e:
        reply = f"☠️ Lỗi rồi anh ui: {e}"

    await context.bot.send_message(chat_id=chat_id, text=reply)

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("✅ Bot Gemini khởi động xong, đã nạp tính cách từ prestart.txt ✨")
    app.run_polling()

if __name__ == "__main__":
    main()
