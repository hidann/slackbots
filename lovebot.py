# coding=utf-8

import os
import time
import json
import sqlite3
from slackclient import SlackClient

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "sendto"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

response_global = ":wat: Не зрозумів, що ви хочете... Щоб надіслати валентинку :revolving_hearts:, використовуйте скрипт у форматі:\n`@valentine " + EXAMPLE_COMMAND + " @отримувач \"Ваше повідомлення:)\"`\n:kissing_heart:"

# видкриваємо БД, якщо файл не існує - створюємо
conn = sqlite3.connect('loveBot.db')
c = conn.cursor()

# створюємо Таблилю в БД, якщо не існує.Якщо існує, то не виконується.
def tableCreate():
	c.execute("CREATE TABLE if not exists loveBot(login TEXT, message TEXT)")

# пишемо дані в БД
def dataEntry(xlogin, message):
    c.execute("INSERT INTO loveBot (login, message) VALUES (?,?)", (xlogin, message))
    conn.commit()

# валідація валентинки і запис адресата і повідомлення в БД
def valentinka(command, channel):
    response = response_global
    if command.startswith(EXAMPLE_COMMAND + ' ' + "<@"):
        i = 0
        k = 0
        while i<1:
            k += 1
            if (command[k] == '@'):
                i += 1
        if i != 1:
            slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
            return None
        xlogin = ""
        k += 1
        while command[k] != ">":
            xlogin += command[k]
            k += 1
        k += 2
        j = command.find('"', 0, len(command))
        y = command.rfind('"', 0, len(command))
        if j!= -1 and y!= -1 and j != y:
            message = ""
            j += 1
            while j != y:
                message += command[j]
                j += 1
            response = "*Cool!* :sparkling_heart:\nВаша валентинка :gift_heart: буде надіслана отримувачу 14 лютого :blush:\n:kiss:"
            dataEntry(xlogin, message)
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output:
                if AT_BOT in output['text'] and EXAMPLE_COMMAND in output['text'] and "@" in output['text'][1]:
                    return output['text'].split(AT_BOT)[1].strip(), output['channel']
                if len(output['text']) > 0 and not BOT_ID in output['user'] and "D" in output['channel'][0]:
                    slack_client.api_call("chat.postMessage", channel=output['channel'], text=response_global, as_user=True)
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("St. Valentine вийшов на полювання!")
        tableCreate() # створюємо таблицю в БД, якщо не існує. Якщо існує, то йдемо далі.
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if channel:
                if command and channel:
                    valentinka(command, channel)
                else:
                    slack_client.api_call("chat.postMessage", channel=channel, text=response_global, as_user=True)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Давай по новой, Миша, все [NormeError]! (Connection failed. Invalid Slack token or bot ID?)")
