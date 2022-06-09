from vk_wrapper import get,user
import pandas as pd
import numpy as np
from pprint import pprint
import json
import plotly.graph_objects as go
import plotly.express as px
import dash_cytoscape as cyto
from keys import keys
from datetime import date, datetime


def calculate_age(dt):
    try:
        born = datetime.strptime(dt, '%d.%m.%Y')
        born.strftime('%Y-%m-%d').replace('-0', '-')
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    except:
        return 0

def user_key():
    return keys['user_id']

class saveClass():
    def saveData():
        data = { "Friends" : get.friends() ,
                 "Followers" : get.followers(),
                 "Groups" : get.groups(),
                 }
        with open("data/data.json", "w") as outfile:
            json.dump(data, outfile)
            print("Data saved!")

    # *************************************************************************#
    def ratio(type='friends'):
        if (type == "friends"):
            response = get.friends("all", fields="sex").json()['response']
            data = response['items']

        else:
            response = get.followers("all", fields="sex").json()['response']
            data = response['items']

        gender = {"female": 0, "male": 0}
        for i in data:
            if i.get('sex') == 1:
                gender["female"] = gender["female"] + 1

            elif i.get('sex') == 2:
                gender["male"] = gender["male"] + 1

            else:
                continue

        return gender

    def save_ratio():
        data={}
        data['friends']=saveClass.ratio('friends')
        data['followers']=saveClass.ratio('follower')
        with open("data/gender.json", "w") as outfile:
            json.dump(data, outfile)
            print("Data saved!")
    #*************************************************************************#
    def save_friends(user_id=user_key()):
        data = get.friends("all",id=user_id,fields='city,bdate,sex,universities,country,single').json()['response']['items']

        # lst = ['id','First','Last','Bday','City','Country','Sex','University','Faculty','Course']
        # df = pd.DataFrame(lst,)

        with open("data/friends.json", "w") as outfile:
            json.dump(data, outfile)
            print("Data saved!")

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
                    "Age": calculate_age(items.get('bdate'))
                }
            )
        dict = pd.DataFrame(d)

        dict.to_csv('data/friends.csv',index=False)



class getClass():
    def data():
        with open("data/data.json") as outfile:
            data = json.load(outfile)
            return data

    def ratio(type="friends"):
        with open("data/gender.json") as outfile:
            dt = json.load(outfile)
        if (type == "friends"):
            data=dt["friends"]
        else:
            data=dt["followers"]
        return data

    def percentage(type):
        with open("data/gender.json") as outfile:
            dt = json.load(outfile)
        if (type == "friends"):
            gender = dt["friends"]
            count = getClass.data()['Friends']
        else:
            gender = dt["followers"]
            count = getClass.data()['Followers']

        gender["female"] = round((gender["female"]/count)*100,1)
        gender["male"] = round((gender["male"] / count)*100,1)
        return gender


    def friends(type="csv"):
        if(type=="json"):
            with open("data/friends.json") as outfile:
                data = json.load(outfile)
                return data
        else:
            data=pd.read_csv('data/friends.csv')
            return data


    def frequency(type='City',size=6):
        df = getClass.friends()
        count=df[type].value_counts()[:size]
        return count

    def username(id=user_key()):
        resp = user.get()['response'][0]
        return resp['first_name']

    def image(id=user_key()):
        resp = user.get()['response'][0]
        return resp['photo_100']



#----------------GRAPH GENERATOR---------------------#

