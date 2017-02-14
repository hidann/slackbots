# coding=utf-8

import os
import time
import json
import sqlite3
from slackclient import SlackClient

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

# видкриваємо БД
conn = sqlite3.connect('loveBot.db')
c = conn.cursor()

# розсилаємо валентики адресатам
def send():
    c.execute("SELECT * FROM loveBot")
    data = c.fetchall()
    for row in data:
        slack_client.api_call("chat.postMessage", channel=row[0], text="" + row[1], username="lovebot", icon_emoji=":gift_heart:")

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Ща буду спамити валентинками!")
        send()
        print("Готово! Можна йти писати код далі :)")
    else:
        print("Давай по новой, Миша, все [NormeError]!(Connection failed. Invalid Slack token or bot ID?)")
