#@KatsiarynaVol
#https://t.me/KatsiarynaVol

import  os
from telebot.types import ReplyKeyboardRemove, InputMediaPhoto
import time
import telebot
import json
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types

from setting import botToken,id_chanel
import requests
import schedule
import time
#from parsing import dict_,all_url,urls,url
from keybords import markup_brend,main_keybord,markup_sizes,all_brend,sizes,markup_price,button_keybord,lot_keybord,otziv_keybord,canal_but,admin_keybord,brend_res
from service_func import post_model,choise,list_post
from admin_add import check_is_admin,check_is_super_admin,new_admin
from admin import post_card,view_lots, edit_caption


bot = telebot.TeleBot (botToken)
new_card_card={}
dict_card={}
id_l=""
commands_user = ["/change_marka", "/change_model", "/change_price",
                 "/admin_add","/view_card"]

def dt(s):
    s = s[1:]
    return s

def fs(st):
    return(st[0])

@bot.message_handler(commands=['start'])
def start_message(message):
    choise.clear()
    photo = open(r"C:\Users\37529\PycharmProjects\заданька\2023-02-09_09-50-32.png", "rb")
    text="Магазин обуви №1 в РБ!!!\n " \
         "'https://sneakerstore.by/'\nhttps://www.instagram.com/air.shop_by/\nhttps://vk.com/club48551970\n+375291929111"
    bot.send_photo(message.chat.id, photo=photo, caption=text)
    bot.send_message(message.chat.id,"Подбери себе пару \n"
                                          ,reply_markup=main_keybord())
#сохранение отзыва и телефона
@bot.message_handler(commands=['text'])
def contact_message(message):
    if message.content_type == "text" and message.text.replace(" ", "") != "" and message.text.isdigit() and int(message.text) > 0:
        bot.send_message(message.chat.id, 'Спасибо за обращение. Мы свяжемся с вами в ближайшее время.',reply_markup=button_keybord())
        choise["oder"]=message.id
        choise["telephone"]=message.text
        #Отправить сообщение админу
        bot.send_message(message.chat.id, 'Поступил новый заказ.'+str(message.id))
        with open('oder/'+str(message.id)+'.json', 'w', encoding='utf-8') as f:
            json.dump(choise, f, ensure_ascii=False, indent=4)

    else:
        msg=bot.send_message(message.chat.id, "попробуй еще раз, впиши только цифры")
        bot.register_next_step_handler(msg, contact_message)

def brend(message):
    global file
    if message.content_type == "text" and message.text.replace(" ", "") != "":
        print(message.text)
        file = message.text
        msg=bot.send_message(message.chat.id, 'Впишите отзыв ')
        bot.register_next_step_handler(msg, save_otziv)
    else:
        bot.send_message(message.chat.id, 'Попробуй еще раз ')

def save_otziv(message):
    if message.content_type == "text" and message.text.replace(" ", "") != "":
        print(message.text)
        print(file)
        choise["text"] = message.text
        choise1={file:choise}
        try:
            f = open("vocabulary/" + str(file) + ".json", "r", encoding="utf-8")
            buf_otziv= json.loads(f.read())
            buf_otziv.update(choise1)
        except:
            print(" Создаю новый отзыв")
        with open('otziv/'+file+'.json', 'w', encoding='utf-8') as f:
            json.dump(choise1, f, ensure_ascii=False, indent=4)
        bot.send_message(message.chat.id, 'Спасибо за otziv, ',reply_markup=button_keybord())

#блок создания новой карточки new_card-photo
@bot.message_handler(commands=['new_card'])
def new_card(message):
    if message.text == "/new_card":
        new_card_card[message.chat.id] = ""
        text = "Так будет выглядеть карточка товара\n Добавления новой:\n Остановить добавление: /stop\n\n Начнём - напишите марку \n"
        #msg = bot.send_message(message.chat.id, text)
        photo = open(r"C:\Users\37529\PycharmProjects\заданька\IMG_0251-auto_width_1000.jfif", "rb")
        msg = bot.send_photo(message.chat.id, photo=photo, caption=text)
        bot.register_next_step_handler(msg, card)
    elif message.text == "/stop":
        bot.send_message(message.chat.id, "Вы вышли из добaвления ")
# #
class Card:
    def __init__(self, marka):
        self.marka = marka
        self.id_prodyct=None
        self.model = None
        self.price = None
        self.size = None
        self.photo = None

def card_obj(obj_card):
    all_atributes = obj_card.__dict__
    text = ""

    for key, value in all_atributes.items():
        val = value
        if key != "photo":
            if value == None:
                val = ""
            text = text + key + " : " + val + "\n"
    return text
