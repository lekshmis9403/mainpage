
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash import dash_table
from dash.dependencies import Input, Output, State
from sklearn.linear_model import LinearRegression
import numpy as np
from scipy import stats
from dash.dash_table.Format import Group




data = pd.read_csv('Goa_New1.csv', na_values=['NA', 'NaN', 'N/A', 'nan', ''])

# Create a color scale for stations
color_scale = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']


# Step 3: Calculate total rainfall per year
total_rainfall_per_year = data.groupby('Year').sum(numeric_only=True).reset_index()
total_rainfall_per_year['Total_Rainfall'] = total_rainfall_per_year.iloc[:, 9:].sum(axis=1, skipna=True)

# Convert rainfall columns to numeric and handle non-numeric values as NaN
rainfall_columns = [str(day) for day in range(1, 367)]
data[rainfall_columns] = data[rainfall_columns].apply(pd.to_numeric, errors='coerce')

# Reshape the data to have 'Year', 'Day', and 'Rainfall' columns
data_melted = data.melt(id_vars=['Year', 'Station'], value_vars=data.columns[9:], var_name='Day', value_name='Rainfall')

# Convert 'Day' to numeric and create a 'Date' column
data_melted['Day'] = pd.to_numeric(data_melted['Day'], errors='coerce')
data_melted['Date'] = pd.to_datetime(data_melted['Year'].astype(str) + '-' + data_melted['Day'].astype(str), format='%Y-%j')

# Merge station information back into the data
data_melted = pd.merge(data_melted, data[['Year', 'Station', 'District']], on=['Year', 'Station'])



def get_top_5_events(data):
    # Melt the data to convert the columns for each day to rows
    melted_data = pd.melt(data, id_vars=['Station', 'Year'], value_vars=[str(i) for i in range(1, 367)],
                          var_name='Day', value_name='Rainfall')

    # Convert the 'Day' column to numeric
    melted_data['Day'] = pd.to_numeric(melted_data['Day'])

    # Find the top 5 events with maximum rainfall
    top_5_events = melted_data.nlargest(5, 'Rainfall')

    return top_5_events


# Import the CSS file
external_stylesheets = ['style.css']

# Create the Dash app with external stylesheets
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Define a function to convert the day number to date string
def day_to_date(day):
    date = pd.to_datetime('2022-01-01') + pd.DateOffset(days=int(day) - 1)
    return date.strftime('%d %b')  # Updated date format to '%d %b'

# Define dropdown options
district_options = [{'label': district, 'value': district} for district in data['District'].unique()]
default_district = district_options[0]['value']

# Define a background image URL (replace with your image URL)
background_image_url = 'https://images.pexels.com/photos/311039/pexels-photo-311039.jpeg?cs=srgb&dl=pexels-lumn-311039.jpg&fm=jpg'


# Define the custom CSS class for the slider

# Define the layout with your content and background image
app.layout = html.Div([
    html.Div(style={'background-image': f'url("{background_image_url}")',
                    'background-size': 'cover',
                    'position': 'fixed',
                    'top': '0',
                    'left': '0',
                    'width': '100%',
                    'height': '100%',
                    'z-index': '-1'}),

    html.Div([
        html.Img(src='https://upload.wikimedia.org/wikipedia/commons/c/cf/Goamap.png',  # Replace with the actual path to your Goa map image
                 style={'width': '700px', 'height': '500px'}),
        html.H1('Goa Rainfall', style={'text-align': 'center', 'margin-top': '20px'})
    ], style={'text-align': 'center'}),

    dcc.Tabs(id='tabs', value='tab1', children=[
        dcc.Tab(label='Actual Rainfall', value='tab1', style={'backgroundColor': '#BC544B', 'color': 'white'}),
        dcc.Tab(label='Climatology', value='tab2', style={'backgroundColor': '#BC544B', 'color': 'white'}),
        dcc.Tab(label='Extreme Events', value='tab3', style={'backgroundColor': '#BC544B', 'color': 'white'}),
        dcc.Tab(label='Trend', value='tab4', style={'backgroundColor': '#BC544B', 'color': 'white'}),
        dcc.Tab(label='Interannual Variability', value='tab5', style={'backgroundColor': '#BC544B', 'color': 'white'})
    ]),

    html.Div(id='tab-content'),
])

