from utils import save_users

def deposit_handler(bot, message, users):
    msg = bot.reply_to(message, "Enter your username:")
    bot.register_next_step_handler(msg, process_deposit_username, bot, users)

def process_deposit_username(message, bot, users):
    username = message.text    
    if username not in users:
        bot.reply_to(message, "User not found. Please signup first.")
        return
    
    msg = bot.reply_to(message, "Enter the amount to deposit:")
    bot.register_next_step_handler(msg, process_deposit_amount, username, bot, users)

def process_deposit_amount(message, username, bot, users):
    try:
        amount = float(message.text)
        if amount <= 0:
            bot.reply_to(message, "Please enter a valid amount greater than zero.")
            return
        if "balance" not in users[username]:
            users[username]["balance"] = 0
        users[username]["balance"] += amount
        save_users(users)
        bot.reply_to(message, f"${amount:.2f} deposited successfully! New balance: ${users[username]['balance']:.2f}")
    except ValueError:
        bot.reply_to(message, "Invalid amount. Please enter a valid number.")
