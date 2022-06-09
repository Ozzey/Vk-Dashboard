from vk_wrapper import get,user
from functions import getClass
import pandas as pd
import json
import time

def save_friends(user_id):
    data = get.friends("all", id=user_id, fields='city,bdate,sex,universities,country,single').json()['response'][
        'items']

    d = []
    for items in data:
        d.append(
            {
                "Id": items["id"],
                "First": items['first_name'],
                "Last": items['last_name'],
                "Bday": items.get('bdate'),
                "City": items.get('city', {}).get('title'),
                "Country": items.get('country', {}).get('title'),
                "Sex": items['sex'],
            }
        )
    dict = pd.DataFrame(d)
    dict.to_csv(f'data/friends_of_friends/{user_id}.csv', index=False)



def save_pic():
    df=getClass.friends('all')
    pictures={}

    for index,friend in df.iterrows():
        try:
            resp = user.get(friend['Id'])['response']
            pictures[friend['First']]=resp[0].get('photo_100')
            print(friend['First'])
            time.sleep(0.5)

        except:
            pictures[friend['First']] = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgCAAYB1aRkaH1UGWgSr0yIwvWoxTn-LAX4fk-konW966GGkTG2RpD1fJDcA3JEiQrhdw&usqp=CAU'
            print("err ",friend['First'])

    with open("data/pictures.json", "w") as outfile:
        json.dump(pictures, outfile)

