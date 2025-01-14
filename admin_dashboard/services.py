import requests
import json


BASE_URL="https://nga-states-lga.onrender.com/fetch"

def load_state():
    try:
        res=requests.get(url=BASE_URL)
        if res.status_code == 200:
            return res.json()
        return None
    except Exception as e:
        print(e)
        return None
    

def load_local_govt(state:str):
    try:
        res=requests.get("https://nga-states-lga.onrender.com/?state={}".format(state.name))
        if res.status_code == 200:
            return res.json()
        return None
    except Exception as e:
        print(e)
        return None