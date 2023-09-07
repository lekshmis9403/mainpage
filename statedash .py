
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import webbrowser  # Import the webbrowser module

app = dash.Dash(__name__)

# Define the list of Indian states and their corresponding URLs
state_urls = {
    'Andhra Pradesh': 'https://example.com/andhra_pradesh',
    'Arunachal Pradesh': 'https://example.com/arunachal_pradesh',
    'Assam': 'https://example.com/assam',
    'Bihar': 'https://example.com/bihar',
    'Chhattisgarh': 'https://example.com/chhattisgarh',
    'Goa': 'https://goadashboard-ynh8.onrender.com/',  # Update with the correct URL for Goa
    'Gujarat': 'https://example.com/gujarat',
    'Haryana': 'https://example.com/haryana',
    'Himachal Pradesh': 'https://example.com/himachal_pradesh',
    'Jharkhand': 'https://example.com/jharkhand',
    'Karnataka': 'https://example.com/karnataka',
    'Kerala': 'https://example.com/kerala',
    'Madhya Pradesh': 'https://example.com/madhya_pradesh',
    'Maharashtra': 'https://example.com/maharashtra',
    'Manipur': 'https://example.com/manipur',
    'Meghalaya': 'https://example.com/meghalaya',
    'Mizoram': 'https://example.com/mizoram',
    'Nagaland': 'https://example.com/nagaland',
    'Odisha': 'https://example.com/odisha',
    'Punjab': 'https://example.com/punjab',
    'Rajasthan': 'https://example.com/rajasthan',
    'Sikkim': 'https://example.com/sikkim',
    'Tamil Nadu': 'https://example.com/tamil_nadu',
    'Telangana': 'https://example.com/telangana',
    'Tripura': 'https://example.com/tripura',
    'Uttarakhand': 'https://example.com/uttarakhand',
    'Uttar Pradesh': 'https://example.com/uttar_pradesh',
    'West Bengal': 'https://example.com/west_bengal',
    # Add URLs for all 28 states here
}

# Define the list of Union Territories and their corresponding URLs
ut_urls = {
    'Andaman and Nicobar Islands': 'https://example.com/andaman_nicobar_islands',
    'Chandigarh': 'https://example.com/chandigarh',
    'Dadra and Nagar Haveli and Daman & Diu': 'https://example.com/dadra_daman',
    'The Government of NCT of Delhi': 'https://example.com/delhi',
    'Jammu & Kashmir': 'https://example.com/jammu_kashmir',
    'Ladakh': 'https://example.com/ladakh',
    'Lakshadweep': 'https://example.com/lakshadweep',
    'Puducherry': 'https://example.com/puducherry',
    # Add URLs for all Union Territories here
}


# Define your logo URL
logo_url = 'https://mausam.imd.gov.in/responsive/img/logo/imd_logo_a.png' 


# app.layout = html.Div([
    
#    html.Div([
#         # Header with logo and title
#         html.Div([
#             html.Img(src=logo_url, style={'width': '70px', 'float': 'left'}),
#             html.Div([
#                 html.H1("Indian Meteorological Department", style={'text-align': 'center', 'font-size': '40px', 'font-weight': 'bold', 'color': 'white'}),
#                 html.P("Government of India", style={'text-align': 'center', 'font-size': '25px', 'color': 'white'}),
#             ], style={'flex': '1', 'text-align': 'center'}),
#         ], style={'display': 'flex', 'align-items': 'center', 'background-color': '#0077B6'}),
#     ]),
#     html.Div([
#         html.H1("Rainfall Data Visualization", style={'text-align': 'center'}),
        
#         # Add your navbar code here
#         html.Nav([
#             dcc.Dropdown(
#                 id='location-dropdown',
#                 options=[
#                     {'label': 'States', 'value': 'states'},
#                     {'label': 'Union Territories', 'value': 'ut'}
#                 ],
#                 placeholder='Select Location Type',
#                 style={'width': '200px', 'margin-right': '20px', 'text-align': 'center'}
#             ),
#             dcc.Dropdown(
#                 id='state-ut-dropdown',
#                 placeholder='Select a State or Union Territory',
#                 style={'width': '300px', 'margin-right': '20px', 'text-align': 'center'}
#             ),
#             html.Button(
#                 'Go',
#                 id='redirect-button',
#                 style={'background-color': 'black', 'color': 'white', 'width': '100px', 'height': '40px', 'font-size': '16px', 'border-radius': '20px'}
#             ),
#         ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
        
