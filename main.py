from telebot.types import ReplyKeyboardRemove, InputMediaPhoto
import time
import telebot
import json
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def dt(s):
    s = s[1:]
    return s

def fs(st):
    return(st[0])
