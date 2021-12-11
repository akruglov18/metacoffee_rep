# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 21:32:23 2021

@author: Super-puper team
"""
import telebot
from telebot import types

bot = telebot.TeleBot('5009339889:AAEhnKB0qSyQECs5g4wHsEOo0ppJTv6g8P4')

orders = dict()
order = {
    'coffee': None,
    'pattern': None,
    'address': None
}

commands = ['/help', '/order']
messages = ['привет', 'пока', 'павел гандон']

main_menu = types.InlineKeyboardMarkup()
main_menu.row_width = 3
main_menu.add(types.InlineKeyboardButton(text='Выбрать кофе', callback_data='1choose_coffee'))
main_menu.add(types.InlineKeyboardButton(text='Выбрать узор', callback_data='2choose_pattern'))
main_menu.add(types.InlineKeyboardButton(text='Ввести адрес доставки', callback_data='3input_address'))
main_menu.add(types.InlineKeyboardButton(text='Оформить заказ', callback_data='4create_order'))
main_menu.add(types.InlineKeyboardButton(text='Отменить заказ', callback_data='5cansel_order'))

def normalize(text):
    text = text.lower()
    text = ' '.join(text.split())
    return text

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global commands, messages, orders
    # нужно предотвратить обработку когда есть кнопки
    text = normalize(message.text)
    if text in commands:
        parse_command(message)
    elif text in messages:
        parse_message(message)
    else:
        bot.send_message(message.from_user.id, "Я вас не понимаю. Напишите /help.")

def parse_command(command):
    global commands, messages
    text = normalize(command.text)
    if text == '/help':
        str_commands = ''
        for comm in commands:
            str_commands += comm + ', '
        str_messages = ''
        for mess in messages:
            str_messages += mess + ', '
        bot.send_message(command.from_user.id, 'Распознаваемые команды: ' + str_commands + ' Распознаваемые сообщения: ' + str_messages)
    elif text == '/order':
        orders[command.from_user.id] = order
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='0yes')
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='0no')
        keyboard.add(key_yes)
        keyboard.add(key_no)
        bot.send_message(command.from_user.id, text='Хотите сделать заказ?', reply_markup=keyboard)

def parse_message(message):
    text = normalize(message.text)
    if text == 'привет':
        bot.send_message(message.from_user.id, 'Че надо')
    elif text == 'пока':
        bot.send_message(message.from_user.id, 'Больше мне не пиши')
    elif text == 'павел гандон':
        bot.send_message(message.from_user.id, 'Истинно так')

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global orders, order, main_menu
    if call.data[0] == '0':
        # создание заказа
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
        if call.data[1:] == 'yes':
            bot.send_message(call.message.chat.id, text='Оформление заказа', reply_markup=main_menu)
        elif call.data[1:] == 'no':
            bot.send_message(call.message.chat.id, 'Ну ладно :(')
    elif call.data[0] == '1':
        # выбираем кофе
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
        if call.data[1:] == 'choose_coffee':
            # создаем кнопки для выбора кофе
            bot.send_message(call.message.chat.id, text='На данный момент кофе нету')
        elif call.data[1:] == 'coffee_1':
            # записываем выбранное кофе в заказ
            orders[call.from_user.id]['coffee'] = 'russian_coffee_1'
            bot.send_message(call.message.chat.id, text='Оформление заказа', reply_markup=main_menu)
        elif call.data[1:] == 'coffee_2':
            # и тд
            pass
    elif call.data[0] == '2':
        # выбираем узор
        # аналогично выбору кофе
        pass
    elif call.data[0] == '3':
        # вводим адрес
        # тут сложна, через кнопку не сделаешь
        # + еще парсить адрес
        pass
    elif call.data[0] == '4':
        # принимаем заказ
        if orders[call.message.chat.id]['coffee'] == None:
            bot.send_message(call.message.chat.id, 'Вы не выбрали кофе')
        elif orders[call.message.chat.id]['pattern'] == None:
            bot.send_message(call.message.chat.id, 'Вы не выбрали узор')
        elif orders[call.message.chat.id]['address'] == None:
            bot.send_message(call.message.chat.id, 'Вы не указали адрес доставки')
        else:
            bot.send_message(call.message.chat.id, 'Заказ принят')
            bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    elif call.data[0] == '5':
        # отменяем заказ
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)

bot.polling(none_stop=True, interval=0)
