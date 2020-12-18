import re
import requests
import pandas as pd
import telebot
from bs4 import BeautifulSoup
import config
from random import randint
import datetime
from datetime import datetime



bot = telebot.TeleBot(config.token)

pict = [
    'https://focusu.com/wp-content/uploads/2017/03/team-celebration-clipart.jpg',
    'https://blog.bonus.ly/hubfs/office-celebrate.png',
    'https://www.morehealthinc.org/wp-content/uploads/2019/01/lets-celebrate-banner.jpg',
    'https://www.incimages.com/uploaded_files/image/1920x1080/getty_504047222_2000133320009280325_398823.jpg',
    'https://www.bagsoflove.co.uk/blog/wp-content/uploads/2019/10/shutterstock_1024473769-886x550.jpg',
    'https://cdn25.img.ria.ru/images/07e4/08/10/1575860833_0:0:2815:2048_600x0_80_0_1_024f5006c2d15855896210651d0af4ec.jpg.webp'
    ]

current = datetime.today().strftime('%A')
n = datetime.today().isoweekday()
if n == 5:
    text = f"Today is {current}. Weekend is tomorrow. Be ready for Holidays!"
if 1 <= n < 5:
    text = f"Today is {current}. Weekend starts in {6 - n} days. Don't wait and celebrate Holidays!"
if n == 6 or n == 7:
    text = f"Today is {current} and this is a Weekend: celebrate Holidays!"


def holiday(day):

    url = 'http://www.holidayscalendar.com/'
    website = requests.get(url).text
    soup = BeautifulSoup(website, 'lxml')
    table = soup.find_all('table')
    if day == 'today':
        rows = table[0].find_all('td')
        holidays = [row.text.strip() for row in rows]
    elif day == 'tomorrow':
        rows = table[1].find_all('td')
        holidays = [row.text.strip() for row in rows if len(row)]
    elif day == 'upcoming':
        rows = table[2].find_all('td')
        holidays = []
        for i in range(1, 39, 4):
            holidays.append(rows[i].text.strip())
            holidays.append(rows[i - 1].text.strip())
    else:
        holidays = 'Something has gone wrong! We still do not know what to celebrate (:'
    return holidays


@bot.message_handler(commands=["picture"])
def print_hi(message):
    bot.send_photo(message.chat.id, pict[randint(0, 5)])

@bot.message_handler(commands=["info"])
def cmd_info(message):
    bot.send_message(message.chat.id, "Info method is used to show you what I am capable of.\n"
                                      "I could provide you with some information about holidays.\n"
                                      "First you gotta select the day: /today, /tomorrow or /upcoming.\n"
                                      "I have info for today's, tomorrow's or 10 upcoming holidays.\n"
                                      "The info contains a holiday, location and type of the holiday for today and tomorrow.\n"
                                      "Type /reset to start anew.")
    bot.send_message(message.chat.id, "The next step is to specify what holidays you are interested in.\n"
                                      "You should enter your choice:\n"
                                      "/today, /tomorrow or /upcoming.\n"
                                      "You can also get lists of available optionss using /listoptions.\n"
                                      "Type /reset to start anew.")
    bot.send_message(message.chat.id, "There's a number of commands you can use here. \n"
                                      "Type /commands to get the list of available functions.\n"
                                      "Type /reset to start anew.")


@bot.message_handler(commands=["listoptions"])
def cmd_listoptions(message):
    x = '/today, /tomorrow, /upcoming'
    bot.send_message(message.chat.id, x)


@bot.message_handler(commands=["commands"])
def cmd_commands(message):
    bot.send_message(message.chat.id,
                     "/reset - is used to discard previous selections and start anew.\n"
                     "/start - is used to start a new dialogue from the very beginning.\n"
                     "/info - is used to know what i can do for you.\n"
                     "/commands - If you got here, you know what it is used for.\n"
                     "/listoptions - is used to choose a day to get info about holidays.\n"
                     "/today - if you want to know today's holidays.\n"
                     "/tomorrow - if you want to know tomorrow's holidays.\n"
                     "/upcoming - if you want to know 10 upcoming holidays.\n")


# По команде /reset будем сбрасывать состояния, возвращаясь к началу диалога
@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Let's start anew.\n"
                                      "From what day do you want to get info about holidays: /today or /yesterday or /upcoming.\n"
                                      "Use /info or /commands to rewind what I am and what can I do.")
    bot.send_photo(message.chat.id, pict[randint(0, 5)])


@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_message(message.chat.id, "Greetings! I'm HolidayCelebrate bot :) \n"
                                      "You gotta specify which day's holidays info you want to get: /today or /yesterday or /upcoming.\n"
                                      "Type /info to know what I am and what I can do for you.\n"
                                      "Type /commands to list the available commands.\n"
                                      "Type /reset to discard previous selections and start anew.")
    bot.send_photo(message.chat.id, pict[randint(0, 5)])


@bot.message_handler(commands=["today"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Ok, we've specified the day.\n"
                                      "You could also type /info to know more about me.\n"
                                      "Type /reset to start anew.")
    bot.send_message(message.chat.id, "\n".join(holiday('today')))
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["tomorrow"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Ok, we've specified the day.\n"
                                      "You could also type /info to know more about me.\n"
                                      "Type /reset to start anew.")
    bot.send_message(message.chat.id, "\n".join(holiday('tomorrow')))
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["upcoming"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Ok, we've specified the day.\n"
                                      "You could also type /info to know more about me.\n"
                                      "Type /reset to start anew.")
    bot.send_message(message.chat.id, "\n".join(holiday('upcoming')))
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: message.text.strip().lower() not in ('/reset', '/info', '/start', '/commands', '/listoptions', '/today', '/tomorrow', '/upcoming'))
def cmd_day(message):
    if message.text.lower().strip() == 'today':
        bot.send_message(message.chat.id, "Ok, we've specified the day.\n"
                                              "You could also type /info to know more about me.\n"
                                              "Type /reset to start anew.")
        bot.send_message(message.chat.id, "\n".join(holiday('today')))
        bot.send_message(message.chat.id, text)
    elif message.text.lower().strip() == 'tomorrow':
        bot.send_message(message.chat.id, "Ok, we've specified the day.\n"
                                              "You could also type /info to know more about me.\n"
                                              "Type /reset to start anew.")
        bot.send_message(message.chat.id, "\n".join(holiday('tomorrow')))
        bot.send_message(message.chat.id, text)
    elif message.text.lower().strip() == 'upcoming':
        bot.send_message(message.chat.id, "Ok, we've specified the day.\n"
                                              "You could also type /info to know more about me.\n"
                                              "Type /reset to start anew.")
        bot.send_message(message.chat.id, "\n".join(holiday('upcoming')))
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, "HolidayCelebrate bot with you:).\n"
                                           "Now you gotta specify which day's info you want to get: /today or /tomorrow or /upcoming.\n"
                                            "I have information about today's, tomorrow's and upcoming holidays.\n"
                                            "To recollect what we are doing now type /info.\n"
                                            "Type /reset to start anew.")


def cmd_sample_message(message):
    bot.send_message(message.chat.id, "Hey there, I'm holidaycelebrate bot!\n"
                                      "I'm not that smart, sorry :(\n"
                                      "Do you want to have fun?.\n"
                                      "That's what I can help you with and advise a reason!\n"
                                      "If so, type /start and let's get some. \n"
                                      "Type /info to know what i can do for you.\n"
                                      "Type /commands to list available commands :).")
    bot.send_photo(message.chat.id, pict[randint(0, 5)])



if __name__ == '__main__':
    bot.infinity_polling()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