@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'tab1':
        return html.Div([
            html.H2('Actual Rainfall', style={'text-align': 'center'}),

            html.Div([
                html.Div([
                    html.H3('Bar-graph Rainfall Distribution of Goa State', style={
                        'text-align': 'center',
                        'display': 'flex',
                        'justify-content': 'center',
                        'align-items': 'center',
                        'color': 'red'
                    }),
                ], style={
                    'border-left': '2px solid black',
                    'border-right': '2px solid black',
                    'border-bottom':'2px solid black',
                    'border-top':'2px solid black',
                    'padding': '3px',
                    'margin': 'auto',
                    'width': 'fit-content',
                    'background-color': '#D3D3D3'
                }),
            ]),
            html.H3('Select Date'),
            dcc.DatePickerRange(
                id='date-range-picker-bar',
                start_date='1971-01-01',
                end_date='2020-12-31'
            ),

            dcc.Graph(id='rainfall-bar-graph'),

            html.Div([
                html.Div([
                    html.H3('Bar-graph Rainfall distribution of Goa Districts', style={
                        'text-align': 'center',
                        'display': 'flex',
                        'justify-content': 'center',
                        'align-items': 'center',
                        'color': 'red'
                    }),
                ], style={
                    'border-left': '2px solid black',
                    'border-right': '2px solid black',
                    'border-bottom': '2px solid black',
                    'border-top': '2px solid black',
                    'padding': '3px',
                    'margin': 'auto',
                    'width': 'fit-content',
                    'margin-bottom': '20px',
                    'margin-top': '20px',
                    'background-color': '#D3D3D3'


                }),
            ]),

            html.Div([
                html.Div([
                    html.Label('Select Year:', style={'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='year-dropdown-bar-sum',
                        options=[{'label': str(year), 'value': year} for year in data['Year'].unique()],
                        value=data['Year'].min()
                    )
                ], style={'width': '720px', 'margin-right': '20px'}),

                html.Div([
                    html.Label('Select District:', style={'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='district-dropdown-bar-sum',
                        options=[{'label': district, 'value': district} for district in data['District'].unique()],
                        value=data['District'].unique()[0]
                    )
                ], style={'width': '720px'})
            ], style={'display': 'flex', 'margin-bottom': '20px'}),

            html.Div([
                dcc.Graph(id='bar-graph-sum'),
                html.Div(id='rainfall-sum-box',
                         style={'position': 'absolute', 'top': '50%', 'right': '30px', 'background-color': 'lightgray',
                                'padding': '5px'}),
            ], style={'position': 'relative', 'height': '70vh'}),

            html.Div([
                html.Div([
                    html.H3('Monthly Distribution of Rainfall', style={
                        'text-align': 'center',
                        'display': 'flex',
                        'justify-content': 'center',
                        'align-items': 'center',
                        'color': 'red'
                    }),
                ], style={
                    'border-left': '2px solid black',
                    'border-right': '2px solid black',
                    'border-bottom': '2px solid black',
                    'border-top': '2px solid black',
                    'padding': '3px',
                    'margin': 'auto',
                    'width': 'fit-content',
                    'margin-bottom': '20px',
                    'background-color': '#D3D3D3'

                }),
            ]),
            html.Div([
                html.Div([
                    html.Label('Select District:', style={'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='district-dropdown-heatmap',
                        options=district_options,
                        value=default_district,
                        placeholder='Select a district'
                    )
                ], style={'width': '720px', 'margin-right': '20px'}),

                html.Div([
                    html.Label('Select Station:', style={'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='station-dropdown-heatmap',
                        placeholder='Select a station'
                    )
                ], style={'width': '720px'})
            ], style={'display': 'flex', 'margin-bottom': '20px'}),


    html.H4('This is Heatmap Monthly Distribution  of Goa State'),

    html.H4('Select tab', style={'text-align': 'center'}),

    html.Div([
        html.Button('Average Rainfall', id='average-rainfall-button', n_clicks=0,
                style={'width': '300px', 'height': '40px', 'margin-right': '10px'}),
    html.Button('Total Rainfall', id='total-rainfall-button', n_clicks=0,
                style={'width': '300px', 'height': '40px'})
], style={'text-align': 'center', 'margin-top': '10px'}),
    dcc.Graph(id='calendar-heatmap'),

            html.Div([
                html.Div([
                    html.H3('Weekly Distribution of Rainfall', style={
                        'text-align': 'center',
                        'display': 'flex',
                        'justify-content': 'center',
                        'align-items': 'center',
                        'color': 'red'
                    }),
                ], style={
                    'border-left': '2px solid black',
                    'border-right': '2px solid black',
                    'border-bottom': '2px solid black',
                    'border-top': '2px solid black',
                    'padding': '3px',
                    'margin': 'auto',
                    'width': 'fit-content',
                    'margin-bottom': '20px',
                    'margin-top': '20px',
                    'background-color': '#D3D3D3'
                }),
            ]),

            html.Div([
                html.Div([
                    html.Label('Select District:', style={'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='district-dropdown-weekly-heatmap',
                        options=district_options,
                        value=default_district,
                        placeholder='Select a district'
                    )
                ], style={'width': '720px', 'margin-right': '20px'}),

                html.Div([
                    html.Label('Select Station:', style={'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='station-dropdown-weekly-heatmap',
                        placeholder='Select a station'
                    )
                ], style={'width': '720px'})
            ], style={'display': 'flex', 'margin-bottom': '20px'}),

    dcc.Graph(id='calendar-heatmap-weekly'),

])

    elif tab == 'tab2':
        return html.Div([

            html.H3('Select year-range from below slider'),
        dcc.RangeSlider(
            id='year-range-slider-climatology',
            min=data['Year'].min(),
            max=data['Year'].max(),
            step=1,
            marks={str(year): str(year) for year in data['Year'].unique()},
            value=[data['Year'].min(), data['Year'].max()],




                  # Apply the custom CSS class to change slider color
            ),






            html.Div([
                html.Div([
                    html.H3('State Climatology', style={
                        'text-align': 'center',
                        'display': 'flex',
                        'justify-content': 'center',
                        'align-items': 'center',
                        'color': 'red'

                    }),
                ], style={
                    'border-left': '2px solid black',
                    'border-right': '2px solid black',
                    'border-bottom': '2px solid black',
                    'border-top': '2px solid black',
                    'padding': '5px',
                    'margin': 'auto',
                    'width': 'fit-content',
                    'margin-bottom': '20px',
                    'background-color': '#D3D3D3'
                }),
            ]),
            dcc.Graph(id='rainfall-graph-state-wise'),

            html.Div([

                dcc.Graph(id='rainfall-trend-state'),
            ]),

            html.Div([
                html.Div([
                    html.H3('District Climatology', style={
                        'text-align': 'center',
                        'display': 'flex',
                        'justify-content': 'center',
                        'align-items': 'center',
                        'color': 'red'
                    }),
                ], style={
                    'border-left': '2px solid black',
                    'border-right': '2px solid black',
                    'border-bottom': '2px solid black',
                    'border-top': '2px solid black',
                    'padding': '5px',
                    'margin': 'auto',
                    'width': 'fit-content',
                    'margin-bottom': '20px',
                    'margin-top': '20px',
                    'background-color': '#D3D3D3'
                }),
            ]),

            html.Div([
                html.Label('Select District:', style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='district-dropdown-climatology',
                    options=[{'label': district, 'value': district} for district in data['District'].unique()],
                    value=data['District'].unique()[0]
                )
            ], style={'width': '100%'}),

            dcc.Graph(id='rainfall-district-bar-graph-climatology'),
            dcc.Graph(id='trend-climatology-district'),

            html.Div([
                html.Div([
                    html.H3('Station Climatology', style={
                        'text-align': 'center',
                        'display': 'flex',
                        'justify-content': 'center',
                        'align-items': 'center',
                        'color': 'red'

                    }),
                ], style={
                    'border-left': '2px solid black',
                    'border-right': '2px solid black',
                    'border-bottom': '2px solid black',
                    'border-top': '2px solid black',
                    'padding': '5px',
                    'margin': 'auto',
                    'width': 'fit-content',
                    'margin-bottom': '20px',
                    'margin-top':'20px',
                    'background-color': '#D3D3D3'
                }),
            ]),
            html.Div([
                html.Label('Select Station:', style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='station-dropdown-climatology',
                    options=[{'label': station, 'value': station} for station in data['Station'].unique()],
                    value=data['Station'].unique()[0]

                )
            ], style={'width': '100%'}),
            dcc.Graph(id='rainfall-bar-graph-climatology'),

        ])


    elif tab == 'tab3':
        return html.Div([
            html.H3('Extreme Events of Goa State', style={'text-align': 'center'}),
            html.Label('Select Date from calender', style={'font-weight': 'bold'}),
            html.Div([

                dcc.DatePickerRange(
                    id='date-range-picker',
                    start_date='1971-01-01',
                    end_date='2020-12-31'
                ),
            ]),
            dash_table.DataTable(
                id='top-events-table-1',  # Table 1
                columns=[
                    {'name': 'Date', 'id': 'Date'},
                    {'name': 'District', 'id': 'District'},
                    {'name': 'Station', 'id': 'Station'},
                    {'name': 'Rainfall (mm)', 'id': 'Rainfall'},
                    {'name': 'Year', 'id': 'Year'}
                ],
                style_data={'whiteSpace': 'normal', 'textAlign': 'center'},
                style_cell={'textAlign': 'center'},
                style_data_conditional=[
                    {'if': {'column_id': 'Date'}, 'textAlign': 'left'}
                ]
            ),
            html.H3('Extreme-Events of District', style={'text-align': 'center'}),
            html.Label('Select District', style={'font-weight': 'bold'}),
            html.Div([

                dcc.Dropdown(
                    id='district-dropdown',
                    options=[
                        {'label': district, 'value': district} for district in data_melted['District'].unique()
                    ],
                    placeholder='Select a district',
                    style={'width': '450px'},
                    value=data_melted['District'].unique()[0]  # Set the first district as default value
                ),
            ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center', 'margin-bottom': '20px'}),
            dash_table.DataTable(
                id='top-events-table-2',  # Table 2
                columns=[
                    {'name': 'Date', 'id': 'Date'},
                    {'name': 'District', 'id': 'District'},
                    {'name': 'Station', 'id': 'Station'},
                    {'name': 'Rainfall (mm)', 'id': 'Rainfall'},
                    {'name': 'Year', 'id': 'Year'}
                ],
                style_data={'whiteSpace': 'normal', 'textAlign': 'center'},
                style_cell={'textAlign': 'center'},
                style_data_conditional=[
                    {'if': {'column_id': 'Date'}, 'textAlign': 'left'}
                ]
            ),

            html.H3('Extreme-Events of Station', style={'text-align': 'center'}),
            html.Div([
                html.Div([
                    html.Label('Select District:', style={'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='district-dropdown-top',
                        options=[
                            {'label': district, 'value': district} for district in data_melted['District'].unique()
                        ],
                        placeholder='Select a district',
                        style={'width': '550px'},
                        value=data_melted['District'].unique()[0]
                    )
                ], style={'width': '720px', 'margin-right': '20px'}),

                html.Div([
                    html.Label('Select Station:', style={'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='station-dropdown',
                        placeholder='Select a station',
                        style={'width': '550px'},
                        value=data_melted['Station'].unique()[0]
                    )
                ], style={'width': '720px'})
            ], style={'display': 'flex', 'margin-bottom': '20px'}),

            dash_table.DataTable(
                id='top-events-table-3',  # Table 3
                columns=[
                    {'name': 'Date', 'id': 'Date'},
                    {'name': 'District', 'id': 'District'},
                    {'name': 'Station', 'id': 'Station'},
                    {'name': 'Rainfall (mm)', 'id': 'Rainfall'},
                    {'name': 'Year', 'id': 'Year'}
                ],
                style_data={'whiteSpace': 'normal', 'textAlign': 'center'},
                style_cell={'textAlign': 'center'},
                style_data_conditional=[
                    {'if': {'column_id': 'Date'}, 'textAlign': 'left'}
                ]
            ),
        ])
    elif tab == 'tab4':
        return html.Div([
            html.Div([
                html.Div([
                    html.H3('Rainfall Trend of State', style={
                        'text-align': 'center',
                        'display': 'flex',
                        'justify-content': 'center',
                        'align-items': 'center',
                        'color': 'red'
                    }),
                ], style={
                    'border-left': '2px solid black',
                    'border-right': '2px solid black',
                    'border-bottom': '2px solid black',
                    'border-top': '2px solid black',
                    'padding': '5px',
                    'margin': 'auto',
                    'width': 'fit-content',
                    'margin-bottom': '20px',
                    'margin-top': '20px',
                    'background-color': '#D3D3D3'
                }),
            ]),
            dcc.Graph(id='trend-state-wise'),

            html.Div([
                html.Div([
                    html.H3('Rainfall Trend of Districts', style={
                        'text-align': 'center',
                        'display': 'flex',
                        'justify-content': 'center',
                        'align-items': 'center',
                        'color': 'red'
                    }),
                ], style={
                    'border-left': '2px solid black',
                    'border-right': '2px solid black',
                    'border-bottom': '2px solid black',
                    'border-top': '2px solid black',
                    'padding': '5px',
                    'margin': 'auto',
                    'width': 'fit-content',
                    'margin-bottom': '20px',
                    'margin-top': '20px',
                    'background-color': '#D3D3D3'
                }),
            ]),

            dcc.Dropdown(
                id='district-dropdown-trend-state',
                options=[{'label': district, 'value': district} for district in data['District'].unique()],
                value=None,
                placeholder="Select a district"
            ),
            dcc.Graph(id='trend-District-wise-regression'),
            # Line chart for rainfall trend

            html.Div([
                html.Div([
                    html.H3('Rainfall Trend of Station', style={
                        'text-align': 'center',
                        'display': 'flex',
                        'justify-content': 'center',
                        'align-items': 'center',
                        'color': 'red'
                    }),
                ], style={
                    'border-left': '2px solid black',
                    'border-right': '2px solid black',
                    'border-bottom': '2px solid black',
                    'border-top': '2px solid black',
                    'padding': '5px',
                    'margin': 'auto',
                    'width': 'fit-content',
                    'margin-bottom': '20px',
                    'margin-top': '20px',
                    'background-color': '#D3D3D3'
                }),
            ]),
            dcc.Dropdown(

                id='station-dropdown-trend',

                options=[{'label': district, 'value': district} for district in data['District'].unique()],
                value=None,
                placeholder="Select Station"
            ),
            dcc.Graph(id='rainfall-trend-station'),
        ])
    elif tab == 'tab5':
        return html.Div([
            html.Div([
                html.Div([
                    html.H3('Interannual Variability of Total Rainfall', style={
                        'text-align': 'center',
                        'display': 'flex',
                        'justify-content': 'center',
                        'align-items': 'center',
                        'color': 'red'
                    }),
                ], style={
                    'border-left': '2px solid black',
                    'border-right': '2px solid black',
                    'border-bottom': '2px solid black',
                    'border-top': '2px solid black',
                    'padding': '5px',
                    'margin': 'auto',
                    'width': 'fit-content',
                    'margin-bottom': '20px',
                    'margin-top': '20px',
                    'background-color': '#D3D3D3'
                }),
            ]),
            html.Div([
                html.Label('Select District:', style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='district-dropdown-total',
                    options=[{'label': district, 'value': district} for district in data['District'].unique()],
                    value=data['District'].unique()[0],
                    style={'width': '100%'}
                )
            ], style={'width': '100%', 'margin-right': '20px'}),

            dcc.Graph(id='histogram-chart'),
            html.Div([
                html.Div([
                    html.H3('Percentage Distribution Of annual Rainfall in Goa', style={
                        'text-align': 'center',
                        'display': 'flex',
                        'justify-content': 'center',
                        'align-items': 'center',
                        'color': 'red'
                    }),
                ], style={
                    'border-left': '2px solid black',
                    'border-right': '2px solid black',
                    'border-bottom': '2px solid black',
                    'border-top': '2px solid black',
                    'padding': '5px',
                    'margin': 'auto',
                    'width': 'fit-content',
                    'margin-bottom': '20px',
                    'margin-top': '20px',
                    'background-color': '#D3D3D3'

                }),
            ]),
            html.Div([
                html.Label('Select Year:', style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='year-dropdown-pie',
                    options=[{'label': str(year), 'value': year} for year in data['Year'].unique()],
                    value=data['Year'].min(),
                    style={'width': '100%'}
                )
            ], style={'width': '100p%', 'margin-right': '20px'}),

            dcc.Graph(id='pie-chart'),
        ])


    return html.Div()  # Empty div as default

# Rest of your callback functions here...




# Create a callback to update the bar graph
@app.callback(
    Output('rainfall-bar-graph', 'figure'),
    Input('date-range-picker-bar', 'start_date'),
    Input('date-range-picker-bar', 'end_date')
)
def update_bar_graph(start_date, end_date):
    # Convert start_date and end_date to pandas datetime format
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter data based on selected date range
    filtered_data = data[
        (data['Year'] >= start_date.year) & (data['Year'] <= end_date.year)
        ]

    # Reshape the data for plotting
    melted_data = filtered_data.melt(id_vars=['Year', 'District', 'Station'],
                                     value_vars=data.columns[9:],
                                     var_name='Day', value_name='Rainfall')
    melted_data['Day'] = pd.to_numeric(melted_data['Day'], errors='coerce')
    melted_data['Date'] = pd.to_datetime(melted_data['Year'].astype(str) + '-' + melted_data['Day'].astype(str),
                                         format='%Y-%j')

    # Filter the melted data for the selected date range
    melted_data = melted_data[(melted_data['Date'] >= start_date) & (melted_data['Date'] <= end_date)]

    # Create a custom color scale for the bars (you can adjust these colors)
    custom_colors = ['#0066cc', '#0055aa', '#004488', '#003366', '#002244']

    # Create the bar graph using Plotly Express with custom color scale and 'Rainfall' as color
    fig = px.bar(melted_data, x='Date', y='Rainfall',
                 title='Rainfall Data',
                 labels={'Date': 'Date', 'Rainfall': 'Rainfall (mm)'},
                 color='Station',
                 color_discrete_sequence=custom_colors,
                 height=500,
                 hover_data=['Station'])



    # Format the x-axis date labels
    fig.update_xaxes(type='date', tickformat='%b %Y', showgrid=False)

    # Add hover template to display actual rainfall values and station information
    hover_template = '<b>Date:</b> %{x|%d %b %Y}<br><b>Rainfall:</b> %{y:.0f} mm<br><b>Station:</b> %{customdata}'
    fig.update_traces(hovertemplate=hover_template, marker_line_color='black')

    return fig

# Define the callback function for the bar graph
@app.callback(
    Output('bar-graph-sum', 'figure'),
    Output('rainfall-sum-box', 'children'),  # Output for the rainfall sum box
    [Input('year-dropdown-bar-sum', 'value'),
     Input('district-dropdown-bar-sum', 'value')]
)
def update_graph(year, district):
    if pd.isna(year):
        # If the year selected is NaN, show data for all years (include NaN years)
        filtered_data = data[data['District'] == district]
        title = f'Rainfall Range for {district} - All Years'
    else:
        filtered_data = data[(data['Year'] == year) & (data['District'] == district)]
        title = f'Rainfall Range for {district} - {year}'

    grouped_data = filtered_data.groupby('Station')

    # Create a list to store data for the bar chart
    chart_data = []

    for station, (_, station_data) in zip(grouped_data.groups.keys(), grouped_data):
        y_values_flat = station_data[rainfall_columns].mean().apply(pd.to_numeric, errors='coerce').tolist()
        y_values_flat = [0 if pd.isna(value) else value for value in y_values_flat]       #filling o with nan
        day_labels = [day_to_date(day) for day in rainfall_columns]
        chart_data.extend(list(zip([station] * len(day_labels), day_labels, y_values_flat)))

    # Create a DataFrame from the list of data for the bar chart
    df = pd.DataFrame(chart_data, columns=['Station', 'Day', 'Rainfall'])

    # Check if the selected year is NaN
    if pd.isna(year):
        # Add data for NaN year to the DataFrame
        nan_year_data = data[data['Year'].isna() & (data['District'] == district)]
        nan_year_values = nan_year_data[rainfall_columns].mean().apply(pd.to_numeric, errors='coerce').tolist()
        nan_year_day_labels = [day_to_date(day) for day in rainfall_columns]
        df = pd.concat([df, pd.DataFrame({'Station': [station] * len(nan_year_day_labels),
                                          'Day': nan_year_day_labels,
                                          'Rainfall': nan_year_values})])

    fig = px.bar(df, x='Station', y='Rainfall', color='Station',
                 labels={'Station': 'Station', 'Rainfall': 'Rainfall'},
                 title=title,
                 color_continuous_scale='jet',
                 height=500)

    # Map day values to day labels for hover information
    day_mapping = {day: day_to_date(day) for day in rainfall_columns}  # Create day_mapping here
    fig.update_layout(hovermode='closest')

    hovertemplate = '<b>Station:</b> %{x}<br><b>Date:</b> %{customdata}<br><b>Rainfall:</b> %{y:.2f}'  # Corrected hovertemplate
    fig.update_traces(hovertemplate=hovertemplate,
                      customdata=df['Day'])  # Corrected customdata


 # Calculate the sum of rainfall for all stations
    total_rainfall = df['Rainfall'].sum()
    # Create a string to display the sum in the rainfall sum box
    rainfall_sum_box_content = html.P(f"Total Rainfall for All Stations: {total_rainfall:.2f} mm")

    return fig, rainfall_sum_box_content







# Define the callback function to update station dropdown based on the selected district
@app.callback(
    Output('station-dropdown-heatmap', 'options'),
    Output('station-dropdown-heatmap', 'value'),  # Add a second output to set the default value
    [Input('district-dropdown-heatmap', 'value')]
)
def update_station_options(selected_district):
    # Filter data for the selected district
    filtered_data = data[data['District'] == selected_district]
    # Define station options for the selected district
    station_options = [{'label': station, 'value': station} for station in filtered_data['Station'].unique()]
    default_station = station_options[0]['value']
    return station_options, default_station  # Return both options and default value

# Define the callback function to update the heatmap based on the selected district and station
@app.callback(
    Output('calendar-heatmap', 'figure'),
    [Input('district-dropdown-heatmap', 'value'),
     Input('station-dropdown-heatmap', 'value'),
     Input('total-rainfall-button', 'n_clicks'),
     Input('average-rainfall-button', 'n_clicks')],
    [State('calendar-heatmap', 'figure')]
)
def update_heatmap(selected_district, selected_station, total_clicks, average_clicks, figure):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Filter data for the selected district and station
    filtered_data = data[(data['District'] == selected_district) & (data['Station'] == selected_station)]

    # Reshape the data for heatmap
    melted_data = pd.melt(filtered_data, id_vars=['Year'], value_vars=[str(i) for i in range(1, 367)],
                          var_name='Day', value_name='Rainfall')

    # Convert Day column to numeric
    melted_data['Day'] = pd.to_numeric(melted_data['Day'])

    # Calculate the weekly differences of days
    melted_data['Week'] = (melted_data['Day'] - 1) // 7 + 1

    # Calculate the month from the 'Day' column
    melted_data['Month'] = melted_data['Day'].apply(lambda day: (pd.to_datetime('2022-01-01') + pd.to_timedelta(day - 1, unit='D')).month)

    if button_id == 'total-rainfall-button':
        rainfall_calculation = melted_data.groupby(['Year', 'Month'])['Rainfall'].sum().reset_index()
    else:
        rainfall_calculation = melted_data.groupby(['Year', 'Month'])['Rainfall'].mean().reset_index()

    custom_colorscale = [
        [0, 'rgb(255, 255, 255)'],  # 0 mm (white)
        [0.01, 'rgb(173, 216, 230)'],  # Light blue
        [0.1, 'rgb(135, 206, 235)'],  # Lighter blue
        [0.25, 'rgb(0, 0, 255)'],  # Blue
        [0.5, 'rgb(0, 0, 128)'],  # Dark blue
        [1.0, 'rgb(0, 0, 0)']  # 1 mm and above (black)
    ]

    fig = go.Figure(go.Heatmap(x=rainfall_calculation['Month'], y=rainfall_calculation['Year'],
                               z=rainfall_calculation['Rainfall'],
                               colorscale=custom_colorscale, colorbar_title='Rainfall'))

    fig.update_layout(title=f'Rainfall Monthly Calendar for District: {selected_district}, Station: {selected_station}',
                      xaxis_title='Months',
                      yaxis_title='Year',
                      xaxis=dict(tickvals=list(range(1, 13)),
                                 ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']),
                      yaxis=dict(autorange='reversed'))

    # Create custom hovertemplate
    hovertemplate = 'Year: %{y}<br>Month: %{customdata}<br>Rainfall: %{z:.0f} mm<br>'
    fig.update_traces(hovertemplate=hovertemplate,
                      customdata=[month for month in rainfall_calculation['Month']])

    hovertext = []
    for year, month, rainfall in zip(rainfall_calculation['Year'], rainfall_calculation['Month'], rainfall_calculation['Rainfall']):
        if pd.notna(rainfall):
            hovertext.append(f'Year: {year}<br>Month: {month}<br>Rainfall: {rainfall} mm')
        else:
            hovertext.append(f'Year: {year}<br>Month: {month}<br>Rainfall: NaN')
    fig.data[0].hovertext = hovertext

    return fig

# Define the callback function to update station dropdown based on the selected district
@app.callback(
    Output('station-dropdown-weekly-heatmap', 'options'),
    Output('station-dropdown-weekly-heatmap', 'value'),  # Add a second output to set the default value
    [Input('district-dropdown-weekly-heatmap', 'value')]
)
def update_station_options(selected_district):
    # Filter data for the selected district
    filtered_data = data[data['District'] == selected_district]
    # Define station options for the selected district
    station_options = [{'label': station, 'value': station} for station in filtered_data['Station'].unique()]
    default_station = station_options[0]['value']
    return station_options, default_station  # Return both options and default value


# Define the callback function to update the heatmap based on the selected district and station
@app.callback(
    Output('calendar-heatmap-weekly', 'figure'),
    [Input('district-dropdown-weekly-heatmap', 'value'),
     Input('station-dropdown-weekly-heatmap', 'value')]
)
def update_heatmap(selected_district, selected_station):
    # Filter data for the selected district and station
    filtered_data = data[(data['District'] == selected_district) & (data['Station'] == selected_station)]

    # Reshape the data for heatmap
    melted_data = pd.melt(filtered_data, id_vars=['Year'], value_vars=[str(i) for i in range(1, 367)],
                          var_name='Day', value_name='Rainfall')

    # Convert Day column to numeric
    melted_data['Day'] = pd.to_numeric(melted_data['Day'])

    # Calculate the weekly differences of days
    melted_data['Week'] = (melted_data['Day'] - 1) // 7 + 1

    # Calculate the weekly sum of rainfall for each year and week
    weekly_rainfall = melted_data.groupby(['Year', 'Week'], as_index=False)['Rainfall'].sum()

    custom_colorscale = [
        [0, 'rgb(255, 255, 255)'],  # 0 mm (white)
        [0.01, 'rgb(173, 216, 230)'],  # Light blue
        [0.1, 'rgb(135, 206, 235)'],  # Lighter blue
        [0.25, 'rgb(0, 0, 255)'],  # Blue
        [0.5, 'rgb(0, 0, 128)'],  # Dark blue
        [1.0, 'rgb(0, 0, 0)']  # 1 mm and above (black)
    ]
    fig = go.Figure(go.Heatmap(x=weekly_rainfall['Week'], y=weekly_rainfall['Year'], z=weekly_rainfall['Rainfall'],
                               colorscale=custom_colorscale, colorbar_title='Rainfall'))

    fig.update_layout(title=f'Rainfall Weekly Calendar for District: {selected_district}, Station: {selected_station}',
                      xaxis_title='Weeks',
                      yaxis_title='Year',
                      xaxis=dict(nticks=52),
                      yaxis=dict(autorange='reversed'))

    # Create custom hovertemplate with week, year, and rainfall info
    hovertemplate = 'Week: %{x}<br>Year: %{y}<br>Sum of Rainfall: %{z} mm'
    fig.update_traces(hovertemplate=hovertemplate)

    # Update hovertemplate to show "0" for cells with no rainfall and "NaN" for cells where data is not available
    hovertext = []
    for week, year, rainfall in zip(weekly_rainfall['Week'], weekly_rainfall['Year'], weekly_rainfall['Rainfall']):
        hovertext.append(f'Week: {week}<br>Year: {year}<br>Rainfall: {rainfall} mm' if pd.notna(rainfall) else f'Week: {week}<br>Year: {year}<br>Rainfall: NaN')
    fig.data[0].hovertext = hovertext

    return fig




# Define the callback function for the state-wise rainfall graph
@app.callback(
    Output('rainfall-graph-state-wise', 'figure'),
    Input('year-range-slider-climatology', 'value')
)
def update_statewise_rainfall_graph(year_range):
    start_year, end_year = year_range
    filtered_data = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]

    # Calculate the average rainfall for each day across the selected years
    avg_rainfall = filtered_data[rainfall_columns].mean()

    # Create a DataFrame for the bar chart
    df = pd.DataFrame({'Day': [day_to_date(day) for day in avg_rainfall.index],
                       'Average Rainfall': avg_rainfall.values})

    fig = px.bar(df, x='Day', y='Average Rainfall',
                 labels={'Day': 'Day', 'value': 'Rainfall'},
                 title=f'Goa State Climatology from  - {start_year} to {end_year}',
                 color_discrete_sequence=['blue'],
                 height=500)

    # Map day values to day labels for hover information
    day_mapping = {day: day_to_date(day) for day in rainfall_columns}
    fig.update_layout(hovermode='x')

    hovertemplate = '<b>Date:</b> %{x}<br><b>Average Rainfall:</b> %{y:.0f} mm'
    fig.update_traces(hovertemplate=hovertemplate)

    return fig

# Define the callback function for the rainfall trend chart
@app.callback(
    Output('rainfall-trend-state', 'figure'),
    Input('year-range-slider-climatology', 'value')
)
def update_trend_chart(year_range):
    start_year, end_year = year_range
    filtered_data = data[
        (data['Year'] >= start_year) & (data['Year'] <= end_year)]

    fig = go.Figure()

    # Iterate through each station and create a line chart for rainfall trend
    for station in filtered_data['Station'].unique():
        station_data = filtered_data[filtered_data['Station'] == station]
        total_rainfall = station_data[rainfall_columns].sum()

        # Check if there are any 0 values in the total_rainfall data and convert them to NaN
        if 0 in total_rainfall.values:
            total_rainfall = total_rainfall.replace(0, float('nan'))

        fig.add_trace(go.Scatter(x=list(range(1, 367)), y=total_rainfall, mode='lines', name=station,
                                 hovertemplate='Day: %{x}<br>Rainfall: %{y}'))

    fig.update_layout(title=f'Station Rainfall Climatology in Goa from ({start_year} to {end_year})',
                      xaxis_title='Day of the Year',
                      yaxis_title='Total Rainfall',
                      yaxis_tickformat='d',  # Format y-axis tick labels as integers
                      margin=dict(t=50, l=0, r=0, b=30),
                      xaxis=dict(
                          tickvals=list(range(1, 367, 30)),  # Set x-axis tick positions at intervals of 30 days
                          ticktext=[f'Day {i}' for i in range(1, 367, 30)]
                          # Set x-axis tick labels as 'Day 30', 'Day 60', etc.
                      ))

    return fig
@app.callback(
    [Output('district-dropdown-climatology', 'options'),
     Output('district-dropdown-climatology', 'value')],
    [Input('year-range-slider-climatology', 'value')]
)
def update_district_dropdown(year_range):
    start_year, end_year = year_range
    district_options = [{'label': district, 'value': district} for district in data['District'].unique()]
    default_district = district_options[0]['value']  # Get the value of the first district
    return district_options, default_district

@app.callback(
    Output('rainfall-district-bar-graph-climatology', 'figure'),
    [Input('year-range-slider-climatology', 'value'),
     Input('district-dropdown-climatology', 'value')]
)
def update_graph(year_range, district):
    start_year, end_year = year_range
    filtered_data = data[(data['Year'] >= start_year) & (data['Year'] <= end_year) & (data['District'] == district)]

    if not filtered_data.empty:
        # Calculate the y_values_flat and day_labels for the chart
        y_values_flat = filtered_data[rainfall_columns].mean().apply(pd.to_numeric, errors='coerce').tolist()
        day_labels = [day_to_date(day) for day in rainfall_columns]
        chart_data = list(zip([district] * len(day_labels), day_labels, y_values_flat,
                              [filtered_data['Year'].unique()[0]] * len(day_labels)))

        df = pd.DataFrame(chart_data, columns=['District', 'Day', 'Rainfall', 'Year'])

        fig = px.bar(df, x='Day', y='Rainfall',
                     labels={'District': 'District', 'Rainfall': 'Rainfall'},
                     title=f'Rainfall Climatology for {district} - {start_year} to {end_year}',
                     color_continuous_scale='jet',
                     height=500)

        # Customize hovertemplate to format Rainfall values without decimal points
        hovertemplate = '<b>Date:</b> %{customdata[0]}<br><b>Rainfall:</b> %{y:.0f} mm'
        fig.update_traces(hovertemplate=hovertemplate,
                          customdata=df[['Day']].values)

        # Rest of your graph customization here...

        return fig
    else:
        # Return an empty graph if there's no data
        return px.bar()













# Define the callback function for the district trend chart
@app.callback(
    Output('trend-climatology-district', 'figure'),
    [Input('year-range-slider-climatology', 'value'),
     Input('district-dropdown-climatology', 'value')]
)
def update_district_trend_chart(year_range, selected_district):
    start_year, end_year = year_range

    # Filter the data for the selected range of years and district
    filtered_data = data[
        (data['Year'] >= start_year) & (data['Year'] <= end_year) & (data['District'] == selected_district)]

    fig = go.Figure()

    # Iterate through each station and create a line chart for rainfall trend
    for station in filtered_data['Station'].unique():
        station_data = filtered_data[filtered_data['Station'] == station]
        total_rainfall = station_data[rainfall_columns].sum()

        # Check if there are any 0 values in the total_rainfall data and convert them to NaN
        if 0 in total_rainfall.values:
            total_rainfall = total_rainfall.replace(0, float('nan'))

        fig.add_trace(go.Scatter(x=list(range(1, 367)), y=total_rainfall, mode='lines', name=station,
                                 hovertemplate='Day: %{x}<br>Rainfall: %{y}'))

    fig.update_layout(title=f'District-Wise Rainfall Climatology from ({start_year} to {end_year}) in {selected_district}',
                      xaxis_title='Day of the Year',
                      yaxis_title='Total Rainfall',
                      yaxis_tickformat='d',  # Format y-axis tick labels as integers
                      margin=dict(t=50, l=0, r=0, b=30),
                      xaxis=dict(
                          tickvals=list(range(1, 367, 30)),  # Set x-axis tick positions at intervals of 30 days
                          ticktext=[f'Day {i}' for i in range(1, 367, 30)]
                          # Set x-axis tick labels as 'Day 30', 'Day 60', etc.
                      ))

    return fig


# Define the callback function for the station-wise rainfall bar graph
@app.callback(
    Output('rainfall-bar-graph-climatology', 'figure'),
    [Input('year-range-slider-climatology', 'value'),
     Input('station-dropdown-climatology', 'value')]
)
def update_stationwise_rainfall_graph(year_range, station):
    start_year, end_year = year_range
    filtered_data = data[(data['Year'] >= start_year) & (data['Year'] <= end_year) & (data['Station'] == station)]

    if not filtered_data.empty:
        # Calculate the y_values_flat and day_labels for the chart
        y_values_flat = filtered_data[rainfall_columns].mean().apply(pd.to_numeric, errors='coerce').tolist()
        day_labels = [day_to_date(day) for day in rainfall_columns]
        chart_data = list(zip([station] * len(day_labels), day_labels, y_values_flat,
                              [filtered_data['Year'].unique()[0]] * len(day_labels)))

        df = pd.DataFrame(chart_data, columns=['Station', 'Day', 'Rainfall', 'Year'])

        fig = px.bar(df, x='Day', y='Rainfall', color='Station',
                     labels={'Station': 'Station', 'Rainfall': 'Rainfall'},
                     title=f'Rainfall Climatology for {station} - {start_year} to {end_year}',
                     color_continuous_scale='jet',
                     height=500)

        # Update hovertemplate to format Rainfall values as integers
        fig.update_traces(hovertemplate='<br><b>Date:</b> %{customdata[0]}<br><b>Rainfall:</b> %{y:.0f} mm',
                          customdata=df[['Day']].values)

        # Rest of your graph customization here...
        return fig

# Create a callback to update the top events table
@app.callback(
    Output('top-events-table-1', 'data'),
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date')
)
def update_table(start_date, end_date):
    # Convert start_date and end_date to pandas datetime format
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter data based on selected date range
    filtered_data = data_melted[
        (data_melted['Date'] >= start_date) & (data_melted['Date'] <= end_date)
    ]

    # Find the top 5 extreme events for the selected date range
    top_events = filtered_data.sort_values(by='Rainfall', ascending=False).head(5)

    # Convert Rainfall to integers
    top_events['Rainfall'] = top_events['Rainfall'].round().astype(int)

    # Format Date column as "dd/mm"
    top_events['Date'] = top_events['Date'].dt.strftime('%d %b')

    # Convert top events to list of dictionaries for DataTable
    top_events_data = top_events.to_dict('records')

    return top_events_data

# Create a callback to update the top events table
@app.callback(
    Output('top-events-table-2', 'data'),
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date'),
    Input('district-dropdown', 'value')
)
def update_table(start_date, end_date, selected_district):
    # Convert start_date and end_date to pandas datetime format
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter data based on selected date range and district
    filtered_data = data_melted[
        (data_melted['Date'] >= start_date) & (data_melted['Date'] <= end_date) & (data_melted['District'] == selected_district)
    ]

    # Find the top 5 extreme events for the selected date range and district
    top_events = filtered_data.sort_values(by='Rainfall', ascending=False).head(5)

    # Convert Rainfall to integers
    top_events['Rainfall'] = top_events['Rainfall'].round().astype(int)

    # Format Date column as "dd/mm"
    top_events['Date'] = top_events['Date'].dt.strftime('%d %b')

    # Convert top events to list of dictionaries for DataTable
    top_events_data = top_events.to_dict('records')

    return top_events_data

# Create a callback to populate the station dropdown based on the selected district
@app.callback(
    Output('station-dropdown', 'options'),
    Input('district-dropdown-top', 'value')
)
def update_station_dropdown(selected_district):
    station_options = [
        {'label': station, 'value': station}
        for station in data_melted[data_melted['District'] == selected_district]['Station'].unique()
    ]
    return station_options

# Create a callback to update the top events table
@app.callback(
    Output('top-events-table-3', 'data'),
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date'),
    Input('district-dropdown-top', 'value'),
    Input('station-dropdown', 'value')
)
def update_table(start_date, end_date, selected_district, selected_station):
    # Convert start_date and end_date to pandas datetime format
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter data based on selected date range, district, and station
    filtered_data = data_melted[
        (data_melted['Date'] >= start_date) & (data_melted['Date'] <= end_date) &
        (data_melted['District'] == selected_district) & (data_melted['Station'] == selected_station)
    ]

    # Find the top 5 extreme events for the selected date range, district, and station
    top_events = filtered_data.sort_values(by='Rainfall', ascending=False).head(5)

    # Convert Rainfall to integers
    top_events['Rainfall'] = top_events['Rainfall'].round().astype(int)

    # Format Date column as "dd/mm"
    top_events['Date'] = top_events['Date'].dt.strftime('%d %b')

    # Convert top events to list of dictionaries for DataTable
    top_events_data = top_events.to_dict('records')

    return top_events_data


# Step 6: Define the callback function to update the graph
@app.callback(
    dash.dependencies.Output('trend-state-wise', 'figure'),
    [dash.dependencies.Input('trend-state-wise', 'hoverData')]
)
def update_graph(hoverData):
    # Create a scatter plot for the data points
    trace_scatter = go.Scatter(
        x=total_rainfall_per_year['Year'],
        y=total_rainfall_per_year['Total_Rainfall'],
        mode='markers',
        marker=dict(color='green'),
        name='Total Rainfall',
        hovertemplate='Year: %{x}<br>Total Rainfall: %{y:.0f} mm'
    )

    # Create the trendline using a scatter plot
    trendline_data = total_rainfall_per_year.sort_values(by='Year')
    trace_trendline = go.Scatter(
        x=trendline_data['Year'],
        y=trendline_data['Total_Rainfall'],
        mode='lines+markers',
        marker=dict(color='green'),
        line=dict(color='green'),
        name='Total Rainfall',
        hovertemplate='Year: %{x}<br>Total Rainfall: %{y:.0f} mm'
    )

    # Create the regression line using the linear regression model
    X = total_rainfall_per_year['Year'].values.reshape(-1, 1)
    y = total_rainfall_per_year['Total_Rainfall'].values
    regression_model = LinearRegression()
    regression_model.fit(X, y)
    regression_line = regression_model.predict(X)

    trace_regression_line = go.Scatter(
        x=total_rainfall_per_year['Year'],
        y=regression_line,
        mode='lines',
        line=dict(color='red'),
        name='Trendline Line',
        hovertemplate='Year: %{x}<br>Total Rainfall: %{y:.0f} mm'
    )

    # Calculate p-value of the regression model
    y_pred = regression_model.predict(X)
    residuals = y - y_pred
    degrees_of_freedom = len(X) - 2  # Number of observations minus number of predictors
    mse = np.sum(np.square(residuals)) / degrees_of_freedom
    se = np.sqrt(mse / np.sum(np.square(X - np.mean(X))))
    t_stat = np.abs(regression_model.coef_[0] / se)

    # Calculate the p-value using the cumulative distribution function (CDF)
    p_value = 2 * (1 - stats.t.cdf(t_stat, df=degrees_of_freedom))

    significance_level = 0.05
    is_significant = p_value < significance_level

    if is_significant:
        significance_msg = "Significant"
    else:
        significance_msg = "Not Significant"

    p_value_msg = f"P-Value: {p_value:.4f} ({significance_msg})"

    layout = go.Layout(
        title='Total Rainfall per Year with Trendline and Regression Line',
        xaxis=dict(title='Year', type='category', tickmode='array', tickvals=total_rainfall_per_year['Year']),
        yaxis=dict(title='Total Rainfall (mm)', tickformat=','),
        hovermode='closest',
        annotations=[
            dict(
                x=0.5,
                y=1.02,
                xref='paper',
                yref='paper',
                xanchor='center',
                text=p_value_msg,
                showarrow=False,
                font=dict(size=12)
            )
        ]
    )

    return {'data': [trace_scatter, trace_trendline, trace_regression_line], 'layout': layout}

# Step 6: Define the callback function to update the graph
@app.callback(
    dash.dependencies.Output('trend-District-wise-regression', 'figure'),
    [dash.dependencies.Input('district-dropdown-trend-state', 'value')]
)
def update_graph(selected_district):
    if selected_district:
        district_data = data[data['District'] == selected_district]
        title = f"Total Rainfall per Year for {selected_district} District"
    else:
        district_data = data
        title = "Total Rainfall per Year"

    # Calculate total rainfall per year for the selected district or overall
    total_rainfall_per_year = district_data.groupby('Year').sum(numeric_only=True).reset_index()
    total_rainfall_per_year['Total_Rainfall'] = total_rainfall_per_year.iloc[:, 9:].sum(axis=1) / 10

    # Exclude years with 0 total rainfall from the trendline and regression line calculations
    filtered_rainfall_data = total_rainfall_per_year[total_rainfall_per_year['Total_Rainfall'] > 0]

    X = filtered_rainfall_data['Year'].values.reshape(-1, 1)
    y = filtered_rainfall_data['Total_Rainfall'].values

    # Calculate trendline (a line connecting scatter points)
    trace_trendline = go.Scatter(
        x=X.flatten(),
        y=y,
        mode='lines',
        line=dict(color='blue', dash='dash'),
        name='Total Rainfall'
    )

    regression_model = LinearRegression()
    regression_model.fit(X, y)
    regression_line = regression_model.predict(X)

    # Calculate p-value of the regression model
    y_pred = regression_model.predict(X)
    residuals = y - y_pred
    degrees_of_freedom = len(X) - 2  # Number of observations minus number of predictors
    mse = np.sum(np.square(residuals)) / degrees_of_freedom
    se = np.sqrt(mse / np.sum(np.square(X - np.mean(X))))
    t_stat = np.abs(regression_model.coef_[0] / se)

    # Calculate the p-value using the cumulative distribution function (CDF)
    p_value = 2 * (1 - stats.t.cdf(t_stat, df=degrees_of_freedom))

    significance_level = 0.05
    is_significant = p_value >= significance_level

    if is_significant:
        significance_msg = "Regression Line is Significant"
    else:
        significance_msg = "Regression Line is Not Significant"

    p_value_msg = f"P-Value: {p_value:.4f}"

    trace_regression_line = go.Scatter(
        x=X.flatten(),
        y=regression_line,
        mode='lines',
        line=dict(color='red'),
        name='Trendline',
        hovertemplate='Year: %{x}<br>Total Rainfall: %{y:.0f} mm'
    )

    trace_scatter = go.Scatter(
        x=filtered_rainfall_data['Year'],
        y=filtered_rainfall_data['Total_Rainfall'],
        mode='markers',
        name='Total Rainfall',
        hovertemplate='Year: %{x}<br>Total Rainfall: %{y:.0f} mm'
    )

    layout = go.Layout(
        title=title,
        xaxis=dict(title='Year', type='category', tickmode='array', tickvals=filtered_rainfall_data['Year']),
        yaxis=dict(title='Total Rainfall (mm)', tickformat=','),
        hovermode='closest',
        annotations=[
            dict(
                x=0.5,
                y=1.08,
                xref='paper',
                yref='paper',
                xanchor='center',
                text=significance_msg,
                showarrow=False,
                font=dict(size=12)
            ),
            dict(
                x=0.5,
                y=1.02,
                xref='paper',
                yref='paper',
                xanchor='center',
                text=p_value_msg,
                showarrow=False,
                font=dict(size=12)
            )
        ]
    )

    return {'data': [trace_scatter, trace_trendline, trace_regression_line], 'layout': layout}




# Step 6: Define the callback function to update the graph
@app.callback(
    dash.dependencies.Output('rainfall-trend-station', 'figure'),
    [dash.dependencies.Input('station-dropdown-trend', 'value')]
)

def update_graph(selected_station):
    if selected_station:
        station_data = data[data['Station'] == selected_station]
        title = f"Total Rainfall per Year for {selected_station}"
    else:
        station_data = data
        title = "Total Rainfall per Year"

    # Calculate total rainfall per year for the selected station or overall
    total_rainfall_per_year = station_data.groupby('Year').sum(numeric_only=True).reset_index()
    total_rainfall_per_year['Total_Rainfall'] = total_rainfall_per_year.iloc[:, 9:].sum(axis=1) / 10

    # Exclude years with 0 total rainfall from the trendline and regression line calculations
    filtered_rainfall_data = total_rainfall_per_year[total_rainfall_per_year['Total_Rainfall'] > 0]

    X = filtered_rainfall_data['Year'].values.reshape(-1, 1)
    y = filtered_rainfall_data['Total_Rainfall'].values

    # Calculate trendline (a line connecting scatter points)
    trace_trendline = go.Scatter(
        x=X.flatten(),
        y=y,
        mode='lines',
        line=dict(color='Red', dash='dash'),
        name='Total Rainfall'
    )

    regression_model = LinearRegression()
    regression_model.fit(X, y)
    regression_line = regression_model.predict(X)

    # Calculate p-value of the regression model
    y_pred = regression_model.predict(X)
    residuals = y - y_pred
    degrees_of_freedom = len(X) - 2  # Number of observations minus number of predictors
    mse = np.sum(np.square(residuals)) / degrees_of_freedom
    se = np.sqrt(mse / np.sum(np.square(X - np.mean(X))))
    t_stat = np.abs(regression_model.coef_[0] / se)

    # Calculate the p-value using the cumulative distribution function (CDF)
    p_value = 2 * (1 - stats.t.cdf(t_stat, df=degrees_of_freedom))

    significance_level = 0.05
    is_significant = p_value >= significance_level

    if is_significant:
        significance_msg = "Regression Line is Significant"
    else:
        significance_msg = "Regression Line is Not Significant"

    p_value_msg = f"P-Value: {p_value:.4f}"

    trace_regression_line = go.Scatter(
        x=X.flatten(),
        y=regression_line,
        mode='lines',
        line=dict(color='red'),
        name='Trendline',
        hovertemplate='Year: %{x}<br>Total Rainfall: %{y:.0f} mm'
    )

    trace_scatter = go.Scatter(
        x=filtered_rainfall_data['Year'],
        y=filtered_rainfall_data['Total_Rainfall'],
        mode='markers',
        marker=dict(color='green'),
        name='Total Rainfall',
        hovertemplate='Year: %{x}<br>Total Rainfall: %{y:.0f} mm'
    )

    layout = go.Layout(
        title=title,
        xaxis=dict(title='Year', type='category', tickmode='array', tickvals=filtered_rainfall_data['Year']),
        yaxis=dict(title='Total Rainfall (mm)', tickformat=','),
        hovermode='closest',
        annotations=[
            dict(
                x=0.5,
                y=1.08,
                xref='paper',
                yref='paper',
                xanchor='center',
                text=significance_msg,
                showarrow=False,
                font=dict(size=12)
            ),
            dict(
                x=0.5,
                y=1.02,
                xref='paper',
                yref='paper',
                xanchor='center',
                text=p_value_msg,
                showarrow=False,
                font=dict(size=12)
            )
        ]
    )

    return {'data': [trace_scatter, trace_trendline, trace_regression_line], 'layout': layout}


# Define the callback function for the rainfall bar chart
@app.callback(
    Output('histogram-chart', 'figure'),
    [Input('district-dropdown-total', 'value')]
)
def update_bar_chart(selected_district):
    # Filter the data based on the selected district
    filtered_data = data[data['District'] == selected_district]

    # Group data by Year and Station and calculate total rainfall
    grouped_data = filtered_data.groupby(['Year', 'Station'])[rainfall_columns].sum().reset_index()

    # Create the bar chart
    fig = go.Figure()

    for i, station in enumerate(grouped_data['Station'].unique()):
        station_data = grouped_data[grouped_data['Station'] == station]
        fig.add_trace(go.Bar(
            x=station_data['Year'],
            y=station_data[rainfall_columns].sum(axis=1),
            name=station,
            marker_color=color_scale[i % len(color_scale)],
            hovertemplate='Year: %{x}<br>Total Rainfall: %{y} mm',
            customdata=[[station] * len(station_data['Year'])]  # Provide custom data for station name
        ))

    fig.update_layout(title=f'Total Rainfall for Each Station Over Years in {selected_district} District',
                      xaxis_title='Year',
                      yaxis_title='Total Rainfall (mm)',
                      barmode='group',  # Group bars for each year
                      margin=dict(t=50, l=0, r=0, b=30),
                      xaxis_tickangle=-45,  # Rotate x-axis labels for better visibility
                      xaxis_tickmode='linear',  # Ensure linear spacing of x-axis ticks
                      xaxis_dtick=1  # Set the interval between x-axis ticks to 1 year
                      )

    return fig

# Define the callback function
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('year-dropdown-pie', 'value'),
     Input('district-dropdown-total', 'value')]
)
def update_graph(year, district):
    filtered_data = data[(data['Year'] == year) & (data['District'] == district)]
    grouped_data = filtered_data.groupby('Station')[rainfall_columns].sum().reset_index()

    fig = px.pie(grouped_data, names='Station', values=grouped_data[rainfall_columns[1:]].sum(axis=1)
, title=f'Pie-Chart Distribution For  {district} - {year}',
                 height=500)
    # Customize hovertemplate and percent label formatting
    fig.update_traces(hovertemplate='<b>Station:</b> %{label}<br><b>Rainfall:</b> %{value:.0f} mm')
    fig.update_layout(showlegend=False)  # Remove the legend


    return fig

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