#     ], style={'width': '100%', 'height': '90vh', 'background-image': "url('https://i.pinimg.com/736x/37/5e/6e/375e6e01c814dd075c8466313b40d79d.jpg')", 'background-size': 'cover', 'background-position': 'center'}),
#  # Footer
# html.Footer([
#     html.Div([
#         html.Div([
#             html.P("Created by", style={'text-align': 'center'}),
#             html.P("Supriya Biradar", style={'text-align': 'center'}),
#             html.P("Shreya Shaha", style={'text-align': 'center'}),
#         ], style={'flex': '1'}),
        
#         html.Div([
#             html.P("Under guidance of", style={'text-align': 'center'}),
#             html.P("Dr. Rajib Chattopadhyay", style={'text-align': 'center'}),
#             html.P("Lekshmi S", style={'text-align': 'center'}),
#         ], style={'flex': '1'}),
        
#         html.Div([
#             html.P("Follow us on social media:", style={'text-align': 'center'}),
#             html.A(html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Facebook_icon.svg/2048px-Facebook_icon.svg.png', style={'width': '30px', 'margin-right': '10px'}), href='https://www.facebook.com/IMDPune/'),
#             html.A(html.Img(src='https://cdn-icons-png.flaticon.com/512/3670/3670151.png', style={'width': '30px', 'margin-right': '10px'}), href='https://twitter.com/climateimd'),
#             html.A(html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/YouTube_full-color_icon_%282017%29.svg/1024px-YouTube_full-color_icon_%282017%29.svg.png', style={'width': '30px', 'margin-right': '10px'}), href='https://www.youtube.com/channel/UCgBa7vNdcw4q_mjW3TPOfmA/videos'),
#         ], style={'flex': '1'}),
        
#     ], style={'display': 'flex', 'justify-content': 'space-around'}),
# ], style={'background-color': 'black', 'color': 'white', 'padding': '10px', 'text-align': 'center'})

# ], style={'font-family': 'Arial, sans-serif'})


