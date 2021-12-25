# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 21:32:23 2021

@author: Super-puper team
"""
import telebot
from telebot import types

bot = telebot.TeleBot('5017063566:AAGWqHQ0p4RbSehjSoDqftkZItILv_hL9Ng')

orders = dict()
order = {
    'coffee': None,
    'pattern': None,
    'address': None,
    'time': 0,
    'isorder': None
}
chat_state = 'Main_menu'
commands = ['/help', '/order']
messages = ['привет', 'пока', 'павел гандон']

main_menu = types.InlineKeyboardMarkup()
main_menu.row_width = 3
main_menu.add(types.InlineKeyboardButton(text='Выбрать кофе', callback_data='1choose_coffee'))
main_menu.add(types.InlineKeyboardButton(text='Выбрать узор', callback_data='2choose_pattern'))
main_menu.add(types.InlineKeyboardButton(text='Ввести адрес доставки', callback_data='3enter_address'))
main_menu.add(types.InlineKeyboardButton(text='Ввести время доставки', callback_data='4choose_time'))
main_menu.add(types.InlineKeyboardButton(text='Оформить заказ', callback_data='5create_order'))
main_menu.add(types.InlineKeyboardButton(text='Отменить заказ', callback_data='6cansel_order'))

def normalize(text):
    text = text.lower()
    text = ' '.join(text.split())
    return text

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global commands, messages, orders,chat_state
    if chat_state == 'Main_menu':
        if message.from_user.id in orders.keys():
            if orders[message.from_user.id]['isorder'] == True:
                return
        text = normalize(message.text)
        if text in commands:
            parse_command(message)
        elif text in messages:
            parse_message(message)
        else:
            bot.send_message(message.from_user.id, "Я вас не понимаю. Напишите /help.")
    elif chat_state == 'Address':
        text = message.text
        if(check_adress(text)):
            orders[message.from_user.id]['address']=text
            chat_state = 'Main_menu'


def check_adress(line):
    if line == None :
        return False
    lst = line.split(' ')
    if len(lst) != 3:
        return False
    counter_dig = []
    counter_let = []
    for word in lst:
        cnt_l = 0
        cnt_d = 0
        for char in word:
          cnt_l += char.isalpha()
          cnt_d += char.isdigit()
        counter_dig.append(cnt_d)
        counter_let.append(cnt_l)
    return (counter_dig[0]==0 and counter_dig[1]==0 and counter_let[2]==0)


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
        orders[command.from_user.id]['isorder'] = True
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='0yes')
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='0no')
        keyboard.add(key_yes)
        keyboard.add(key_no)
        bot.send_message(command.from_user.id, text='Хотите сделать заказ?', reply_markup=keyboard)

# убрать/закодировать павла + всякий текст
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
    global orders, order, main_menu,chat_state
    if call.data[0] == '0':
        # создание заказа
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
        if call.data[1:] == 'yes':
            bot.send_message(call.message.chat.id, text='Оформление заказа', reply_markup=main_menu)
        elif call.data[1:] == 'no':
            orders.pop(call.from_user.id)
            bot.send_message(call.message.chat.id, 'Ну ладно :(')
    elif call.data[0] == '1':
        # выбираем кофе
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
        if call.data[1:] == 'choose_coffee':
            choose_coffe = types.InlineKeyboardMarkup()
            choose_coffe.add(types.InlineKeyboardButton(text='Латте',           callback_data='1coffee_1'))
            choose_coffe.add(types.InlineKeyboardButton(text='Эспрессо',        callback_data='1coffee_2'))
            choose_coffe.add(types.InlineKeyboardButton(text='Мокко',           callback_data='1coffee_3'))
            choose_coffe.add(types.InlineKeyboardButton(text='Капучино',        callback_data='1coffee_4'))
            choose_coffe.add(types.InlineKeyboardButton(text='Горячий шоколад', callback_data='1coffee_5'))
            bot.send_message(call.from_user.id, text='Выберите кофе', reply_markup=choose_coffe)
        elif call.data[1:] == 'coffee_1':
            orders[call.from_user.id]['coffee'] = 'Латте'
            bot.send_message(call.message.chat.id, text='Оформление заказа', reply_markup=main_menu)
        elif call.data[1:] == 'coffee_2':
            orders[call.from_user.id]['coffee'] = 'Эспрессо'
            bot.send_message(call.message.chat.id, text='Оформление заказа', reply_markup=main_menu)
        elif call.data[1:] == 'coffee_3':
            orders[call.from_user.id]['coffee'] = 'Мокко'
            bot.send_message(call.message.chat.id, text='Оформление заказа', reply_markup=main_menu)
        elif call.data[1:] == 'coffee_4':
            orders[call.from_user.id]['coffee'] = 'Капучино'
            bot.send_message(call.message.chat.id, text='Оформление заказа', reply_markup=main_menu)
        elif call.data[1:] == 'coffee_5':
            orders[call.from_user.id]['coffee'] = 'Горячий шоколад'
            bot.send_message(call.message.chat.id, text='Оформление заказа', reply_markup=main_menu)
    elif call.data[0] == '2':
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
        if call.data[1:] == 'choose_pattern':
            choose_pattern = types.InlineKeyboardMarkup()
            choose_pattern.add(types.InlineKeyboardButton(text='Сердечко',      callback_data='2pattern_1'))
            choose_pattern.add(types.InlineKeyboardButton(text='Пейзаж',        callback_data='2pattern_2'))
            choose_pattern.add(types.InlineKeyboardButton(text='Лебедь',        callback_data='2pattern_3'))
            choose_pattern.add(types.InlineKeyboardButton(text='Смайлик',       callback_data='2pattern_4'))
            choose_pattern.add(types.InlineKeyboardButton(text='Без узора',     callback_data='2pattern_5'))
            bot.send_message(call.from_user.id, text='Выберите узор для кофе', reply_markup=choose_pattern)
        elif call.data[1:] == 'pattern_1':
            orders[call.from_user.id]['pattern'] = 'Сердечко'
            bot.send_message(call.message.chat.id, text='Оформление заказа', reply_markup=main_menu)
        elif call.data[1:] == 'pattern_2':
            orders[call.from_user.id]['pattern'] = 'Пейзаж'
            bot.send_message(call.message.chat.id, text='Оформление заказа', reply_markup=main_menu)
        elif call.data[1:] == 'pattern_3':
            orders[call.from_user.id]['pattern'] = 'Лебедь'
            bot.send_message(call.message.chat.id, text='Оформление заказа', reply_markup=main_menu)
        elif call.data[1:] == 'pattern_4':
            orders[call.from_user.id]['pattern'] = 'Смайлик'
            bot.send_message(call.message.chat.id, text='Оформление заказа', reply_markup=main_menu)
        elif call.data[1:] == 'pattern_5':
            orders[call.from_user.id]['pattern'] = 'Без узора'
            bot.send_message(call.message.chat.id, text='Оформление заказа', reply_markup=main_menu)
    elif call.data[0] == '3':
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
        print(call.data[1:])
        if call.data[1:] == 'enter_address':
            enter_address = types.InlineKeyboardMarkup()
            enter_address.add(types.InlineKeyboardButton(text='Ввести адрес самому',           callback_data='3enter_address_1'))
            enter_address.add(types.InlineKeyboardButton(text='Использовать геолокацию(доступно только на смартфонах)',callback_data='3enter_address_2',request_location=T))
            bot.send_message(call.from_user.id, text='Выберите как вы хотите ввести адрес', reply_markup=enter_address)
        elif(call.data[1:] == 'enter_address_1'):
            enter_address_man = types.InlineKeyboardMarkup()
            orders[call.from_user.id]['address']=None
            chat_state = 'Address'
            enter_address_man.add(types.InlineKeyboardButton(text='Принять',           callback_data='3enter_address_3'))
            bot.send_message(call.message.chat.id, text='Введите адрес в формате <Город> <Улица> <Дом>', reply_markup=enter_address_man)
        elif(call.data[1:] == 'enter_address_2'):
            bot.send_message(call.message.chat.id, text='Оформление заказа', reply_markup=main_menu)
        elif(call.data[1:] == 'enter_address_3'):
            if orders[call.from_user.id]['address'] == None:
                enter_address_man = types.InlineKeyboardMarkup()
                enter_address_man.add(types.InlineKeyboardButton(text='Принять',           callback_data='3enter_address_1'))
                bot.send_message(call.message.chat.id, text='Введите корректный адресс!', reply_markup=enter_address_man)
            else:
                bot.send_message(call.from_user.id, text='Оформление заказа', reply_markup=main_menu)

    elif call.data[0] == '4':
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
        choose_time = types.InlineKeyboardMarkup()
        choose_time.add(types.InlineKeyboardButton(text='+5 минут',           callback_data='4сhoose_time_1'))
        choose_time.add(types.InlineKeyboardButton(text='+15 минут',          callback_data='4сhoose_time_2'))
        choose_time.add(types.InlineKeyboardButton(text='+30 минут',          callback_data='4сhoose_time_3'))
        choose_time.add(types.InlineKeyboardButton(text='+45 минут',          callback_data='4сhoose_time_4'))
        choose_time.add(types.InlineKeyboardButton(text='+60 минут',          callback_data='4сhoose_time_5'))
        choose_time.add(types.InlineKeyboardButton(text='Завершить',          callback_data='4сhoose_time_6'))
        if call.data[1:] == 'choose_time':
            bot.send_message(call.from_user.id, text='Введите время', reply_markup=choose_time)
        elif call.data[1:] == 'сhoose_time_1':
            orders[call.from_user.id]['time'] = orders[call.from_user.id]['time'] + 5
            mes = 'Доставить вам кофе через ' + str(orders[call.from_user.id]['time']) + ' минут?'
            bot.send_message(call.message.chat.id, text='Ввод времени\n' + mes, reply_markup=choose_time)
        elif call.data[1:] == 'сhoose_time_2':
            orders[call.from_user.id]['time'] = orders[call.from_user.id]['time'] + 15
            mes = 'Доставить вам кофе через ' + str(orders[call.from_user.id]['time']) + ' минут?'
            bot.send_message(call.message.chat.id, text='Ввод времени\n' + mes, reply_markup=choose_time)
        elif call.data[1:] == 'сhoose_time_3':
            orders[call.from_user.id]['time'] = orders[call.from_user.id]['time'] + 30
            mes = 'Доставить вам кофе через ' + str(orders[call.from_user.id]['time']) + ' минут?'
            bot.send_message(call.message.chat.id, text='Ввод времени\n' + mes, reply_markup=choose_time)
        elif call.data[1:] == 'сhoose_time_4':
            orders[call.from_user.id]['time'] = orders[call.from_user.id]['time'] + 45
            mes = 'Доставить вам кофе через ' + str(orders[call.from_user.id]['time']) + ' минут?'
            bot.send_message(call.message.chat.id, text='Ввод времени\n' + mes, reply_markup=choose_time)
        elif call.data[1:] == 'сhoose_time_5':
            orders[call.from_user.id]['time'] = orders[call.from_user.id]['time'] + 60
            mes = 'Доставить вам кофе через ' + str(orders[call.from_user.id]['time']) + ' минут?'
            bot.send_message(call.message.chat.id, text='Ввод времени\n' + mes, reply_markup=choose_time)
        elif call.data[1:] == 'сhoose_time_6':
            mes = 'Доставим вам кофе через ' + str(orders[call.from_user.id]['time']) + ' минут'
            bot.send_message(call.message.chat.id, text=mes, reply_markup=main_menu)
    elif call.data[0] == '5':
        # принимаем заказ
        if orders[call.message.chat.id]['coffee'] == None:
            bot.send_message(call.message.chat.id, 'Вы не выбрали кофе')
        elif orders[call.message.chat.id]['pattern'] == None:
            bot.send_message(call.message.chat.id, 'Вы не выбрали узор')
        elif orders[call.message.chat.id]['address'] == None:
            bot.send_message(call.message.chat.id, 'Вы не указали адрес доставки')
        else:
            # вывести полную инфу о заказе
            bot.send_message(call.message.chat.id, 'Заказ принят')
            bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    elif call.data[0] == '6':
        # отменяем заказ
        orders.pop(call.from_user.id)
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    print(orders[call.from_user.id])

bot.polling(none_stop=True, interval=0)
