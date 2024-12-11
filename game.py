import random
import time

GAME_RANGE = (1, 100)
PRICE_PER_NUMBER = 1
BETTING_TIME = 300
ADMIN_FEE_PERCENT = 30

users = {}
prize_pool = 0

def start_game():
    global users, prize_pool
    users = {}
    prize_pool = 0
    print("New game started")
    # Simulate betting time for demonstration purposes (replace this with actual timing logic)
    time.sleep(BETTING_TIME)
    close_game()

def place_bet(user_name, chat_id, numbers):
    global prize_pool
    if len(numbers) > 5:
        return "You can only choose up to 5 numbers."
    for num in numbers:
        if num < GAME_RANGE[0] or num > GAME_RANGE[1]:
            return f"Number {num} is out of range. Choose numbers between {GAME_RANGE[0]} and {GAME_RANGE[1]}."
    payment = len(numbers) * PRICE_PER_NUMBER
    if user_name not in users:
        users[user_name] = {"numbers": [], "paid": 0, "chat_id": chat_id}
    users[user_name]["numbers"].extend(numbers)
    users[user_name]["paid"] += payment
    prize_pool += payment
    return f"Bet placed! You chose {numbers}."


def close_game(bot):
    global users, prize_pool
    
    if not users:
        print("No bets placed this round. Game canceled.")
        return

    winning_number = random.randint(*GAME_RANGE)
    print(f"The winning number is: {winning_number}")
    winners = [user for user, data in users.items() if winning_number in data["numbers"]]

    total_prize = prize_pool
    admin_fee = (ADMIN_FEE_PERCENT / 100) * total_prize
    prize_after_fee = total_prize - admin_fee

    if not winners:
        print(f"No winners this round. Admin fee: ${admin_fee:.2f}. Prize pool after admin fee: ${prize_after_fee:.2f}.")
        for user, data in users.items():
            chat_id = data["chat_id"]
            print(f"Sending message to {chat_id}: No winners this round. The winning number was: {winning_number}.")  # Debugging
            bot.send_message(chat_id, f"No winners this round. The winning number was: {winning_number}.")
    else:
        winner_share = prize_after_fee / len(winners)
        print(f"Admin fee: ${admin_fee:.2f}. Prize pool after admin fee: ${prize_after_fee:.2f}.")
        for winner, data in users.items():
            if winner in winners:
                chat_id = data["chat_id"]
                print(f"Sending message to {chat_id}: Congratulations! You won ${winner_share:.2f}.")  # Debugging
                bot.send_message(chat_id, f"Congratulations! The winning number is {winning_number}. You won ${winner_share:.2f}!")
    
    # Notify all users about the winning number
    for user, data in users.items():
        chat_id = data["chat_id"]
        print(f"Sending message to {chat_id}: The winning number was: {winning_number}.")  # Debugging
        bot.send_message(chat_id, f"The winning number was: {winning_number}.")

