import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import datetime as dt
import plotly.express as px

@st.cache(persist=True, allow_output_mutation=True) # cache the dataframe for faster loading
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
    data['time_of_day'] = data['hour'].apply(lambda x: 'Morning' if x < 12 else 'Afternoon' if x < 18 else 'Evening/Night')
    return data

data = load_data()
original_data = data.copy()

st.write(
    """
    ### Toronto Vehicle-Pedestrian Collision Analysis and Visualization
    """
)

midpoint = (np.average(data['latitude']), np.average(data['longitude'])) # get the midpoint of the coordinates

year_slider = st.slider('Filter by year', 2006, 2020, 2016)
# Filter data to only include rows where the hour is equal to the hour selected
year_data = data[data['date_time'].dt.year == year_slider]
year_checkbox = st.checkbox('Show all years', value=False)

if year_checkbox:
    year_data = original_data
    # Make the year_slider disappear
    year_slider = st.empty()
    st.markdown('<center>Scatter Plot of Collisions Between 2006 and 2020</center>', unsafe_allow_html=True)
else:
    st.markdown('<center>Scatter Plot of Collisions During Year %s</center' % (year_slider), unsafe_allow_html=True)

# fatality_slider = st.slider('Fatality Slider', 0, 78, 50)
# year_data = year_data.query('fatal_no >= @fatality_slider')

st.write(pdk.Deck(
    # map_style='mapbox://styles/mapbox/light-v9',
    # Contrasting map style
    map_style='mapbox://styles/mapbox/dark-v9',
    initial_view_state={
        'latitude': midpoint[0],
        'longitude': midpoint[1],
        'zoom': 10,
        'pitch': 50,
    },
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=year_data[['latitude', 'longitude', 'date_time', 'time', 'date', 'street1', 'street2', 'injury']],
            get_position=['longitude', 'latitude'],
            get_fill_color=[200, 0, 0, 150],
            get_radius=110,
            pickable=True,
            auto_highlight=True,
        )
    ],
    tooltip={
        'html': '<b>Date & Time</b>: {date} {time} <br> <b>Street intersection</b>: {street1} & {street2} <br> <b>Injury</b>: {injury}',
        'style': {'backgroundColor': 'steelblue', 'color': 'white'}
    }
))

# hour_slider = st.slider('Hour to look at', 0, 23, 17)
time_of_day_dropdown = st.selectbox('Filter by time of day', ['Morning', 'Afternoon', 'Evening/Night'])
hour_data = data[data['time_of_day'] == time_of_day_dropdown]

if st.checkbox('Show all hours', value=True):
    hour_data = data

st.markdown('<center>Map of Collision Clusters Filtered by Time of Day</center>', unsafe_allow_html=True)

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

grouped_injury = data.groupby('injury').count()['index_'].drop('<Null>')
injury_fig = px.bar(grouped_injury, x=grouped_injury.index, y=grouped_injury.values)
injury_fig.update_layout(title='Number of Collisions by Injury Type', xaxis_title='Injury Type', yaxis_title='Number of Collisions'
                , title_x=0.5)
# injury_fig.update_traces(mode='markers+lines', hoverinfo='all')
grouped_time_of_day = data.groupby('time_of_day').count()['index_']
time_of_day_fig = px.bar(grouped_time_of_day, x=grouped_time_of_day.index, y=grouped_time_of_day.values)
time_of_day_fig.update_layout(title='Number of Collisions by Time of Day', xaxis_title='Time of Day', yaxis_title='Number of Collisions'
                        , title_x=0.5)
# Change the hover text to include the date and time

st.write(time_of_day_fig)
st.write(injury_fig)