def card(message):
    if message.text == "/new_card":
        msg = bot.send_message(message.chat.id, "Начнём . Пришли название марки")
        bot.register_next_step_handler(msg, card)
    elif message.text == "/stop":
        bot.send_message(message.chat.id, "Вы вышли из добaвления ")

    elif message.content_type == "text" and message.text.replace(" ", "") != "" and message.text not in commands_user:
        new_c = Card(message.text)
        new_card_card[message.chat.id] = new_c
        dict_card["brand"]= str(message.text).capitalize()
        bot.send_message(message.chat.id, card_obj(new_card_card[message.chat.id]))
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)
        msg = bot.send_message(message.chat.id,
                               "Теперь отправьте id-prodyct, \n/change_marka для редактирования марки , \nОстановить добавление: /stop")
        bot.register_next_step_handler(msg, id_prodyct)
    elif message.text in commands_user:
        msg = bot.send_message(message.chat.id, "что-то пошло не так, попробуй снова. \nПришли марку")
        bot.register_next_step_handler(msg, card)
    else:
        msg = bot.edit_message_text(message.chat.id,
                           "что-то пошло не так, попробуй снова\nДля выхода пришли '/stop'\nДля обновления карточки пришли '/new_card'")
        bot.register_next_step_handler(msg, card)
def id_prodyct(message):
    if message.text == "/new_lot":
        msg = bot.send_message(message.chat.id, "Начнём с начала. Пришли название марки")
        bot.register_next_step_handler(msg, card)

    elif message.text == "/stop":
        bot.send_message(message.chat.id, "Вы вышли из добaвления ")

    elif message.content_type == "text" and message.text.replace(" ", "") != "" and message.text.isdigit() and message.text not in commands_user:
        new_card_card[message.chat.id].id_prodyct = message.text
        dict_card["id_prodyct"]= str(message.text)
        bot.send_message(message.chat.id, card_obj(new_card_card[message.chat.id]))
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id-1)
        bot.delete_message(message.chat.id, message.message_id-2)
        msg = bot.send_message(message.chat.id, "Теперь пришли название модели")
        bot.register_next_step_handler(msg,model)

    else:
        msg = bot.send_message(message.chat.id,
                           "Ты неверно написал, напиши снова или\nДля выхода пришли '/stop'\nДля обновления карточки пришли '/new_card'")
        bot.register_next_step_handler(msg, id_prodyct)
def model(message):
    if message.text == "/new_card":
        msg = bot.send_message(message.chat.id, "Начнём с начала. Пришли название марки")
        bot.register_next_step_handler(msg, card)

    elif message.text == "/stop":
        bot.send_message(message.chat.id, "Вы вышли из добaвления ")

    elif message.content_type == "text" and message.text.replace(" ", "") != "":
        new_card_card[message.chat.id].model = message.text
        dict_card["model"]= str(message.text).capitalize()
        bot.send_message(message.chat.id, card_obj(new_card_card[message.chat.id]))
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)

        msg = bot.send_message(message.chat.id,
                               "Теперь отправьте цену  \n/change_model для редактирования модели, \nОстановить добавление: /stop")
        bot.register_next_step_handler(msg, price)
    else:
        msg = bot.send_message(message.chat.id,
                               "что-то пошло не так, попробуй снова\nДля выхода пришли '/stop'\nДля обновления карточки пришли '/new_card'")
        bot.register_next_step_handler(msg, model)
def price(message):
    if message.text == "/new_card":
        msg = bot.send_message(message.chat.id, "Начнём с начала. Пришли название марки")
        bot.register_next_step_handler(msg, card)
    elif message.text == "/stop":
        bot.send_message(message.chat.id, "Вы вышли из добaвления ")
    elif message.text == "/change_model":
        msg = bot.send_message(message.chat.id, "Введи модель, \n\nОстановить добавление: /stop")
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.register_next_step_handler(msg, model)
    elif message.content_type == "text" and message.text.replace(" ", "") != "" and message.text.isdigit() and message.text not in commands_user:
        new_card_card[message.chat.id].price = message.text
        dict_card ["price"]=str(message.text)
        bot.send_message(message.chat.id, card_obj(new_card_card[message.chat.id]))
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)
        msg = bot.send_message(message.chat.id,
                               "Теперь отправьте размеры в наличии\n/change_price для редактирования цены , \nОстановить добавление: /stop")
        bot.register_next_step_handler(msg, size)
    else:
        msg = bot.send_message(message.chat.id,
                           "что-то пошло не так, попробуй снова\nДля выхода пришли '/stop'\nДля обновления карточки пришли '/new_card'")
        bot.register_next_step_handler(msg,price)
