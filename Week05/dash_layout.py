# Import required packages
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output

# Add Dataframe
df = pd.DataFrame({
    'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 'Bananas'],
    'Amount': [4, 3, 2, 2, 4, 1],
    'City': ['SF', 'SF', 'SF', 'NYC', 'MTL', 'NYC']
})
# Add a bar graph figure
fig = px.bar(df, x='Fruit', y='Amount', color='City', barmode='group')

app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1(
        children='Dashboard',
        style={
            'textAlign': 'center'
        }
    ),
    # Create dropdown
    dcc.Dropdown(options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='NYC' # Providing a value to dropdown
    ),
    # Bar graph
    dcc.Graph(id='example-graph-2', figure=fig)

])

# Run Application
if __name__ == '__main__':
    app.run_server()