# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

# Read the airline data into a DataFrame
airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str,
                                      'Div2Airport': str, 'Div2TailNum': str})

# Create a Dash application
app = dash.Dash(__name__)

# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 component
# Add a html.Div and core input text component
# Finally, add graph component.
app.layout = html.Div(children=[html.H1('Airline Performance Dashboard',
                                        style={'text-align': 'center', 'color': '#503D36', 'font-size': 40, 'font-family': 'Bebas Neue'}),
                                html.Div(["Input Year", dcc.Input(id='input-year', value=2010, type='number',
                                                                style={'width': '100%', 'font-size': 35, 'font-family': 'Bebas Neue'})],
                                        style={'text-align': 'center', 'color': '#503D36', 'font-size': 40, 'font-family': 'Bebas Neue'}),
                                html.Br(),
                                html.Br(),
                                html.Div(dcc.Graph(id='line-plot')),
                                ])

# add callback decorator
@app.callback(Output(component_id='line-plot', component_property='figure'), Input(component_id='input-year', component_property='value'))

#