def size(message):
    if message.text == "/new_card":
        msg = bot.send_message(message.chat.id, "Начнём с начала.  Пришли название марки")
        bot.register_next_step_handler(msg, card)
    elif message.text == "/stop":
        bot.send_message(message.chat.id, "Вы вышли из добaвления ")
    elif message.text == "/change_price":
        msg = bot.send_message(message.chat.id, "Введи новую цену , \n\nОстановить добавление: /stop")
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)
        bot.register_next_step_handler(msg, price)
    elif message.content_type == "text" and message.text.replace(" ", "") != ""  and message.text not in commands_user:
        new_card_card[message.chat.id].size = message.text
        dict_card["size"]= str(message.text)
        bot.send_message(message.chat.id, card_obj(new_card_card[message.chat.id]))
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)
        msg = bot.send_message(message.chat.id, "Осталось загрузить фото  \nОстановить добавление: /stop")
        bot.register_next_step_handler(msg, photo)
    else:
        msg = bot.send_message(message.chat.id,
                               "что-то пошло не так, попробуй снова\nДля выхода пришли '/stop'\nДля обновления карточки пришли '/new_card'")
        bot.register_next_step_handler(msg, size)
def photo(message):
    if message.text == "/new_card":
        msg = bot.send_message(message.chat.id, "Начнём с начала. Пришли название лота")
        bot.register_next_step_handler(msg, card)
    elif message.text == "/stop":
        bot.send_message(message.chat.id, "Вы вышли из добaвления ")

    elif message.content_type == "photo":
        photo1=( message.photo[-1].file_id)
        dict_card["photo"]=photo1
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)
        bot.send_photo(message.chat.id, photo1,card_obj(new_card_card[message.chat.id]))
        id_pro = dict_card["id_prodyct"]
        print(id_pro)

        bot.send_message(message.chat.id,
                         "Вот карточка .\nЧто делаем дальше?\nЕсли нужно что-то исправить выбери: \n /change_card - изменение марки \n /change_model - изменение модели \n /change_price - изменение цены лота \n  Нажми сохранить\n Переходи в канал : https://t.me/+VJylJ1N-IRA3NTMy\n"
                         "для создания новой карточки пришли /new_card",reply_markup=lot_keybord())

    else:
        msg = bot.send_message(message.chat.id,
                               "что-то пошло не так, попробуй снова\nДля выхода пришли '/stop'\nДля обновления карточки пришли /new_card")
        bot.register_next_step_handler(msg, photo)
    print(dict_card)
    #return dict_card

# admin_add-добавление админа
@bot.message_handler(commands=['admin_add'])
def start_admin(message):
    #проверка на суперадмина
    if check_is_super_admin(message.from_user.id,bot):
        msg = bot.send_message(message.chat.id, "Перешлите сюда сообщение от человека, которого вы хотите добавить в Администраторы\nДля выхода пришли '/stop'")
        bot.register_next_step_handler(msg, catch_reply)
