# Import required libraries and modules
import pandas as pd
import numpy as np
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import folium

# Create DataFrame from the shootings data
df = pd.read_csv('Shootings_and_Firearm_Discharges.csv')

# Take sample of the dataframe with 350 random rows with random seed of 1
df = df.sample(350, random_state=1)

# Create a map of Toronto
map_toronto = folium.Map(location=[43.6532, -79.3832], zoom_start=11)

# Add markers to the map for each shooting

# Create dash app
app = dash.Dash(__name__)

# Dash layout
app.layout = html.Div(children=[
    html.H1(children='Shootings and Firearm Discharges'),
    ]
)