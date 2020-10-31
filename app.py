import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.express as px

# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '15%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '18%',
    'margin-right': '5%',
    'padding' : '10px 5px 15px 20px' 
}

TEXT_STYLE = {
    'textAlign': 'left',
    'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

df = pd.read_csv('co-emissions-per-capita.csv')
df_country = df[~df['Code'].isnull()]
df_country.reset_index(drop=True,inplace=True)
df['Year'] = pd.to_datetime(df['Year'],format='%Y')
fig = px.choropleth(df_country, locations="Code", color="Per capita CO2 emissions", color_continuous_scale='Inferno',range_color=[0,30], animation_frame="Year")
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
fig.layout.width=800
fig.layout.height=500

fig.layout.modebar.orientation='h'

fig.layout.coloraxis.colorbar.x = -0.1
fig.layout.coloraxis.colorbar.xanchor = 'left'

fig.layout.updatemenus[0]['pad']={'t':-0.3}
fig.layout.updatemenus[0].direction = 'up'
fig.layout.updatemenus[0].x = -0.1
fig.layout.updatemenus[0].xanchor = 'left'

fig.layout.sliders[0]['pad']={'t':-0.3}
fig.layout.sliders[0]['len']= 1
fig.layout.sliders[0].x = 0

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

sidebar = html.Div( 
    [
        html.H2('Sommaire', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)

content_zero_row = dbc.Row(
    [
        html.H4('Worldwide temperature',style=TEXT_STYLE),
    ]
)

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

content_second_row = dbc.Row(
    [
    ]
)

content_third_row = dbc.Row(
    [
    ]
)

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

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([sidebar, content])


@app.callback(
    Output('graph_1', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)
    fig = {
        'data': [{
            'x': [1, 2, 3],
            'y': [3, 4, 5]
        }]
    }
    return fig


@app.callback(
    Output('graph_2', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_2(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)
    fig = px.choropleth(df_country, locations="Code", color="Per capita CO2 emissions", color_continuous_scale='Inferno',range_color=[0,30], animation_frame="Year",title='Per capita CO2 emissions')
    return fig


@app.callback(
    Output('graph_3', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_3(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)
    df = px.data.iris()
    fig = px.density_contour(df, x='sepal_width', y='sepal_length')
    return fig


@app.callback(
    Output('graph_4', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_4(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)  # Sample data and figure
    df = px.data.gapminder().query('year==2007')
    fig = px.scatter_geo(df, locations='iso_alpha', color='continent',
                         hover_name='country', size='pop', projection='natural earth')
    fig.update_layout({
        'height': 600
    })
    return fig


@app.callback(
    Output('graph_5', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_5(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)  # Sample data and figure
    df = px.data.iris()
    fig = px.scatter(df, x='sepal_width', y='sepal_length')
    return fig


@app.callback(
    Output('graph_6', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_6(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)  # Sample data and figure
    df = px.data.tips()
    fig = px.bar(df, x='total_bill', y='day', orientation='h')
    return fig


if __name__ == '__main__':
    app.run_server(port='8085')
