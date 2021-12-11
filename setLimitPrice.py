from database import SelectTable
from database import UpdateTable
import requests
import json

selectTable = SelectTable.SelectTable()
notifications = selectTable.allNotifications()

baseUrl = 'https://indodax.com/api/ticker/'

for notif in notifications:
    endpoint = notif['coin_name'].lower() + 'idr'
    response = requests.get(baseUrl + endpoint)
    jsonResponse = response.json()

    coinLimitPrice = jsonResponse['ticker']['last']

    updateTable = UpdateTable.UpdateTable()
    updateTable.notification(notif, coinLimitPrice)