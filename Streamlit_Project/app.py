import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import datetime as dt
import plotly.express as px

@st.cache(persist=True, allow_output_mutation=True)
def load_data():
    data = pd.read_csv('/home/abaral/Coursera Course Files/DataVis/Streamlit_Project/Pedestrians.csv')
    data.rename(mapper= lambda x: str(x).lower(), axis='columns', inplace=True)
    # Remove rows with missing values in longitude and latitude columns
    data.dropna(subset=['longitude', 'latitude'], inplace=True, how='any', axis=0)
    # Clean the date column
    data['date'] = data['date'].apply(lambda x: x[:10])
    # Convert time to string format
    data['time'] = data['time'].apply(lambda x: str(x))
    # add 0s to the beginning of the time string until it is of length 4
    data['time'] = data['time'].apply(lambda x: x if len(x) == 4 else '0'*(4-len(x)) + x)
    # Convert time column from military time to standard time
    data['time'] = data['time'].apply(lambda x: dt.datetime.strptime(x, '%H%M').strftime('%I:%M %p'))
    # Add date_time column
    data['date_time'] = data['date'] + ' ' + data['time']
    # Convert date_time column to datetime format
    data['date_time'] = pd.to_datetime(data['date_time'])
    data['fatal_no'].replace('<Null>', 0, inplace=True)
    data['fatal_no'] = data['fatal_no'].astype(int)
    data['time_of_day'] = data['hour'].apply(lambda x: 'Morning' if x < 12 else 'Afternoon' if x < 18 else 'Evening')
    return data

data = load_data()
original_data = data.copy()

st.write(
    """
    ### Toronto Vehicle Collision Data Analysis and Visualization
    """
)

midpoint = (np.average(data['latitude']), np.average(data['longitude']))

year_slider = st.slider('Year to look at', 2006, 2020, 2016)
# Filter data to only include rows where the hour is equal to the hour selected
year_data = data[data['date_time'].dt.year == year_slider]

if st.checkbox('Show all years'):
    year_data = original_data

# fatality_slider = st.slider('Fatality Slider', 0, 78, 50)
# year_data = year_data.query('fatal_no >= @fatality_slider')

st.write(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state={
        'latitude': midpoint[0],
        'longitude': midpoint[1],
        'zoom': 10,
        'pitch': 50,
    },
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=year_data[['latitude', 'longitude', 'date_time', 'time', 'date', 'street1', 'street2', 'fatal_no']],
            get_position=['longitude', 'latitude'],
            get_fill_color=[200, 0, 0, 150],
            get_radius=100,
            pickable=True,
            auto_highlight=True,
        )
    ],
    tooltip={
        'html': '<b>Date & Time</b>: {date} {time} <br> <b>Street intersection</b>: {street1} & {street2}',
        'style': {'backgroundColor': 'steelblue', 'color': 'white'}
    }
))

hour_slider = st.slider('Hour to look at', 0, 23, 17)
hour_data = data[data['date_time'].dt.hour == hour_slider]

if st.checkbox('Show all hours', value=True):
    hour_data = data

st.write(
    pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v9',
        initial_view_state={
            'latitude': midpoint[0],
            'longitude': midpoint[1],
            'zoom': 10,
            'pitch': 50,
        },
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=hour_data[['latitude', 'longitude', 'date_time', 'time', 'date', 'street1', 'street2', 'fatal_no']],
                get_position=['longitude', 'latitude'],
                radius=100,
                extruded=True,
                pickable=True,
                elevation_scale=4,
                elevation_range=[0, 1000],
                auto_highlight=True,
            )
        ],
        tooltip={
            'html': 'Elevation value: {elevationValue}',
            'style': {'backgroundColor': 'steelblue', 'color': 'white'}
        }
    )
)

grouped_data = data.groupby('injury').count()['index_'].drop('<Null>')
fig = px.bar(grouped_data, x=grouped_data.index, y=grouped_data.values)
fig.update_layout(title='Number of Collisions by Injury Type', xaxis_title='Injury Type', yaxis_title='Number of Collisions'
                , title_x=0.5)
st.write(fig)