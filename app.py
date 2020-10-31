#Import libs
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.express as px

#The style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '15%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

#The style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '18%',
    'margin-right': '5%',
    'padding' : '10px 5px 15px 20px' 
}

#The style for the text 
TEXT_STYLE = {
    'textAlign': 'left',
    'color': '#191970'
}

#Import local dataframe 
df = pd.read_csv('co-emissions-per-capita.csv')

#Remove rows where country code is not filled and create a new df "df_country"
df_country = df[~df['Code'].isnull()]

#Reset index of the df and drop the old index
df_country.reset_index(drop=True,inplace=True)

#Convert column 'Year' to datetime format as follows : 01-01-XXXX 00:00:00,000000
df['Year'] = pd.to_datetime(df['Year'],format='%Y')

#Draw a plotly choropleth 
fig = px.choropleth(df_country, locations="Code", color="Per capita CO2 emissions", color_continuous_scale='Inferno',range_color=[0,30], animation_frame="Year")

#Define margin for figure layout so the chart can fill as much space as possible
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

#Define dims for layout
fig.layout.width=800
fig.layout.height=500

#Set orientation of the modebar 
fig.layout.modebar.orientation='h'

#Set the colorbar to the left side of the cart
fig.layout.coloraxis.colorbar.x = -0.1
fig.layout.coloraxis.colorbar.xanchor = 'left'

#Set the position of updatemenus (play and stop buttons) 
#One above the other (direction = 'up')
fig.layout.updatemenus[0]['pad']={'t':-0.3}
fig.layout.updatemenus[0].direction = 'up'
fig.layout.updatemenus[0].x = -0.1
fig.layout.updatemenus[0].xanchor = 'left'

#Set the slider near the chart 
fig.layout.sliders[0]['pad']={'t':-0.3}
fig.layout.sliders[0]['len']= 1
fig.layout.sliders[0].x = 0

#sidebar components, contains all the link of the
#different paragraphs 
controls = dbc.FormGroup(
    [
        html.A('Worldwide temperatures',href='#card_title_1', style={
            'textAlign': 'center'
        }),
        html.Br(),
       html.A('Worldwide greenhouse gas emissions ',href='#card_title_1', style={
            'textAlign': 'center'
        }),
        html.Br(),
       html.A('Effect of global warming',href='#card_title_1', style={
            'textAlign': 'center'
        }),
         html.Br(),
       html.A('Predictions',href='#card_title_1', style={
            'textAlign': 'center'
        }),      
    ]
)

#Create the sidebar
sidebar = html.Div( 
    [
        html.H2('Sommaire', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)

#row 0 content
content_zero_row = dbc.Row(
    [
        html.H4('Worldwide temperature',style=TEXT_STYLE),
    ]
)

#row 1 content
content_first_row = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_2',
            config = {
            'modeBarButtonsToAdd' : ['drawline', 'drawopenpath', 'drawrect', 'eraseshape'],
            'displayModeBar'         : True
                    },
            figure = fig
            )],md=7),
        dbc.Col(
            dbc.Textarea(
            id='textarea-example',
            value='Textarea content initialized\nwith multiple lines of text',
            style={ 'width': '100%', 'min-height': '400px',
                'box-sizing': 'border-box', 'border': 'none'},
            ),md=5,
        ),  
    ]
)

#row 2 content
content_second_row = dbc.Row(
    [
    ]
)

#row 3 content
content_third_row = dbc.Row(
    [
    ]
)

#Main content
content = html.Div(
    [
        html.H3('A data centered view on Global Warming', style=TEXT_STYLE),
        "by Valérie Didier, Esperence Moussa, Colin Verhille, Christophe Duruisseau",
        html.Hr(),
        content_zero_row,
        content_first_row,
        content_second_row,
        content_third_row,
    ],
    style=CONTENT_STYLE
)

#use bootstrap stylesheet
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
#define page layout, which contains sidebar and content
app.layout = html.Div([sidebar, content])

#Run the server at port 8085
#Accessible through : http://localhost:8085
if __name__ == '__main__':
    app.run_server(port='8085')
