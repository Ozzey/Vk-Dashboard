import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import plotly.express as px
from dash.dependencies import Input, Output

from functions import saveClass,getClass,graphs

from app import app
from app import server


dfriends = getClass.percentage("friends")
dfollowers = getClass.percentage("followers")


body = dbc.Container(className="body",children=[

        dbc.Row(html.Div(className="header",children=[html.H1("STATISTICS",className="heading"),
                          html.Div(className='flex',
                                   children=[html.Img(src=getClass.image(),className='round'),
                                             html.H4(getClass.username(),
                                                     className="heading"),
                                             ])])),

        dbc.Row(
            dbc.Col(className="bigRow",children=[
                    html.Div(className="stats",children=[html.H3("Friends",className="card-title"),
                                                         html.H4(f'{getClass.data()["Friends"]} people'),

                                                         html.Div(className="sub",children=[
                                                                html.H6(f'M : {dfriends["male"]}%',className="card-content"),
                                                                html.H6(f' || ',className="card-content"),
                                                                html.H6(f'F : {dfriends["female"]}%',className="card-content")])
                                                         ]),

                    html.Div(className="stats",children=[html.H3("Followers",className="card-title"),
                                                         html.H4(f'{getClass.data()["Followers"]} people',),
                                                         html.Div(className="sub", children=[
                                                             html.H6(f'M : {dfollowers["male"]}%',
                                                                     className="card-content"),
                                                             html.H6(f' || ', className="card-content"),
                                                             html.H6(f'F : {dfollowers["female"]}%',
                                                                     className="card-content")])
                                                         ]),
                    html.Div(className="stats",children=[html.H3("Groups",className="card-title"),
                                                         html.H4(f'{getClass.data()["Groups"]} groups')]),
            ])
        ),

        dbc.Row(
            dbc.Col(className="bigRow",children=[
                    html.Div(className="charts_line",children=[html.H3("Friends Network",className="card-title"),graphs.cyto()]),
                    html.Div([html.Div(className="charts_pie",children=[html.H3("Sex Ratio",className="card-title"),dcc.Graph(id="graph",figure=graphs.pi(),style={'height': '80%'})]),
                                                              html.Div(className="filler",children=[html.H3("Age",className="card-title"),dcc.Graph(id='bar',figure=graphs.age(),style={'height': '80%'})]),
                             ])
            ])
        ),

        dbc.Row(
            dbc.Col(className="bigRow", children=[
                html.Div(className="charts_choro", children=[html.H3("Geo-Location Stats", className="card-title"),dcc.Graph(id="gr",figure=graphs.choro(),style={'height': '80%'})]),
                html.Div(className="charts_pill", children=[html.H3("City", className="card-title"),dcc.Graph(id="surf",figure=graphs.citysurf(),style={'height': '80%'})]),
            ])
        ),

],fluid=True)


nav = dbc.Container( className= "side-bar", children=[
        dbc.Col(children=[html.Img(src=app.get_asset_url('logo.svg'))],style={"background-color":"transparent"}),
])



app.layout = html.Div(className="main-body", children=[
    dbc.Row(dbc.Col(className="parent", children=[nav,body]))
])



if __name__ == '__main__':
    app.run_server(port=6969,debug=True)