app.layout = html.Div([
    html.Div([
        # Header with logo and title
        html.Div([
            html.Img(src=logo_url, style={'width': '90px',  'margin-left': '50px'}),
            html.Div([
                html.H1("INDIA METEOROLOGICAL DEPARTMENT", style={'text-align': 'center', 'font-size': '30px', 'font-weight': 'bold', 'color': 'white'}),
                html.P("Government of India", style={'text-align': 'center', 'font-size': '25px', 'color': 'white'}),
            ], style={'flex': '1', 'text-align': 'center'}),
        ], style={'display': 'flex', 'align-items': 'center', 'background-color': '#191970'}),
    ]),
    html.Div([
        html.H1("Rainfall Data Visualization", style={'text-align': 'center'}),

        # Add your navbar code here
        html.Nav([
            dcc.Dropdown(
                id='location-dropdown',
                options=[
                    {'label': 'States', 'value': 'states'},
                    {'label': 'Union Territories', 'value': 'ut'}
                ],
                placeholder='Select Location Type',
                style={'width': '200px', 'margin-right': '20px', 'text-align': 'center'}
            ),
            dcc.Dropdown(
                id='state-ut-dropdown',
                placeholder='Select a State or Union Territory',
                style={'width': '300px', 'margin-right': '20px', 'text-align': 'center'}
            ),
            html.Button(
                'Go',
                id='redirect-button',
                style={'background-color': 'black', 'color': 'white', 'width': '100px', 'height': '40px', 'font-size': '16px', 'border-radius': '20px'}
            ),
        ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
     
        # About Section
        html.Div([
            html.Div([
                html.H2("ABOUT", style={'text-align': 'left', 'font-weight': 'bold','font-size': '32px'}),
               html.P(
    "Rainfall Dashboard provides valuable insights into historical rainfall patterns and trends in States of India"
    "This interactive dashboard is a comprehensive tool for both meteorologists and the general public to explore and analyze rainfall data"
    "It offers a visual representation of total rainfall per year, complete with a trendline and regression analysis to identify long-term trends"
    "Users can select specific districts, stations, or date ranges to customize their analysis, making it a valuable resource for researchers, policymakers, and anyone interested in understanding the region's rainfall patterns"
    ,
    style={'text-align': 'left','font-size':'20px'},
),

            ], style={'flex': '1'}),
            html.Div([
                html.Img(src='https://o.remove.bg/downloads/285752b3-8d02-4eeb-b334-1518a207a1db/data-visualization-vector-24713162-removebg-preview.png', style={'width': '100%'}),
                 
            ], style={'flex': '1'}),
        ], style={'display': 'flex', 'width': '100%', 'padding': '20px'}),
    ], style={'width': '100%', 'height': '90vh', 'background-image': "url('https://i.pinimg.com/736x/37/5e/6e/375e6e01c814dd075c8466313b40d79d.jpg')", 'background-size': 'cover', 'background-position': 'center'}),
    
html.Footer([
    html.Div([
        html.Div([
            html.P("Created by", style={'text-align': 'center'}),
            html.P("Supriya Biradar", style={'text-align': 'center'}),
            html.P("Shreya Shaha", style={'text-align': 'center'}),
        ], style={'flex': '1'}),
        
        html.Div([
            html.P("Under guidance of", style={'text-align': 'center'}),
            html.P("Dr. Rajib Chattopadhyay", style={'text-align': 'center'}),
            html.P("Lekshmi S", style={'text-align': 'center'}),
        ], style={'flex': '1'}),
        
         html.Div([
            html.P("Managed By", style={'text-align': 'center'}),
            html.P("Climate Applications and User Interface Group", style={'text-align': 'center'}),
            html.P("CRS IMD,Pune", style={'text-align': 'center'}),
        ], style={'flex': '1'}),

        html.Div([
            html.P("Follow us on social media:", style={'text-align': 'center'}),
            html.A(html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Facebook_icon.svg/2048px-Facebook_icon.svg.png', style={'width': '30px', 'margin-right': '10px'}), href='https://www.facebook.com/IMDPune/'),
            html.A(html.Img(src='https://cdn-icons-png.flaticon.com/512/3670/3670151.png', style={'width': '30px', 'margin-right': '10px'}), href='https://twitter.com/climateimd'),
            html.A(html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/YouTube_full-color_icon_%282017%29.svg/1024px-YouTube_full-color_icon_%282017%29.svg.png', style={'width': '30px', 'margin-right': '10px'}), href='https://www.youtube.com/channel/UCgBa7vNdcw4q_mjW3TPOfmA/videos'),
        ], style={'flex': '1'}),
        
    ], style={'display': 'flex', 'justify-content': 'space-around'}),
], style={'background-color': 'black', 'color': 'white', 'padding': '10px', 'text-align': 'center'})

], style={'font-family': 'Arial, sans-serif'})


@app.callback(
    Output('state-ut-dropdown', 'options'),
    [Input('location-dropdown', 'value')]
)
def update_dropdown(location_type):
    if location_type == 'states':
        return [{'label': state, 'value': state} for state in state_urls.keys()]
    elif location_type == 'ut':
        return [{'label': ut, 'value': ut} for ut in ut_urls.keys()]
    else:
        return []

@app.callback(
    Output('redirect-button', 'n_clicks'),
    [Input('redirect-button', 'n_clicks')],
    [State('state-ut-dropdown', 'value')]
)
def open_external_url(n_clicks, selected_location):
    if n_clicks and selected_location:
        selected_url = state_urls.get(selected_location) if selected_location in state_urls else ut_urls.get(selected_location)
        if selected_url:
            webbrowser.open_new_tab(selected_url)  # Open the URL in a new tab

if __name__ == '__main__':
    app.run_server(debug=True)