def catch_reply(message):
    if message.content_type == "text" and message.text =="/stop":
        bot.send_message(message.chat.id, "Вы вышли из добавления администратора")
    elif not message.forward_from:
        msg = bot.send_message(message.chat.id, "Что-то пошло не так. Нужно Переслать сообщение от пользователя, которого вы хотите сделать админом\nПопробуйте снова\n напишите /stop - для выхода")
        bot.register_next_step_handler(msg, catch_reply)
    else:
        id = message.forward_from.id
        user_name = message.forward_from.username
        new_admin(id,user_name,bot,message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def call(call):
    id = call.message.chat.id
    flag = fs(call.data)
    data = dt(call.data)
    user_name = call.message.chat.username
    choise["user_name"] = user_name
    choise["user_name_id"] = call.message.chat.id
    #choise["brand"]=''
    print(call.data)
    bot.answer_callback_query(callback_query_id=call.id)

    #пост лотов
    if flag=="p":
       # bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        if len(choise)<4:
            choise["brand"] =""
            #choise["size"] = ""
        choise["price"] = data
        print(choise)
        buf_new=post_model(choise)
        num1=len(buf_new)
    if flag == "p":
        num1 = 0
        #buf_new=list_post(num, post_model(choise),bot,call.id)
        buf_new=post_model(choise)
        if len(buf_new) !=0:
            list_post(num1, buf_new, bot, call)


        else:
            bot.delete_message(call.message.chat.id, call.message.message_id - 1)
            bot.send_message(id,
                             "К сожалению у нас нет моделей удовлетворяющих\n Вашим условиям, но они обязательно появяться! \nМожно оставить заявку!\n звоните менеджеру +37529 192 91 11")
            choise.clear()
            bot.send_message(id, 'Оставьте ваш контактный номер для заказа, чтобы наш менеджер смог связаться с вами. ',
                             reply_markup=otziv_keybord())
#
    if flag=="n":
        bot.delete_message(call.message.chat.id, call.message.message_id )
        choise["brand"] = data
        bot.send_message(id, "Вот все возможные размеры \n", reply_markup=markup_sizes(sizes))
        print(choise)
#
    if flag=="z":
        bot.delete_message(call.message.chat.id, call.message.message_id )
        #print(choise)
        choise["size"]=data
        bot.send_message(id, "Выбери диапазон цен \n", reply_markup=markup_price())
        #print(choise)
    #выбор брэнда
    if flag=="s":
        page=0
        choise.clear()
        print(choise)
        print(len(all_brend))
        bot.send_message(id, "Вот все возможные категории \n", reply_markup=markup_brend(brend_res(all_brend),page))
    #
    if flag=="c":
        msg=bot.send_message(id, "Впишите номер телефона")
        bot.register_next_step_handler(msg, contact_message)

    #отзывы
    if flag=="g":
        msg = bot.send_message(id, "Впишите брэнд ")
        bot.register_next_step_handler(msg, brend)
    #
    if flag=="o":
        print(data)
        #bot.send_message(id, "Смотреть отзывы\n", reply_markup=otziv_markup())

    # выход из команды /view_lots !! canal
    if flag == "<":
       try:
           bot.delete_message(call.message.chat.id, call.message.message_id)
       except:
           print()
#пост карточки товара в канал
    if flag=="i":
        id_pro = dict_card["id_prodyct"]
        with open('admin_card/' + str(id_pro) + '.json', 'w', encoding='utf-8') as f:
            json.dump(dict_card, f, ensure_ascii=False, indent=15)

        msg=bot.send_photo(id_chanel, dict_card["photo"], caption=post_card(id_pro),reply_markup=canal_but(id_pro,call.message.message_id))
        chanal_msg_id=msg.message_id
        #bot.delete_message(id_chanel,msg.message_id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        bot.delete_message(call.message.chat.id, call.message.message_id - 2)
        bot.send_photo(id, dict_card["photo"],
                       caption=" опубликован. Переходи в канал : https://t.me/+VJylJ1N-IRA3NTMy\n"
                               "для создания нового  '/new_card'",reply_markup=admin_keybord(id_pro,chanal_msg_id))

#редактирование карточки
    if flag=="r":
        id_pro=data
        view_lots(call.message,id_pro, bot,call.id,call.from_user.id)

#редактирование полей карточки
    if flag=="e":
        data=data.split("@")
        edit_part=data[0]
        id_pro=data[1]
        print(data)
        msg = bot.send_message(call.message.chat.id,
                               "Для изменeния поля - " + edit_part + ", отправьте сообщение в чат \nДля выхода напишите /stop")
        bot.register_next_step_handler(msg, edit_caption,id_pro,bot,data[2],call.message.chat.id ,call.id,edit_part)


#удаление карточки из канала и з джейсона
    if flag=="d":
        data = data.split("@")
        print(data)
        d=call.message.message_id
        os.remove('C:\\Users\\37529\\PycharmProjects\\заданька\\admin_card\\' + data[0] + ".json")
        print(call.message.chat.id, call.message.message_id)
        bot.delete_message(call.message.chat.id, d)
        #удалить сообщение в канале
        bot.delete_message(id_chanel,data[1])

#вперед-назад для карточек
    if flag=="v":
        bot.delete_message(call.message.chat.id, call.message.message_id-4)
        bot.delete_message(call.message.chat.id, call.message.message_id-3)
        bot.delete_message(call.message.chat.id, call.message.message_id-2)
        bot.delete_message(call.message.chat.id, call.message.message_id-1)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        data=data.split("@")
        print(data)
        num1 = int(data[1])
        list_post(num1, post_model(choise),bot, call)

#вперед-назад для брэндов
    if flag=="a":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        data = data.split("@")
        print(data)
        page = int(data[1])
        print(page)

        bot.send_message(id,"Вот все возможные категории \n", reply_markup=markup_brend(brend_res(all_brend), page))

print("Ready")
bot.infinity_polling()

