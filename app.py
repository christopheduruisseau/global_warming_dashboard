#Import libs
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

#Style definition 
#region
#Apply custom format to map figures
def formatMap(fignb):
    #Define margin for figure layout so the chart can fill as much space as possible
    fignb.update_layout(margin=dict(l=0, r=0, t=0, b=0))

    #Define dims for layout
    fignb.layout.width=800
    fignb.layout.height=500

    #Set orientation of the modebar 
    fignb.layout.modebar.orientation='h'

    #Set the colorbar to the left side of the cart
    #fignb.layout.coloraxis.colorbar.len = 0.8
    fignb.layout.coloraxis.colorbar.x = -0.2
    fignb.layout.coloraxis.colorbar.xanchor = 'left'

    #Set the position of updatemenus (play and stop buttons) 
    #One above the other (direction = 'up')
    #Last config allow to set the duration of animation
    fignb.layout.updatemenus[0]['pad']={'t':-0.4}
    #fignb.layout.updatemenus[0].direction = 'up'
    fignb.layout.updatemenus[0].x = -0.18
    fignb.layout.updatemenus[0].xanchor = 'left'
    fignb.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 5

    #Set the slider near the chart 
    #fignb.layout.sliders[0]['pad']={'t':-0.3}
    fignb.layout.sliders[0]['pad']={'t':-0.2}
    fignb.layout.sliders[0]['y'] = 0.08
    fignb.layout.sliders[0]['len']= 1
    fignb.layout.sliders[0].x = 0

#Apply custom format to scatter figures
def formatScatter(fignb):
     #Define margin for figure layout so the chart can fill as much space as possible
    fignb.update_layout(margin=dict(l=0, r=0, t=0, b=0),legend=dict(yanchor="top",y=0.99, xanchor="left",x=0.01))
    #Define dims for layout
    fignb.layout.width=800
    fignb.layout.height=500

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
#endregion

#Dataframes
#region
#Import local dataframe 
ultimate_df = pd.read_csv('ultimate_df.csv')
#New df which is part of ultimate_df
world_df = ultimate_df.loc[ultimate_df['Country'] == 'World']


# Slicing the df to remove the World value:
df_count = ultimate_df[~(ultimate_df['Country'] == 'World')]
# Creating list & dictionary to iterate over for value names and colors:
GHG_list = ['Annual CO2 emissions', 'Methane', 'Nitrous_oxide', 'Total GHG']
GHG_name = ['Carbone Dioxyde', 'Methane', 'Nitrous Oxyde', 'Total Greenhouse Gas']
GHG_color = [px.colors.sequential.Blues, px.colors.sequential.Greens, px.colors.sequential.Oranges, px.colors.sequential.Reds]
GHG_name_dict = dict(zip(GHG_list, GHG_name))
GHG_color_dict = dict(zip(GHG_list, GHG_color))

# Code for the correlation plots between temperature variation and Greenhouse Gas Emissions:
# Slicing the df to avoid Nan values
world_1990_df = world_df[world_df['Year']>1989]

# Setting a dictionnary for the colors:
GHG_disc_color = ['rgb(107,174,214)', 'rgb(116,196,118)', 'rgb(253,141,60)', 'rgb(165,15,21)']
GHG_disc_color_dict = dict(zip(GHG_list, GHG_disc_color))
#endregion

#Figure 1
#region
# Code for the Figure:
fig1 = go.Figure()
#Add a line on the scatterplot
fig1.add_trace(go.Scatter(x=world_df.Year, y=np.zeros(len(world_df.Year)),
                    mode='lines',
                    name='1961- 1990 mean',
                    line=dict(color="#000000")))
#Draw the scatterplot 
fig1.add_trace(go.Scatter(x=world_df.Year, y=world_df.temperature_variations,
                    mode='markers',
                    name='Global temperature (rolling mean)',
                    marker={'color':world_df.temperature_variations, 'colorscale':px.colors.cyclical.IceFire, 'size':13, 'cmid':0, 'cmin':-2, 'cmax':2},
                    hovertemplate="Year : %{x}<br>Variation : %{y}"))
