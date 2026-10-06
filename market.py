import os
import telebot

# Get bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ Bot ishlayapti!")


if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
