from database import SelectTable
import requests
import json
from dotenv import load_dotenv
from pathlib import Path
import os

selectTable = SelectTable.SelectTable()
notifications = selectTable.allNotifications()

def checkCoin(notif):
    result = False
    baseUrl = 'https://indodax.com/api/ticker/'
    endpoint = notif['coin_name'].lower() + 'idr'
    response = requests.get(baseUrl + endpoint)
    jsonResponse = response.json()

    coinLastPrice = jsonResponse['ticker']['last']

    if (notif['condition'] == 'less'):
        if (notif['price_limit'] > coinLastPrice):
            sendNotification(notif, coinLastPrice)
            result = True
    elif (notif['condition'] == 'greater'):
        if (notif['price_limit'] < coinLastPrice):
            sendNotification(notif, coinLastPrice)
            result = True
    elif (notif['condition'] == 'equal'):
        if (coinLastPrice == notif['price_limit']):
            sendNotification(notif, coinLastPrice)
            result = True

    return result

def sendNotification(notif, coinLastPrice):
    if (notif['condition'] == 'less' or notif['condition'] == 'greater'):
        message = notif['coin_name'] + ' coin is ' + notif['condition'] + ' than Rp ' + "{:,}".format(int(notif["price_limit"])) + " => @ Rp " + "{:,}".format(int(coinLastPrice))
    else :
        message = notif['coin_name'] + ' coin is ' + notif['condition'] + ' Rp ' + notif['price_limit']

    sendTelegram(message)

def sendTelegram(message):
    env_path = str(Path('.') / '.env')
    load_dotenv(dotenv_path=env_path)
    url = 'https://api.telegram.org/bot'+os.getenv("TELEGRAM_BOT_TOKEN")+'/sendMessage?chat_id='+os.getenv("TELEGRAM_CHAT_ID")+'&text=' + message
    
    response = requests.get(url)

for notif in notifications:
    print (checkCoin(notif))