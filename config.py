import os
import json
import telebot
from dotenv import load_dotenv
from telebot.types import LabeledPrice
from utils import save_users, load_users

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
PAYMENT_PROVIDER_TOKEN = os.getenv("PAYMENT_PROVIDER_TOKEN")  # Ensure this is set in your .env file

bot = telebot.TeleBot(API_TOKEN)

users = load_users()

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Welcome! Please /signup or /login.")

@bot.message_handler(commands=["deposit"])
def deposit(message):
    chat_id = message.chat.id
    username = message.chat.username

    if username not in users:
        bot.reply_to(message, "You need to signup first.")
        return

    title = "Deposit Funds"
    description = "Add funds to your bot account"
    payload = f"deposit_{username}"
    currency = "ETB"
    prices = [LabeledPrice(label="Deposit Amount", amount=500 * 100)]
    bot.send_invoice(
        chat_id,
        title,
        description,
        payload,
        PAYMENT_PROVIDER_TOKEN,
        currency,
        prices,
        start_parameter="deposit",
        is_flexible=False
    )

@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message):
    username = message.chat.username
    payment_info = message.successful_payment

    amount = payment_info.total_amount / 100
    currency = payment_info.currency

    if username in users:
        users[username]["balance"] = users.get(username, {}).get("balance", 0) + amount
        save_users(users)
        bot.reply_to(message, f"Payment successful! {amount:.2f} {currency} has been added to your account. New balance: {users[username]['balance']:.2f} {currency}.")
    else:
        bot.reply_to(message, "User not found.")

bot.polling()
