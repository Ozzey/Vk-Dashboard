import requests
import json
from pprint import pprint
from keys import keys

ACCESS_TOKEN = keys["ACCESS_TOKEN"]
user_id = keys["user_id"]

def user_key():
    return keys['user_id']

class get:
    def followers(val="count",offset=0,fields=None,name_case=None,v=5.131):
        response = requests.get(
            f'https://api.vk.com/method/users.getFollowers?v={v}&offset={offset}&fields={fields}&name_case={name_case}&access_token={ACCESS_TOKEN}')
        dict = response.json()

        if (val == "count"):
            return dict['response']['count']

        return response

    #------------------------------------------------------------------
    def friends(val="count",id = user_key(),offset=0,count=0,fields=None,name_case=None,v=5.131):

        response = requests.get(
            f'https://api.vk.com/method/friends.get?v={v}&user_id={id}&offset={offset}&count={count}&fields={fields}&name_case={name_case}&access_token={ACCESS_TOKEN}')

        dict = response.json()

        if (val=="count"):
            return dict['response']['count']

        return response
    #--------------------------------------------------------------#
    def requests(val="count",
                     offset=0,
                     count=0,
                     fields=None,
                     name_case=None,
                     v=5.131,
                     extended=0,
                     need_mutual=0,
                     out=0,
                     ):

        response = requests.get(
            f'https://api.vk.com/method/friends.getRequests?v={v}&offset={offset}&count={count}&fields={fields}&extended={extended}&need_mutual={need_mutual}&out={out}name_case={name_case}&access_token={ACCESS_TOKEN}')

        dict = response.json()

        if (val=="count"):
            return dict['response']['count']

        return response
    #--------------------------------------------------------------#

    def counter(val=None):
        response = requests.get(
            f'https://api.vk.com/method/account.getCounters?v={5.131}&access_token={ACCESS_TOKEN}')

        dict = response.json()
        if(val==None):
            return response

        return dict['response'][val]


    def groups(val="count",
               fields=None,
                    user_id=user_key(),
                     offset=0,
                     count=0,
                     extended=1):

        response = requests.get(
            f'https://api.vk.com/method/groups.get?v={5.131}&fields={fields}&user_id={user_id}&offset={offset}&count={count}&extended={extended}&&access_token={ACCESS_TOKEN}')

        dict = response.json()
        if (val == "count"):
            return dict['response']['count']

        return response


class user:
    def get(id=user_key(),fields='photo_100'):
        response = requests.get(
            f'https://api.vk.com/method/users.get?v={5.131}&user_id={id}&fields={fields}&access_token={ACCESS_TOKEN}')

        dict = response.json()
        return dict


