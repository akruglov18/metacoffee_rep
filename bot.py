# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 21:32:23 2021

@author: Super-puper team
"""
import telebot
from telebot import types

bot = telebot.TeleBot('5009339889:AAEhnKB0qSyQECs5g4wHsEOo0ppJTv6g8P4')

# talking module

# order begin

# choose coffee type

# choose decoration

# choose address

# report

orders = dict()

@bot.message_handler(content_types=['text'])
def get_text_messages(message) :
    if (message.text == "/get"):
        get_keyboards(message)
    global answer
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
       bot.send_message(message.from_user.id, "Напиши привет")
    elif message.text == "Покажи" :
        bot.send_message(message.from_user.id, orders[message.from_user.id])
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
        orders[message.from_user.id] = message.text

@bot.message_handler(commands=['get'])
def get_keyboards(commands) :
    itembtn1 = types.KeyboardButton('a')
    itembtn2 = types.KeyboardButton('v')
    itembtn3 = types.KeyboardButton('d')
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(commands.from_user.id, "Done", reply_markup=markup)

bot.polling(none_stop=True, interval=0)

















