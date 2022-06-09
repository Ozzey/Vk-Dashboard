import dash
import dash_bootstrap_components as dbc


external_style = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href':"https://use.fontawesome.com/releases/v5.3.1/css/all.css",
        'rel': 'stylesheet',
        'integrity': 'sha384-mzrmE5qonljUremFsqc01SB46JvROS7bZs3IO2EmfFsd15uHvIt+Y8vEf7N7fWAU',
        'crossorigin': 'anonymous'
    }
]



app= dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP, external_style],
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}],
                suppress_callback_exceptions=True)

app.title = "VKontakte Dashboard"
app._favicon = ("assets/favicon.svg")

server=app.server
