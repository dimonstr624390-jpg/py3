from random import choice
import telebot
from config import token

API_TOKEN = token
bot = telebot.TeleBot(API_TOKEN)
message_count = 0

class Car:
    def __init__(self, brand, color):
        self.brand = brand 
        self.color = color 

    def info(self):
        return f"Робот собрал машину!\nМарка: {self.brand}\nЦвет: {self.color}"

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Привет, если ты что-то скажешь, то я повторю это! Кстати, у меня есть и другие команды:\n/info - все сообщения, который обработал бот\n/car - распредилитель классов по образцу машины, бот обрабатывает информацию, которую дал пользователь, вставляя её в своё сообщения, делая более красивое представлние характеристик данного автомобиля(Например, после призыва команды, бот выдаёт нам оповещение, что нужно дать машине марку и цвет. После того, как мы, например, написали, что машина марки Toyota и цвет у неё красный, бот обрабатывает данную информацию и выдаёт в своём сообщении. )")

@bot.message_handler(commands=['info'])
def send_info(message):
    global message_count
    bot.reply_to(message, f"Всего обработано сообщений: {message_count}")

@bot.message_handler(commands=['coin'])
def coin_handler(message):
    coin = choice(["ОРЕЛ", "РЕШКА"])
    bot.reply_to(message, coin)

@bot.message_handler(commands=['car'])
def handle_car_command(message):
    arguments = telebot.util.extract_arguments(message.text)

    if not arguments:
        bot.reply_to(
            message,
            'Пожалуйста, укажите марку и цвет. Пример: `/car Toyota Красный`',
            parse_mode='Markdown',
        )
        return

    args_list = arguments.split(maxsplit=1)

    if len(args_list) < 2:
        bot.reply_to(
            message,
            'Недостаточно данных! Введите и марку, и цвет через пробел.',
        )
        return

    brand = args_list[0]
    color = args_list[1]

    my_car = Car(brand=brand, color=color)
    bot.send_message(message.chat.id, my_car.info())


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    global message_count
    message_count += 1
    bot.reply_to(message, message.text)


if __name__ == '__main__':
    bot.infinity_polling()
