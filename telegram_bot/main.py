import telebot

bot = telebot.TeleBot('5421084248:AAH7AV2izEqgcgeWeyzOySFO4llPzujluls')

@bot.message_handler(commands = ['start'])
def start(message):
    text = f'Привет, <b>{message.from_user.first_name}</b> <b>{message.from_user.last_name}</b>'
    bot.send_message(message.chat.id, text, parse_mode = 'html' )

def get_user_text(message):
    bot.send_message(message.chat.id, text, parse_mode='html')


bot.infinity_polling()
