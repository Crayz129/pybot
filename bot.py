# Настроить бота на отправку сообщений +
# Сделать чтобы он рандомно отправлял числа в "руку" игрока +
# Сделать чтобы брал "карты" себе +-
# Научить считать сумму +
# Сделать чтобы сравнивал с "рукой" игрока +
# В будущем может прикрутить визуал и возможность добирать(и игроку и боту), сплитить и добавить банк; добавить кнопку
# Вебхуки / гетайпдейтс
#                                                                                                                                                                                                                                                                                                                                                                                                                 Если залью это на гх и найду где-то в будущем, то хочу напомнить себе, что Саша лучшая <3 ❤💙💜🖤💞 вау ебать вс код воспринимает юникодовские эмодзи 🚽 
# Разделить игру на фазы(продолжить игру по кнопке)
# Если сумма дилера =< 16, он обязан добрать, иначе он обязан не брать
import telebot
from telebot import types
import random
import time
import requests
global bank
global summ 
global card 
token = '1371006028:AAFn3c6F0DoutVUzdbRhjScdKQPuxXNbC-Y'
#MethodGetUpdates = 'https://api.telegram.org/bot{token}/getUpdates?offset=10'.format(token=token)
#https://api.telegram.org/bot1371006028:AAFn3c6F0DoutVUzdbRhjScdKQPuxXNbC-Y/getUpdates?offset=10
bot = telebot.TeleBot(token)
markup = types.InlineKeyboardMarkup()
kartinki = ["Валет", "Дама", "Король", "Туз"]
global summa 
global summabot 
summa = 0
summabot = 0


def numbers_to_kartinki(card):
    for x in range(len(card)):
        if card[x] == 11:
            card[x] = kartinki[0]
        elif card[x] == 12:
            card[x] = kartinki[1]
        elif card[x] == 13:
            card[x] = kartinki[2]
        elif card[x] == 14:
            card[x] = kartinki[3]   
def razdacha(message,card,summa,summabot):
    summ = card.copy() 
    msg = bot.send_message(message.from_user.id, str(card))       
    #card.append(random.randint(11, 14))
    for x in range(len(summ)):
        for t in range(11,15):
            if summ[x] == t and t !=14:
                summ[x] = 10
            elif summ[x] == t and t == 14:
                summ[x] = 11
    for i in range(len(summ)):
        if i%2 == 0:           
            summa += int(summ[i])
        else: 
            summabot += int(summ[i])
    numbers_to_kartinki(card)
    return msg
@bot.message_handler(content_types='text')
def start(message):
    #getupdates(message)
    btn1 = types.InlineKeyboardButton("Играть", callback_data='yes')
    msg0 = bot.send_message(message.from_user.id, 'Wanna play?', reply_markup=markup.row(btn1))
    @bot.callback_query_handler(func=lambda call: True)
    def check(message):
        if btn1.callback_data == 'yes' and btn1.callback_data != 'pass':
            blackjack(message) 
            time.sleep(0.5)
            bot.delete_message(message.from_user.id, msg0.message_id)
        else:
            bot.send_message(message.from_user.id, "Ну бб тогда")
def blackjack(message):
    #getupdates(message)
    card = [random.randint(3, 14),random.randint(3, 14),random.randint(3, 14),random.randint(3, 14)]
    razdacha(message,card,summa,summabot)
    msg = razdacha(message,card,summa,summabot)
    #if summabot < 16:
        
    if summa == 21 and summabot != 21:
        bot.send_message(message.from_user.id, "Ваши карты: "+str(card[0])+', '+str(card[1]))
        bot.send_message(message.from_user.id, 'У Вас блекджек, Вы победили!')
    elif summa == 21 and summabot == 21:
        bot.send_message(message.from_user.id, "Ничья!")
    else:
        bot.send_message(message.from_user.id, "Ваши карты: "+str(card[0])+', '+str(card[1]) + '\n'+ "Ваш счёт: " + str(summa))
        time.sleep(0.5)
        btn1 = types.InlineKeyboardButton("Продолжить", callback_data='pass')
        # markup.to_dict
        msg3 = bot.send_message(message.from_user.id, "Карты крупье: "+ str(card[2])+", "+'*****'+'\n'+"Счёт крупье: "+str(summabot), reply_markup=markup.row(btn1))
        time.sleep(0.5)
        if summa > summabot:
            bot.send_animation(message.from_user.id, 'https://tenor.com/view/aot-attack-on-titan-gif-21478955')
            msg2 = bot.send_message(message.from_user.id, "Вы выиграли!", reply_markup=markup)
            #bot.send_photo(message.from_user.id, 'https://sun9-80.userapi.com/impg/taRHXKr_qUSeGfzCsYeGx6qFj_1yV7bjBG1vpA/j24ntxDjM7g.jpg?size=1080x1080&quality=95&sign=9e4188b54c00ae80411ef33b023be4f9&type=album')
        elif summa == summabot:
            msg2 = bot.send_message(message.from_user.id, "Ничья!", reply_markup=markup)
        elif summa < summabot:
            if summabot == 21: 
                msg2 = bot.send_message(message.from_user.id, "У крупье блэкджек. Вы проиграли!", reply_markup=markup)
            else:
                msg2 = bot.send_message(message.from_user.id, "Вы проиграли!", reply_markup=markup)
    bot.delete_message(message.from_user.id, msg.message_id)
    time.sleep(5)
    bot.edit_message_reply_markup(message.from_user.id, msg2.message_id) 
""" def getupdates(message, offset = 0):
    response = requests.get('https://api.telegram.org/bot{token}/getUpdates')
    result = response.json()
    print(result) """
bot.infinity_polling() 
   
