import requests
import json
import time
import datetime

def JSONRequester(URL):
    r = requests.get(URL)  # <=== Requete URL

    json_data = json.loads(r.text)
    j = json.dumps(json_data, ensure_ascii=False)
    JSON = json.loads(j)

    return JSON


def get_time():
    tz = pytz.timezone('Europe/Berlin')
    berlin_now = datetime.datetime.now(tz)
    return berlin_now.strftime('%d-%m-%Y %H:%M:%S')
