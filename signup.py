import json
from utils import save_users  # Ensure this import is included
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def signup(bot, message, users):
    msg = bot.reply_to(message, "Enter username:")
    bot.register_next_step_handler(msg, process_signup_username, bot, users)

def process_signup_username(message, bot, users):
    username = message.text
    if username in users:
        bot.reply_to(message, "This username is already taken. Try again.")
        return
    msg = bot.reply_to(message, "Enter your password:")
    bot.register_next_step_handler(msg, process_signup_password, username, bot, users)

def process_signup_password(message, username, bot, users):
    password = message.text
    users[username] = {"password": password, "balance": 0}  # Ensure balance is initialized
    save_users(users)
    bot.reply_to(message, "Registration successful! You can now login.")

def login(bot, message, users):
    msg = bot.reply_to(message, "Enter username:")
    bot.register_next_step_handler(msg, process_login_username, bot, users)

def process_login_username(message, bot, users):
    username = message.text
    if username not in users:
        bot.reply_to(message, "Username not found. Please /signup first.")
        return
    msg = bot.reply_to(message, "Enter your password:")
    bot.register_next_step_handler(msg, process_login_password, username, bot, users)

def process_login_password(message, username, bot, users):
    password = message.text
    if users[username]["password"] == password:
        bot.reply_to(message, "Login successful! Welcome back.")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Place Bet", callback_data="place_bet"))
        bot.send_message(message.chat.id, "You can now place your bet:", reply_markup=markup)
    else:
        bot.reply_to(message, "Incorrect password! Please try again.")