#Set legend
fig1.update_layout(xaxis_title='Years',
                   yaxis_title='Temperature (degrees C)', 
                   plot_bgcolor='rgba(0,0,0,0.05)',
                   legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                    ))

#format it
formatScatter(fig1)
#change yaxe range
fig1.update_yaxes(range=[-1, 1])

#endregion

#Figure 2
#region
#Create new mapplot
fig2 = px.choropleth(ultimate_df, 
                    locations="Code", 
                    color="temperature_variations", 
                    hover_name="Country", 
                    color_continuous_scale=px.colors.cyclical.IceFire, 
                    color_continuous_midpoint=0, 
                    animation_frame="Year", 
                    range_color=[-2,2], 
                    title='Worldwide temperatures variations'
                    )
#format it                   
fig2.update_layout(margin={'r':0, 't':30, 'l':0, 'b':0}, coloraxis_colorbar=dict(title="Temperature Variation"))
formatMap(fig2)
#endregion


#sidebar components, contains all the link of the
#different paragraphs 
controls = dbc.FormGroup(
    [
        html.Ul(className="list-unstyled", children=
        [
            html.Li(
                html.A('Part 1 : Global Warming',href='', style={'textAlign': 'center','text-decoration': 'underline','color': '#191970'}),
            ),
            html.Li(
                html.A('Figure 1 : Global temperature variation from 1850 to 2015',href='',style={'font-size':'11px','color': '#191970'}),
            ),
            html.Li(
                html.A('Figure 2. Worldwide temperature variations by country from 1850 to 2015.',href='',style={'font-size':'11px','color': '#191970'}),
            ),
            html.Br(),
            html.Li(
                html.A('Part 2: Impact of humans’ activities on global warming (Greenhouse Gas Emissions, Solar radiations) ',href='', style={'textAlign': 'center','text-decoration': 'underline','color': '#191970'}),
            ),
            html.Li(
                html.A('Figure 4. Solar radiations vs. global temperature.',href='', style={'font-size':'11px','color': '#191970'})
            ),
            html.Li(
                html.A('Figure 5. Global greenhouse gas emissions over time (CO2, CH4, N2O).',href='', style={'font-size':'11px','color': '#191970'})
            ),
            html.Li(
                html.A('Figure 6. Greenhouse gas emissions by country.',href='', style={'font-size':'11px','color': '#191970'})
            ),
            html.Li(
                html.A('Figure 7. Correlation between greenhouse gas emissions and temperature evolution.',href='', style={'font-size':'11px','color': '#191970'})
            ),
            html.Li(
                html.A('Figure 8. CO2 emissions during COVID period',href='', style={'font-size':'11px','color': '#191970'})
            ),
            html.Br(),
            html.Li(
                html.A('Part 3: Impact of Global Warming on Life on Earth',href='', style={'textAlign': 'center','text-decoration': 'underline','color': '#191970'}),
            ),
            html.Li(
                html.A('Figure 9. Make me melt',href='', style={'font-size':'11px','color': '#191970'})
            ),
            html.Li(
                html.A('Figure 10. Impact on biodiversity (protected area)',href='', style={'font-size':'11px','color': '#191970'})
            ),
            html.Br(),
             html.Li(
                html.A('Part 4: Projections: Forecasting the evolution of variables in play in the years to come ',href='', style={'textAlign': 'center','text-decoration': 'underline','color': '#191970'}),
            ),
             html.Li(
                html.A('Figure 11. Projected temperature evolution',href='', style={'font-size':'11px','color': '#191970'})
            )
        ]
        ),
    ]
)

#Create the sidebar
sidebar = html.Div( 
    [
        html.H2('Index', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)

#Main content 
#region
#row 0 content : part title 
content_row_0 = dbc.Row(align="center",justify="center",children=
    [
        dbc.Col(width="auto", children=[
            html.H2('Is global warming a myth ?')
        ] 
        )
    ]
)

#row intro wordlwide temperature 
intro_worldwide_temperature = dbc.Row([
    html.H4('Worldwide temperature'),
    html.Div()]
)

#row 1 content : txtarea (should be modified at the end)
content_row_1 = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='fig1',
            config = {
            'displayModeBar'         : True
                    },
            figure = fig1
            )],md=7),
        dbc.Col(
            html.Div()
        ),  
    ]
)

