#@KatsiarynaVol
#https://t.me/KatsiarynaVol

from telebot.types import ReplyKeyboardRemove, InputMediaPhoto
import telebot
import json
from setting import botToken

#from parsing import dict_,all_url,urls,url
from keybords import markup_brend,main_keybord,markup_sizes,all_brend,sizes,otziv_keybord
#from main import choise

choise = {'user_name':None,
        'user_name_id':None,
        "brand":'',
        "price":None,
          "size": None }

bot = telebot.TeleBot (botToken)

#сбор карточек по выбранному бренду, проверку по размерам делать нет смысла, т.к. у каждой модели есть все размеры
def post_model(choise):
    print(choise)
    list_price ={0:"до 100 ",1:"100-150",3:"150-170",4:"170-250",5:"250 и больше"}
    f = open('data.json', 'r', encoding='utf-8')
    dict_all = json.loads(f.read())
    f.close()
    buf=[]
    buf_new=[]
    val= list(choise.values())
    keys=list(choise.keys())
    for i in dict_all:
        if i['brand']==choise['brand']:
            buf_new.append(i)
        if choise['brand']=='':
            buf_new.append(i)
    #print(buf_new)
    if choise['price'] != '':
        for i in range(1, len(keys)):
                for x in buf_new:
                    if val[i] == "до 100 ":
                        if x['price'] < '100':
                            buf.append(x)
                    if val[i] == "100-150":
                        if x['price'] >'101' and x['price']< "150":
                            buf.append(x)
                    if val[i] == "150-170":
                        if x['price'] >'151' and x['price']< "170":
                            buf.append(x)
                    if val[i] == "170-250":
                        if x['price'] >'171' and x['price']< "250":
                            buf.append(x)
                    if val[i] == "250 и больше":
                        if x['price'] >"251":
                            buf.append(x)
    if choise['price'] == '':
        [buf.append(x) for x in buf_new]
    print(len(buf_new))
    print(len(buf))

    return buf_new
post_model(choise)

#делим выбранные карточки и отправляем по 4 штуки
def list_post(num1,buf_new,bot,call):
    if len(buf_new)>0:
        size = 4
        chuck_list = [buf_new[i:i + size] for i in range(0, len(buf_new), size)]
        for i in chuck_list[num1]:
            text = "Брэнд: " + str(i['brand']) + '\n' + "Модель/цвет: " + str(i['model']) + '\n' + "Цена: " + str(
                i['price']) + " BYN" + '\n' + "Размеры: " + str(i['size'])
            photo=i['photo']
            for j in photo:
                j = j.replace(' ', "").split(",")
            media_group = []
            for num, url in enumerate(photo):
                media_group.append(InputMediaPhoto(media=url, caption=text if num == 0 else ''))

            bot.send_media_group(call.message.chat.id, media_group)
        bot.send_message(call.message.chat.id,"Оставить отзыв по выбранной модели ",  reply_markup = otziv_keybord(num1,chuck_list))
    else:
        bot.send_message(call.message.chat.id, "К сожалению у нас нет моделей удовлетворяющих\n Вашим условиям, но они обязательно появяться! "
                                               "\nМожно оставить заявку!\n звоните менеджеру +37529 192 91 11")



#запись отзывов
def otziv(choise,bot,chat_id):
    c=choise['brand']
    try:
        f = open("otziv/" + c + ".json", "r" , encoding="utf-8")
        f.close()
        bot.send_message(chat_id,"У данной модели нет отзывов")
    except:
        text=[]
        f = open("otziv/" + c + ".json", "r", encoding="utf-8")
        buf=json.loads(f.read())
        f.close()
        print(buf)
        # t=buf["text"]
        # text.append[t]



