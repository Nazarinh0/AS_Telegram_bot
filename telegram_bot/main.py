import telebot
from telebot.types import LabeledPrice, ShippingOption

token = '5421084248:AAH7AV2izEqgcgeWeyzOySFO4llPzujluls'
provider_token = '381764678:TEST:38849'
bot = telebot.TeleBot(token)

prices = [LabeledPrice(label='Аккаунт заряженный №1', amount=1500000), LabeledPrice('Мануал по созданию аккаунта', 500000)]

shipping_options = [
    ShippingOption(id='instant', title='WorldWide Teleporter').add_price(LabeledPrice('Teleporter', 1000)),
    ShippingOption(id='pickup', title='Local pickup').add_price(LabeledPrice('Pickup', 300))]


@bot.message_handler(commands=['start'])
def start(message):
    text = f'''
        Привет, <b>{message.from_user.first_name}</b> <b>{message.from_user.last_name}</b>
Здесь Вы можете приобрести аккаунты для различных площадок, либо мануалы по созданию собственного аккаунта
Напишите <b>/buy</b> чтобы сделать покупку
    '''
    bot.send_message(message.chat.id, text, parse_mode = 'html' )


@bot.message_handler(commands=['buy'])
def buy(message):
    bot.send_invoice(
        message.chat.id,  # chat_id
        'Аккаунт заряженный №1',  # title
        ' Хотите бизнес, но не можете? Наш аккаунт Вам поможет!',  # description
        'ЧТО ЭТО ЗА ТЕКСТ??',  # invoice_payload
        provider_token,  # provider_token
        'rub',  # currency
        prices,  # prices
        photo_url='http://i.ytimg.com/vi/6FrC2-1OMUA/maxresdefault.jpg',
        photo_height=250,  # !=0/None or picture won't be shown
        photo_width=250,
        photo_size=512,
        is_flexible=False,  # True If you need to set up Shipping Fee
        start_parameter='lol')


@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    print(shipping_query)
    bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                              error_message='Все плохо, попробуйте позже, может заработает')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Ох, у нас чуть не угнали данные Вашей карты, но мы все защитили"
                                                " Попробуйте оплатить попозже, нам надо передохнуть")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,
                     'Ураа! Поздравляем, Вы приобрели супераккаунт!'
                     'Не бойтесь, когда-нибудь Вы его обязательно получите в своё распоряжение'.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')


# def get_user_text(message):
#     bot.send_message(message.chat.id, text, parse_mode='html')


bot.infinity_polling(skip_pending = True)
