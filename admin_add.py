#@KatsiarynaVol
#https://t.me/KatsiarynaVol

import json

#добавление нового админа в json
def new_admin(id_new_admin, user_name_new_admin, bot, chat_id):
    try:
        f = open("admin/"+str(id_new_admin)+".json", "r", encoding="utf-8")
        f.close()
        bot.send_message(chat_id,"Данный пользователь уже является админом")
    except:
        admin = {"admin": {"id_user": id_new_admin, "user_name": "@" + str(user_name_new_admin)}}
        with open('admin/' + str(id_new_admin) + ".json", 'w', encoding='utf-8') as f:
            json.dump(admin, f, ensure_ascii=False, indent=4)
        bot.send_message(chat_id,"Пользователь @" + str(user_name_new_admin) + " успешно добавлен")


#проверка на админа
def check_is_admin(user_id, bot):
    try:
        name_file = "admin/" + str(user_id) + ".json"
        f = open(name_file, 'r', encoding='utf-8')
        f.close()
        return True
    except:
        bot.send_message(user_id, "Вы не являетесь Администратором")
        return False

#проверка на суперадмина
def check_is_super_admin(user_id, bot):
    print(user_id)
    try:
        f = open("admin/admin.json", 'r', encoding="utf-8")
        buf = json.loads(f.read())
        super_admins = buf["super_admin"]["id_user"]
        print(super_admins)
        if user_id == super_admins:
            return True
        else:
            bot.send_message(user_id,"Вы не являетесь Супер Администратором")
            return False
    except:
        print("что-то пошло не так в функции check_is_super_admin")