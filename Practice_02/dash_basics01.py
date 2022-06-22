# Import required packages
import pandas as pd
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

# Read the data
airline_data = pd.read_csv('airline_2m.csv',
                          encoding = "ISO-8859-1",
                          dtype={'Div1Airport': str, 'Div1TailNum': str,
                                 'Div2Airport': str, 'Div2TailNum': str})

app = dash.Dash(__name__)

# Design dash app layout
app.layout = html.Div(children=[html.H1('Airline Dashboard',
                                        style={'text-align': 'center', 'color': colors['text'], 'font-size': 40, 'font-family': 'Bebas Neue'}),
                                   html.Div(['Input: ', dcc.Input(id='input-yr', value='2010',
                                   type='number', style={'height': '30px', 'width': '100px', 'font-size': 35}),],
                                   style={'text-align': 'center', 'color': colors['text'], 'font-size': 30, 'font-family': 'Bebas Neue'}),
])