#row 2 content : fig2 
content_row_2 = dbc.Row(
    [
      dbc.Col(align='left',children=[
            dcc.Graph(id='fig2',
            config = {
            'modeBarButtonsToAdd' : ['drawline', 'drawopenpath', 'drawrect', 'eraseshape'],
            'displayModeBar'         : True
                    },
            figure = fig2
            )],md=7)
            
    ]
)

#row 3 content : fig 6
content_row_3 = dbc.Row(
         dcc.Graph(id='fig6',
            config = {
            'modeBarButtonsToAdd' : ['drawline', 'drawopenpath', 'drawrect', 'eraseshape'],
            'displayModeBar'         : True
                    })
)

#row 4 content : radio button for fig6
content_row_4 = dbc.Row(
   dcc.RadioItems(inputStyle={"margin-right": "10px","margin-left":"20px"},
                id='crossfilter-yaxis-column',
                options=[{'label': j, 'value': i} for i,j in GHG_name_dict.items()],
                value='Methane',
            ) 
)

#row 5 content : fig7
content_row_5 = dbc.Row(
         dcc.Graph(id='fig7',
            config = {
            'modeBarButtonsToAdd' : ['drawline', 'drawopenpath', 'drawrect', 'eraseshape'],
            'displayModeBar'         : True
                    })
)

#row 6 content : radio buttons for fig7
content_row_6 = dbc.Row(
   dcc.RadioItems(inputStyle={"margin-right": "10px","margin-left":"20px"},
                id='crossfilter-yaxis-column2',
                options=[{'label': j, 'value': i} for i,j in GHG_name_dict.items()],
                value='Methane',
            ) 
)

#Main content
content = html.Div(
    [
        html.H1('A data centered view on Global Warming', style=TEXT_STYLE),
        "by Valérie Didier, Esperence Moussa, Colin Verhille, Christophe Duruisseau",
        html.Br(),
        html.Br(),
        html.Div(),
        html.Hr(),
        content_row_0,
        html.Hr(),
        intro_worldwide_temperature,
        html.Br(),
        html.Br(),
        content_row_1,
        content_row_2,
        content_row_4,
        content_row_3,
        content_row_5,
        content_row_6
    ],
    style=CONTENT_STYLE
)

#endregion

#use bootstrap stylesheet
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
#define page layout, which contains sidebar and content
app.layout = html.Div([sidebar, content])

#Callbacks
#region

#Callback for fig6
@app.callback(
    Output('fig6', 'figure'),
    [Input('crossfilter-yaxis-column', 'value')])
def update_graph(col_value):
  fig6 = px.choropleth(df_count, 
                    locations="Code", 
                    color=col_value, 
                    hover_name="Country", 
                    color_continuous_scale=GHG_color_dict[col_value],
                    animation_frame="Year", 
                    range_color=[df_count[col_value].min(),df_count[col_value].max()], 
                    title=f'Worldwide {GHG_name_dict[col_value]} emissions'
                    )
  fig6.update_layout(margin={'r':0, 't':30, 'l':0, 'b':0}, coloraxis_colorbar=dict(title=f"{GHG_name_dict[col_value]} emissions"))
  formatMap(fig6)
  return fig6

#Callback for fig7
@app.callback(
    Output('fig7', 'figure'),
    [Input('crossfilter-yaxis-column2', 'value')])
def update_graph1(col_value):
  fig7 = px.scatter(world_1990_df, x=col_value, y='temperature_variations', trendline='ols')
  fig7.update_traces(marker={'color':GHG_disc_color_dict[col_value], 'size':7})
  fig7.update_layout(title=f'Correlation between Temperature variation and {GHG_name_dict[col_value]} emissions',
                   xaxis_title=f'{GHG_name_dict[col_value]} emissions (tonnes)',
                   yaxis_title='Temperature Variation (degrees C)', 
                    plot_bgcolor='rgba(0,0,0,0.05)')
  return fig7

#endregion

#Run the server at port 8085
#Accessible through : http://localhost:8085
if __name__ == '__main__':
    app.run_server(port='8085')
