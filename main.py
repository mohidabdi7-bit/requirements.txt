import os
import telebot
from google import genai

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_KEY)

SALMAN_SYSTEM_PROMPT = """
تو دستیار هوشمند «سلمان» در کانون فرهنگی کبوتران مسجد (@kabutarmasjed) هستی.
مخاطبان: دانشجویان علوم پزشکی و پیراپزشکی.
وظیفه: راهنمایی فکری، کلامی، معرفتی و پاسخ به چالش‌های روزانه.
لحن: صمیمی، حکیمانه، علمی، دقیق و مستدل با ساختار شکیل.
"""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام و نور حاجی! 🕊️✨ دستیار سلمان آماده پاسخگویی است.")

@bot.message_handler(func=lambda msg: True)
def handle_chat(message):
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message.text,
            config={"system_instruction": SALMAN_SYSTEM_PROMPT, "temperature": 0.7}
        )
        bot.reply_to(message, response.text or "پاسخی دریافت نشد.")
    except Exception as e:
        bot.reply_to(message, f"خطا: {str(e)}")

if __name__ == "__main__":
    print("سلمان آنلاین شد!")
    bot.infinity_polling()
