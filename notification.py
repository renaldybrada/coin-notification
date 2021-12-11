from database import SelectTable
from database import UpdateTable
import requests
import json
from dotenv import load_dotenv
from pathlib import Path
import os

def checkCoin(notif):
    result = {
        "status": False,
        "message": ""
    }
    baseUrl = 'https://indodax.com/api/ticker/'
    endpoint = notif['coin_name'].lower() + 'idr'
    response = requests.get(baseUrl + endpoint)
    jsonResponse = response.json()

    coinLastPrice = jsonResponse['ticker']['last']

    updateTable = UpdateTable.UpdateTable()

    if (notif['condition'] == 'less'):
        if (notif['price_limit'] > coinLastPrice):
            updateTable.notification(notif, coinLastPrice)
            result['status'] = True
    elif (notif['condition'] == 'greater'):
        if (notif['price_limit'] < coinLastPrice):
            updateTable.notification(notif, coinLastPrice)
            result['status'] = Trues
    elif (notif['condition'] == 'equal'):
        if (coinLastPrice == notif['price_limit']):
            result['status'] = True

    if (result['status'] == True):
        result['message'] = formNotifMessage(notif, coinLastPrice)

    return result

def formNotifMessage(notif, coinLastPrice):
    message = ""
    if (notif['condition'] == 'less' or notif['condition'] == 'greater'):
        message = notif['coin_name'] + ' coin is ' + notif['condition'] + ' than Rp ' + "{:,}".format(int(notif["price_limit"])) + " => @ Rp " + "{:,}".format(int(coinLastPrice))
    else :
        message = notif['coin_name'] + ' coin is ' + notif['condition'] + ' Rp ' + notif['price_limit']

    return message

def sendTelegram(message):
    env_path = str(Path('.') / '.env')
    load_dotenv(dotenv_path=env_path)
    url = 'https://api.telegram.org/bot'+os.getenv("TELEGRAM_BOT_TOKEN")+'/sendMessage?chat_id='+os.getenv("TELEGRAM_CHAT_ID")+'&text=' + message
    
    response = requests.get(url)


selectTable = SelectTable.SelectTable()
notifications = selectTable.allNotifications()
messages = []

for notif in notifications:
    checkCoinResult = checkCoin(notif)
    if (checkCoinResult['status']):
        messages.append(checkCoinResult['message'])

if (len(messages) > 0):
    messageSent = '\n=============\n'.join(messages)
    print(messageSent)

    sendTelegram(messageSent)