import telebot
import os
from telebot import types # расширенные возможности (клавиатура)
from config import exchanges
from extensions import Converter, ApiException

bot = telebot.TeleBot(os.getenv('CRYPTO_BOT_TOKEN')) # получение доступа к боту

def create_markup(base = None): # в качестве аргумента указана валюта, которую необходимо скрыть после выбора пользователем
    """Клавиатура"""
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # создаем объект клавиатуры, сворачиваем подложку после клика
    buttons = []
    for val in exchanges.keys():
        if val != base:
            buttons.append(types.KeyboardButton(val.capitalize()))  # добавление кнопок клавиатуры в список
    markup.add(*buttons) # передаём кнопки в клавиатуру
    return markup


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = f"""Здравствуйте, {message.from_user.first_name}!\U0001F60A
    
Меня зовут Карри, я бот для перевода валюты\U0001F4B8

Для начала работы введите команду /convert"""
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    """Обработчик, возращающий тип валюты, доступной для перевода."""
    text = 'Доступные валюты: \n'
    for i in exchanges.keys(): # проходимся по ключам словаря и выводим значения с новой строчки
        text = '\n'.join((text, i)) # каждая новая валюта переносится на новую строку
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = 'Выберите базовую валюту\U00002B07'
    bot.send_message(message.chat.id, text, reply_markup=create_markup()) # reply_markup - отправление клавиатуры
    bot.register_next_step_handler(message, base_handler)  # регистрация обработчика на следующее сообщение. Если этот же пользователь в этом же чате напишет сообщение, то бот это сообщение передаёт в указанную функцию

def base_handler(message: telebot.types.Message):
    base = message.text.strip().lower()
    text = 'Выберите котируемую валюту\U00002B07'
    bot.send_message(message.chat.id, text, reply_markup=create_markup(base))
    bot.register_next_step_handler(message, sym_handler, base)

def sym_handler(message: telebot.types.Message, base):
    sym = message.text.strip()
    text = 'Введите количество конвертируемой валюты\U00002B07'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, sym)

def amount_handler(message: telebot.types.Message, base, sym):
    amount = message.text.strip()
    try:
        new_price = Converter.get_price(base, sym, amount)
    except ApiException as e:
        bot.send_message(message.chat.id, f"Ошибка конвертации: \n{e}")
    else:
        text = f"""Цена {amount} {base} в {sym.lower()} = {round(new_price, 2)}\n
Если Вы хотите продолжить работу, введите команду /convert\n
Всегда рад помочь!\U0001F609"""
        bot.send_message(message.chat.id, text)

if __name__ == "__main__":
    bot.polling() # запуск бота

