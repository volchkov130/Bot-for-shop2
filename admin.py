#@KatsiarynaVol
#https://t.me/KatsiarynaVol


import telebot
import json
from setting import botToken
from  keybords import  lot_keybord,edit_card_keyboard
from admin_add import check_is_admin
bot = telebot.TeleBot (botToken)
id_chanel = "@test_canal_test_ca"
#пост в канал

def post_card(id_pro):
    res=''
    f = open('admin_card/'+str(id_pro)+'.json', 'r', encoding='utf-8')
    post_all = json.loads(f.read())
    f.close()
    print(post_all)
    post_all = {'brand': 'Ggg', 'id_prodyct': '222', 'model': 'Hhh', 'price': '55', 'size': '55'}
    print(post_all["brand"])
    res = 'Брэнд:' + post_all["brand"]+ "\n"+'Модель: ' + str(post_all["model"]) + "\n"+'Цена: ' + str(post_all["price"])+ "\n"+'Размеры: В ассортименте' + "\n"

    return res

#изменение карточки
def view_lots(message,id_pro, bot, chat_id,user_id):
    print(chat_id)
    if check_is_admin(user_id, bot):
        print("try",id_pro)
    try:
        bot.send_message(message.chat.id, "Выбери поле",reply_markup=edit_card_keyboard(id_pro))
    except:
        bot.send_message(message.chat.id, "Какая-то хрень, но файл с ID - " + str(id_pro) + " не найден :(")
        return 0, 0


#изменение карточки , сохранение в джейсон, замена в канале
def edit_caption(message,id_pro,bot, message_id,chat_id,call, edit_part):
    print("message_id",message_id)
    print(call)
    print(chat_id)
    if message.text == "/stop":
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)
        bot.send_message(message.chat.id, "Вы вышли из редактирования",)
    elif message.content_type == "text":
        f = open("admin_card/" + str(id_pro) + ".json", "r", encoding="utf-8")
        lot = json.loads(f.read())
        f.close()
        text = f'Брэнд: {lot["brand"]}\n' \
               f'Модель: {lot["model"]}\n' \
               f'Цена: {lot["price"]}\n'

        for i in (lot):
            if edit_part == i:
                i = edit_part+ ": " + message.text
                break
        text=text.split("\n")
        for i in range(len(text)):
            if edit_part in text[i]:
                text[i]=edit_part+": " + message.text
        caption = "\n".join(text)
        print(caption)
        print(message.chat.id, message_id)
        bot.delete_message(message.chat.id, message.message_id-1)
        #bot.delete_message(message.chat.id, message.message_id)
        bot.edit_message_caption(caption=caption, chat_id=id_chanel, message_id=message_id)

        names = ["Брэнд",'Модель', 'Цена']
        keys = ['brand', "model", "price"]
        caption = caption.split("\n")
        print(caption)
        for i in range(len(names)):
            for x in caption:
                if names[i] in x:
                    lot[keys[i]] = x.replace((names[i] + ": "), "")
        with open('admin_card/' + id_pro + ".json", 'w', encoding='utf-8') as f:
            json.dump(lot, f, ensure_ascii=False, indent=4)
        bot.send_message(chat_id, "Кaрточка " + str(id_pro) + " успешно изменена")

        # bot.edit_message_caption(caption=new_caption, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=edit_card_keyboard(id_lot,type_lot))
        # bot.delete_message(message.chat.id, message.message_id-1)
        # bot.delete_message(message.chat.id, message.message_id)
