import os
import telebot

# Get bot token and admin ID from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")

if not ADMIN_ID:
    raise ValueError("ADMIN_ID environment variable is not set")

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Products dictionary
PRODUCTS = {
    "100_gold": {"name": "100 GOLD", "price": "12,000 so'm"},
    "200_gold": {"name": "200 GOLD", "price": "23,000 so'm"},
    "500_gold": {"name": "500 GOLD", "price": "55,000 so'm"},
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Handle /start command and show main menu"""
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    market_btn = telebot.types.KeyboardButton("🛒 Market")
    support_btn = telebot.types.KeyboardButton("📞 Support")
    markup.add(market_btn, support_btn)
    
    bot.send_message(
        message.chat.id,
        "Assalomu alaikum! 👋\nMarket-Bot'ga xush kelibsiz!",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == "🛒 Market")
def show_products(message):
    """Show available products"""
    markup = telebot.types.InlineKeyboardMarkup()
    
    markup.add(telebot.types.InlineKeyboardButton(
        "100 GOLD — 12,000 so'm",
        callback_data="product_100_gold"
    ))
    markup.add(telebot.types.InlineKeyboardButton(
        "200 GOLD — 23,000 so'm",
        callback_data="product_200_gold"
    ))
    markup.add(telebot.types.InlineKeyboardButton(
        "500 GOLD — 55,000 so'm",
        callback_data="product_500_gold"
    ))
    
    bot.send_message(
        message.chat.id,
        "🛍️ Mahsulotlarni tanlang:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == "📞 Support")
def show_support(message):
    """Show support message"""
    bot.send_message(
        message.chat.id,
        "📞 Qo'llab-quvvatlash:\n\nSavollaringiz bo'lsa, biz bilan bog'laning: @support"
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("product_"))
def handle_product_selection(call):
    """Handle product selection"""
    product_id = call.data.replace("product_", "")
    
    if product_id in PRODUCTS:
        product = PRODUCTS[product_id]
        
        markup = telebot.types.InlineKeyboardMarkup()
        buy_btn = telebot.types.InlineKeyboardButton(
            "🛒 Sotib olish",
            callback_data=f"buy_{product_id}"
        )
        markup.add(buy_btn)
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"Siz tanlagan mahsulot:\n\n{product['name']}\n💰 Narx: {product['price']}",
            reply_markup=markup
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def handle_buy_button(call):
    """Handle buy button click"""
    product_id = call.data.replace("buy_", "")
    
    if product_id in PRODUCTS:
        bot.send_message(
            call.message.chat.id,
            "Iltimos, o'z Telegram foydalanuvchi nomingizni kiriting:\n(Masalan: @username)"
        )
        
        # Store product ID for next step
        bot.register_next_step_handler(
            call.message,
            process_username,
            product_id
        )


def process_username(message, product_id):
    """Process username input and send order to admin"""
    username = message.text.strip()
    product = PRODUCTS[product_id]
    
    # Create order message for admin
    order_message = (
        f"📦 Yangi buyurtma!\n\n"
        f"Mahsulot: {product['name']}\n"
        f"Narx: {product['price']}\n"
        f"Foydalanuvchi: {username}\n"
        f"User ID: {message.from_user.id}"
    )
    
    try:
        # Send order to admin
        bot.send_message(ADMIN_ID, order_message)
        
        # Send confirmation to user
        bot.send_message(
            message.chat.id,
            f"✅ Sizning buyurtma admin'ga yuborildi!\n\n"
            f"Mahsulot: {product['name']}\n"
            f"Narx: {product['price']}\n"
            f"Telegram: {username}\n\n"
            f"Admin tez orada siz bilan bog'lanadi."
        )
    except Exception as e:
        bot.send_message(
            message.chat.id,
            "❌ Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring."
        )
        print(f"Error sending order to admin: {e}")


if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
