import telebot

bot = telebot.TeleBot("7635770061:AAHFybSa5rn8T8pmQjFBn7HvNzLY6lzyLWs")

@bot.message_handler(commands=["start"])
def send_welcome(massage):
    bot.send_message(massage,"hi")

bot.infinity_polling();