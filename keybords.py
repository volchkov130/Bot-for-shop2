#@KatsiarynaVol
#https://t.me/KatsiarynaVol

from telebot.types import ReplyKeyboardRemove, InputMediaPhoto
import time
import telebot
import json
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
from bs4 import BeautifulSoup
import pprint
from setting import botToken
import requests
import schedule
import time
#from parsing import dict_,all_url,urls,url
bot = telebot.TeleBot (botToken)

sizes=['36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '42.5', '36.5', '44.5']
all_brend=['Saucony', 'Retropy', 'Nike',  'Niteball',  'Bad', 'Jordan',  'Slide', 'Balenciaga', 'superstar', 'Forum', 'Premiata', 'Dior', 'ZX', 'Rebasus', 'Adiprene', 'Adi2000', 'Ozelia',  'SB', 'nite', 'Converse',  'кеды', 'Fei', 'zx', 'Dr.Martens', 'Spezial', 'COLUMBIA', 'Ozweego', 'climacool', 'zx500', 'BLAZER', 'High', 'Brown', 'Dunk', 'Jazz', 'Black\\Orange', 'Air', 'Sonic', 'Yeezy', 'deerupt']
def main_keybord():

    keyboard = InlineKeyboardMarkup()
    button_1 = (InlineKeyboardButton("Выбрать марку ",callback_data="s"))
    button_2 = (InlineKeyboardButton("Фильтр по цене", callback_data="z"))
    keyboard.add(button_1,button_2)
    return keyboard

def button_keybord():
    button_1 = (InlineKeyboardButton("Вернуться к выбору модели", callback_data="s"))
    return button_1


# def markup_brend(all_brend):
#     #sizes, all_brend=dict_(all_url(urls(url)))
#     categoru_markup = InlineKeyboardMarkup()
#     for x in all_brend:
#         categoru_markup.add(InlineKeyboardButton("▪️"+x,callback_data="n" + str(x)))
#
#     return categoru_markup

def brend_res(all_brend):
    size = 9
    res = [all_brend[i:i + size] for i in range(0, len(all_brend), size)]
    print(res)
    return res

def markup_brend(res,page):
    print('page',page)
    #sizes, all_brend=dict_(all_url(urls(url)))
    categoru_markup = InlineKeyboardMarkup()
    button_4 = (InlineKeyboardButton("Вперед", callback_data="a" +"@"+ str(page + 1)))
    button_5 = (InlineKeyboardButton("Назад ", callback_data="a" +"@"+ str(page - 1)))
    print(res[page])
    for x in res[page]:
        #print(x)
        categoru_markup.add(InlineKeyboardButton("▪️"+x,callback_data="n" + str(x)))

    if page + 1 < len(res):
        categoru_markup.add(button_4)
    if page >= 1:
        categoru_markup.add(button_5)

    return categoru_markup


def markup_sizes(sizes):
    #sizes, all_brend=dict_(all_url(urls(url)))
    sizes_markup = InlineKeyboardMarkup()
    for x in sizes:
        sizes_markup.add(InlineKeyboardButton("▪️"+x,callback_data="z" + str(x)))
    sizes_markup.add(InlineKeyboardButton("Пропустить", callback_data="z"))
    sizes_markup.add(InlineKeyboardButton("Отзывы по выбранной модели", callback_data="o"))
    return sizes_markup


def markup_price():
    list_price={0:"до 100 ",1:"100-150",3:"150-170",4:"170-250",5:"250 и больше"}
    price_markup = InlineKeyboardMarkup()
    for x in list_price.values():
        price_markup.add(InlineKeyboardButton("▪️"+x,callback_data="p" + str(x)))
    price_markup.add(InlineKeyboardButton("Пропустить",callback_data="p" ))

    return price_markup


def contact_markup():
    keyboard = InlineKeyboardMarkup()
    reg_button = InlineKeyboardButton(text="Оставить номер телефона",
                                      callback_data="c")
    keyboard.add(reg_button)

    return keyboard

def lot_keybord():
    lot_keybord = InlineKeyboardMarkup()
    button_1 = (InlineKeyboardButton("Опубликовать", callback_data="i"))
    button_2 = (InlineKeyboardButton("Удалить", callback_data="d"))
    lot_keybord.add(button_1,button_2)
    return lot_keybord




def canal_but(id_pro,id_message):
    canal_but=InlineKeyboardMarkup()
    canal_but.add(InlineKeyboardButton("Выбрать и сделать заказ",url="https://t.me/test_06022023_bot?start=1"))
    return canal_but

def admin_keybord(id_pro,id_message):
    admin_keybord=InlineKeyboardMarkup(row_width=1)
    button_1 = (InlineKeyboardButton("Редактировать", callback_data="r" + str(id_pro)+"@"+str(id_message)))
    button_2 = (InlineKeyboardButton("Удалить", callback_data="d" + str(id_pro)+"@"+str(id_message)))
    admin_keybord.add(button_1, button_2)
    return admin_keybord



def edit_card_keyboard(data):
    print("edit_card_keyboard")
    keyboard = InlineKeyboardMarkup(row_width=3)
    names = ["Брэнд",'Модель', 'Цена']
    button_list = [InlineKeyboardButton(text=x, callback_data="e"+ x+"@"+ str(data)) for x in names]
    # save_button = InlineKeyboardButton(text="Сохранить", callback_data="w" + str(data))
    # button_public_in_channel = (InlineKeyboardButton("Опубликовать", callback_data="*" + str(data)))
    exitbutton = InlineKeyboardButton(text="Выход", callback_data="<")
    keyboard.add(*button_list)
    # keyboard.add(save_button)
    # keyboard.add(button_public_in_channel)
    keyboard.add(exitbutton)
    return keyboard

def otziv_keybord(num,chuck_list):

    otziv_keybord = InlineKeyboardMarkup()
    button_1 = (InlineKeyboardButton("оставить отзыв по брэнду ", callback_data="g"))
    button_2 = (InlineKeyboardButton("Вернуться к выбору модели", callback_data="s"))
    button_3 = (InlineKeyboardButton(text="Оставить номер телефона для заказа/связи", callback_data="c"))
    button_4 = (InlineKeyboardButton("Вперед", callback_data="v" + "@" + str(num + 1)))
    button_5 = (InlineKeyboardButton("Назад ", callback_data="v" + "@" + str(num - 1)))
    if num +1<len(chuck_list):
        otziv_keybord.add(button_4)
    if num>=1:
        otziv_keybord.add(button_5)

    otziv_keybord.add(button_1)
    otziv_keybord.add(button_2)
    otziv_keybord.add(button_3)
    return otziv_keybord

