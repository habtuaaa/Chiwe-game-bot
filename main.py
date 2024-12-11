import os
import telebot
from dotenv import load_dotenv
from signup import signup, login
from deposit import deposit_handler
from game import place_bet, start_game, close_game, users
from utils import load_users, save_users
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("No API_TOKEN found. Please set it in your .env file.")
bot = telebot.TeleBot(API_TOKEN)

users = load_users()

# Welcome message with 'Play' button
@bot.message_handler(commands=["start"])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Play", callback_data="play"))
    bot.send_message(message.chat.id, "Welcome to Chiwe Bot Game!", reply_markup=markup)

# Callback query handler for all buttons
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "play":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Sign Up", callback_data="signup"))
        markup.add(InlineKeyboardButton("Log In", callback_data="login"))
        bot.send_message(call.message.chat.id, "Choose an option:", reply_markup=markup)
    elif call.data == "signup":
        signup(bot, call.message, users)
    elif call.data == "login":
        login(bot, call.message, users)
    elif call.data == "start_game":
        start_game()
        bot.send_message(call.message.chat.id, "The game has started! You can place your bets now.")
    elif call.data == "place_bet":
        select_numbers(call.message)
    elif call.data == "confirm_bet":
        bot.send_message(call.message.chat.id, "Congrats! You have placed your bet. 🥳 Please wait 30 seconds for the result...")
        time.sleep(30)  # Simulate countdown
        close_game(bot)
        bot.send_message(call.message.chat.id, "The game has been closed. Checking results...")
    elif call.data.startswith("num_"):
        number = int(call.data.split("_")[1])
        handle_number_selection(call.message, number)
    elif call.data == "close_game":
        handle_close_game(call.message)
    elif call.data == "exit":
        on_exit(call.message)

# Function to select numbers in a grid layout
def select_numbers(message):
    markup = InlineKeyboardMarkup(row_width=5)
    buttons = []
    for i in range(1,101):  # Adjust the range as needed
        buttons.append(InlineKeyboardButton(str(i), callback_data=f"num_{i}"))
    markup.add(*buttons)
    bot.send_message(message.chat.id, "Choose 5 random numbers:", reply_markup=markup)

# Handler for number selection
selected_numbers = {}

def handle_number_selection(message, number):
    user_id = message.chat.id
    if user_id not in selected_numbers:
        selected_numbers[user_id] = []
    if len(selected_numbers[user_id]) < 5:
        selected_numbers[user_id].append(number)
        if len(selected_numbers[user_id]) == 5:
            confirm_bet(message)
        else:
            bot.send_message(message.chat.id, f"Number {number} added. Choose more numbers.")
    else:
        bot.send_message(message.chat.id, "You have already selected 5 numbers. Confirm your bet.")

# Function to confirm bet
def confirm_bet(message):
    user_id = message.chat.id
    numbers = selected_numbers[user_id]
    user_name = message.chat.username
    response = place_bet(user_name, user_id, numbers)
    bot.send_message(message.chat.id, response)
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Close Game", callback_data="close_game"))
    markup.add(InlineKeyboardButton("Exit", callback_data="exit"))
    bot.send_message(message.chat.id, f"You have entered your numbers successfully: {numbers}. You can now close the game or exit:", reply_markup=markup)

def handle_close_game(message):
    close_game(bot)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Try Again", callback_data="start_game"))
    bot.send_message(message.chat.id, "The game has been closed. Checking results...", reply_markup=markup)

def on_exit(message):
    save_users(users)
    bot.reply_to(message, "User data saved. Exiting bot.")

# Existing command handlers
@bot.message_handler(commands=["signup"])
def handle_signup(message):
    signup(bot, message, users)

@bot.message_handler(commands=["login"])
def handle_login(message):
    login(bot, message, users)

@bot.message_handler(commands=["deposit"])
def handle_deposit(message):
    deposit_handler(bot, message, users)

bot.polling()