class graphs:
    def pi():
        male_foll = getClass.ratio("friends")["male"]
        female_foll = getClass.ratio("friends")["female"]

        labels = ['Male','Female']
        values = [male_foll,female_foll]
        fig = go.Figure(data=[go.Pie(values=values, labels=labels,pull=[0, 0.2])])
        fig.update_layout(paper_bgcolor='#282C31',autosize=False, height=270,width=300)
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=20))
        fig.update_traces(marker=dict(colors = ["#7F7FD5", "#E786D7"]))
        fig.update_layout(font = dict(color = '#CACACA',size=15))
        return fig


    def choro():
        df = pd.read_csv('data/friends.csv')
        count = df["Country"].value_counts().to_dict()
        dt = pd.DataFrame(count.items(), columns=['country', 'count'])

        fig = go.Figure(
            data={
                'type': 'choropleth',
                'locations': dt['country'],
                'z': dt['count'],
                'locationmode': 'country names',
                'colorscale': 'Purpor',
                'colorbar_title' : "Friends",
                'marker': {
                    'line': {
                        'color': 'rgb(0,0,0)',
                        'width': 2
                    }
                }
            },
            layout={
                'geo': {
                    'projection': {
                        'type': 'orthographic',
                    },
                    'scope': 'world',
                }
            }
        )

        fig.update_layout(paper_bgcolor='#282C31', autosize=False, height=375, width=600)
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=20))
        fig.update_layout(font=dict(color='#CACACA', size=15))
        fig.update_layout(geo_bgcolor='#282C31')

        return fig


    def cyto():
        graph  = {}
        friends = getClass.friends()
        df= friends.head(50)

        with open("data/pictures.json") as outfile:
            pic = json.load(outfile)

        for index, friend in df.iterrows():
            try:
                f = pd.read_csv(f'data/friends_of_friends/{friend["Id"]}.csv')
                mut = df.merge(f)
                arr = mut['First'].tolist()
                graph[friend["First"]] = arr

            except:
                continue

        i=0
        for index, fri in df.iterrows():
            if(graph.get(fri['First'])==None):
                df.drop(labels=i,axis=0)
            i+=1

        nodes = []
        for  index,x in df.iterrows():
            dict={'data' : {'id':x['First'],'label': x['First'].capitalize(),'url':pic[x['First']]}}
            nodes.append(dict)



        edges = []
        for key,value in graph.items():
            for val in value:
                dict={'data':{'source':key,'target':val}}
                edges.append(dict)


        fig = cyto.Cytoscape(
            id='org-chart',
            autoungrabify=False,
            minZoom=0.2,
            maxZoom=5,
            layout={'name': 'circle'},

            style={'width': '100%', 'height': '85%'},

            elements=  nodes+edges,

            stylesheet=[
                {
                    'selector': 'edge', 'style': {'line-color': '#7F7FD5'}
                },
                {
                    'selector': 'node',
                    'style': {
                        'content': 'data(label)',
                        'background-image': 'data(url)',
                        'width': 80,
                        'height': 80,
                        'background-fit': 'cover',

                    }
                },
                {
                    'selector': 'label',  # as if selecting 'node' :/
                    'style': {
                        'content': 'data(label)',  # not to loose label content
                        'color': '#E786D7',
                        'font' : "Open Sans",
                    }
                }
            ]
        )

        return fig

    #****************************************************************************#

    def age():
        df = getClass.friends()
        keys=[0,20,25,30]
        sub=["<20","20-25","26-30","30<"]
        fem=[]
        mem=[]
        sumf=0
        sums=0

        for i in range(len(keys)-1):
            details = df.apply(lambda x: True
                if x['Sex'] == 1 and keys[i]<=x['Age']<=keys[i+1]
                else False, axis=1)
            num_rows = len(details[details == True].index)
            fem.append(num_rows)
            sumf+=num_rows
        fem.append(abs(getClass.ratio()['female']-sumf))

        for i in range(len(keys) - 1):
            details = df.apply(lambda x: True
            if x['Sex'] == 2 and keys[i] <= x['Age'] <= keys[i + 1]
            else False, axis=1)
            num_rows = len(details[details == True].index)
            mem.append(num_rows)
            sums += num_rows
        mem.append(abs(getClass.ratio()['male'] - sums))


        fig= go.Figure(data=[
                go.Bar(name='Male', x=sub,y=mem, marker_color='#7F7FD5'),
                go.Bar(name='Female', x=sub,y=fem,marker_color='#E786D7')
        ])

        fig.update_layout(barmode='group')
        fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="#282C31",
        )

        fig.update_layout(font = dict(color = '#CACACA',size=15))
        fig.update_layout(plot_bgcolor = "#282C31")
        return fig

    #**************************************************************************#

    def citysurf():
        df = pd.read_csv('data/friends.csv')
        count = df["City"].value_counts()[:5].to_dict()
        dt = pd.DataFrame(count.items(), columns=['city', 'count'])
        sum=len(df.index)-dt['count'].sum()
        dt.loc[len(df.index)] = ['Others',sum]

        fig = px.pie(dt, names='city',values='count',
                     color_discrete_sequence=px.colors.sequential.Purpor_r)

        fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="#282C31",
        )

        fig.update_layout(font=dict(color='#CACACA', size=15))
        fig.update_layout(plot_bgcolor="#282C31")
        fig.update_traces(hole=0.3)

        return fig