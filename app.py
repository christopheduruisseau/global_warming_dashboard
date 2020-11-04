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
from plotly.subplots import make_subplots
from text_content import * 

#region style definition
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

# Getting the color specifications and intervals for the different GHG:
rangecolor_co2 = getColorPal('YlOrRd', 0, 9)
rangecolor_ghg = getColorPal('YlOrBr', 1, 8)
rangecolor_meth = getColorPal('Reds', 1, 6)
rangecolor_no = getColorPal('OrRd', 2, 5)

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

#region dataframes

#Import ultimate_df dataframe 
ultimate_df = pd.read_csv('ultimate_df.csv')
#Import paleo_df dataframe
paleo_df=pd.read_csv('paleodf.csv',parse_dates=True)
#Import covid_df
Covid_df = pd.read_csv('confinementC02variation.csv')
Covid_df['CO2_variation'] = Covid_df['CO2_variation'].apply(lambda x : x.replace('%','')) 
Covid_df['CO2_variation'] = Covid_df['CO2_variation'].apply(lambda x : x.replace(',','.')) 
Covid_df['CO2_variation'] = Covid_df['CO2_variation'].astype('float64')
#Import Predicted Future Temperatures:
predictions_df = pd.read_csv('Future_temperature_predictions.csv')

#endregion

#region figure definitions except for those with callbacks  

#region figure 1
# Slicing the df to select only the World values:
world_df = ultimate_df.loc[ultimate_df['Country'] == 'World']

# Code for the Figure:
fig1 = go.Figure()

fig1.add_trace(go.Scatter(x=world_df.Year, y=np.zeros(len(world_df.Year)),
                    mode='lines',
                    name='1961- 1990 mean',
                    line=dict(color="#000000")))
fig1.add_trace(go.Scatter(x=world_df.Year, y=world_df.temperature_variations,
                    mode='markers',
                    name='Global temperature (rolling mean)',
                    marker={'color':world_df.temperature_variations, 'colorscale':px.colors.cyclical.IceFire, 'size':13, 'cmid':0, 'cmin':-2, 'cmax':2},
                    hovertemplate="Year : %{x}<br>Variation : %{y}"))
fig1.update_layout(#title='Global temperature : Deviation from the mean',
                   xaxis_title='Years',
                   yaxis_title='Temperature (degrees C)', 
                   plot_bgcolor='rgba(0,0,0,0.05)',
                   )
fig1.update_yaxes(range=[-1, 1])

formatScatter(fig1)
#endregion

#region figure 2
# Generating the chloropleth Worldwide Map for Temperature variations by Year and By Country
fig2 = px.choropleth(ultimate_df[ultimate_df['Year']<2014], 
                    locations="Code", 
                    color="temperature_variations", 
                    hover_name="Country", 
                    color_continuous_scale=px.colors.cyclical.IceFire, 
                    color_continuous_midpoint=0, 
                    animation_frame="Year", 
                    range_color=[-2,2] 
                    #title='Worldwide temperatures variations'
                    )
fig2.update_layout(margin={'r':0, 't':30, 'l':0, 'b':0}, coloraxis_colorbar=dict(title="Temperature Variation"))

formatMap(fig2)
#endregion 

#region figure 3a
# Plotting Global temperature from -21ka to 1850:
fig3a = go.Figure()

fig3a.add_trace(go.Scatter(x=paleo_df.End, y=paleo_df.Temperature,
                    mode='markers',
                    #name='Global land temperature (TraCE-21ka simulation)',
                    marker={'color':paleo_df.Temperature, 'colorscale':px.colors.cyclical.IceFire, 'size':13, 'cmid':0, 'cmin':-2, 'cmax':10},
                    hovertemplate="Year : %{x}<br>Temp : %{y}"))
fig3a.update_layout(#title='Global temperature since -19 000 (TraCE-21ka simulation)',
                   xaxis_title='Years',
                   yaxis_title='Temperature (degrees C)', 
                   plot_bgcolor='rgba(0,0,0,0.05)',
                   )
formatScatter(fig3a)
#endregion

#region figure 3b
# Plotting temperature variations from 0 to nowdays:
df_recent = paleo_df[paleo_df.Start>0]

#pour utiliser les variations de l'utimate df, je calcule la valeur du premier point : la dernière valeur de df paleo - la premieère variation contemporaine
premierpoint=df_recent.loc[df_recent.index.max(), "Temperature"]-world_df.loc[world_df.index.min(), "temperature_variations"]
premierpoint

fig3b = go.Figure()



fig3b.add_trace(go.Scatter(x=df_recent.End, y=df_recent.Temperature,
                    mode='markers',
                    name='Global land temperature (TraCE-21ka simulation)',
                    marker={'color':"grey"},
                    hovertemplate="Year : %{x}<br>Temp : %{y}"))

fig3b.add_trace(go.Scatter(x=world_df.Year, y=world_df.temperature_variations+premierpoint,
                    mode='markers',
                    name='Global land temperature (Berkeley Earth)',
                    marker={'color':"red", 'cmid':8, 'cmin':6, 'cmax':10},
                    hovertemplate="Year : %{x}<br>Temp : %{y}"))

fig3b.update_layout(#title='Global temperature since JC',
                   xaxis_title='Years',
                   yaxis_title='Temperature (degrees C)', 
                   plot_bgcolor='rgba(0,0,0,0.05)',
                   )

formatScatter(fig3b)
#endregion

#region figure 4
df_solar = ultimate_df[ultimate_df["Code"]=="OWID_WRL"][["Year", "temperature_values", "temperature_variations", "Solar_irradiation"]]

#je crée une colonne de variation de l'activité solaire, et je la calcule par rapport à la période de référence 1960-1991, comme pour les températures, en lissant la moyenne sur 10ans
df_solar["solar_variation"]=0
solar_mean=df_solar[df_solar.Year.between(1961,1990)]["Solar_irradiation"].mean()
for i in range(len(df_solar.Solar_irradiation)):
  df_solar.loc[i, "solar_variation"]=df_solar.loc[i, "Solar_irradiation"]-solar_mean

df_solar.solar_variation=df_solar.solar_variation.rolling(10).mean()

#Go pour le graphique
fig4 = make_subplots(specs=[[{"secondary_y": True}]])

fig4.add_trace(go.Scatter(x=df_solar.Year, y=df_solar.temperature_variations,
                    mode='markers',
                    name='Global temperature variation (rolling mean)',
                    marker={'color':df_solar.temperature_variations, 'colorscale':px.colors.cyclical.IceFire, 'size':13, 'cmid':0, 'cmin':-2, 'cmax':2}
                    ),secondary_y=False)
fig4.add_trace(go.Scatter(x=df_solar.Year, y=df_solar["solar_variation"],
                    mode='markers',
                    name='Solar irradiation variation (rolling mean)',
                    marker={'color':'rgb(166,54,3)', 'colorscale':px.colors.sequential.Oranges, 'size':7, 'cmid':0, 'cmin':-1, 'cmax':0.5}
                    ),secondary_y=True)

fig4.update_layout(#title='Temperature variations compared to solar activity variation (deviation from period 1961-1990)',
                   xaxis_title='Years',
                   yaxis_title='Temperature (degrees C)', 
                    plot_bgcolor='rgba(0,0,0,0.05)')
fig4.update_yaxes(title_text="Temperature (degrees C)", secondary_y=False)
fig4.update_yaxes(title_text="Solar irradiation (W/m2)", secondary_y=True)
fig4.update_yaxes(range=[-1, 1])
formatScatter(fig4)
#endregion

#region figure 5
# Line plot for global greenhouse gas emissions (using world_df)
world_1990_df = world_df[world_df['Year']>1989]

fig5 = go.Figure()
fig5.add_trace(go.Scatter(
    x=world_1990_df['Year'], y=world_1990_df['Annual CO2 emissions'],
    mode='lines',
    name='Carbon Dioxide',
    text='Carbon Dioxide',
    #hoverinfo='text+Year+Annual CO2 emissions',
    line=dict(color='rgb(252,78,42)'),
    stackgroup='one'
))
fig5.add_trace(go.Scatter(
    x=world_1990_df['Year'], y=world_1990_df['Methane'],
    mode='lines',
    name='Methane',
    text='Methane',
    line=dict(color='rgb(165,15,21)'),
    stackgroup='one'
))
fig5.add_trace(go.Scatter(
    x=world_1990_df['Year'], y=world_1990_df['Nitrous_oxide'],
    mode='lines',
    name='Nitrous Oxide',
    text='Nitrous Oxide',
    line=dict(color='rgb(127,0,0)'),
    stackgroup='one'
))
fig5.update_layout(title='Global Greenhouse Gas Emissions',
                   xaxis_title='Years',
                   yaxis_title='Greenhouse gas emissions (tonnes of CO2 equivalent)', 
                    plot_bgcolor='rgba(0,0,0,0.05)')
formatScatter(fig5)
#endregion

#region figure 6
# Slicing the df to remove the World value:
df_count = ultimate_df[~(ultimate_df['Country'] == 'World')]
df_count_1990 = df_count[df_count['Year']>1989]

# Creating list & dictionary to iterate over for value names and colors:
GHG_name = ['Carbone Dioxide', 'Methane', 'Nitrous Oxide', 'Total Greenhouse Gas']
GHG_color = [rangecolor_co2, rangecolor_meth, rangecolor_no, rangecolor_ghg]
GHG_cat_list = ['C02_cat', 'methane_cat', 'n_oxide_cat', 'GHG_cat']
GHG_label_list = ['C02_lbl', 'methane_lbl', 'n_oxide_lbl', 'GHG_lbl']

GHG_color_dict = dict(zip(GHG_cat_list, GHG_color))#
GHG_cat_name_dict = dict(zip(GHG_cat_list, GHG_name))
GHG_label_dict = dict(zip(GHG_cat_list, GHG_label_list))

#endregion

#region figure 7 
# Code for the correlation plots between temperature variation and Greenhouse Gas Emission for Dash

# Setting a dictionnary for the colors:
GHG_disc_color = ['rgb(252,78,42)', 'rgb(165,15,21)', 'rgb(127,0,0)', 'rgb(204,76,2)']
GHG_list = ['Annual CO2 emissions', 'Methane', 'Nitrous_oxide', 'Total GHG']
GHG_disc_color_dict = dict(zip(GHG_list, GHG_disc_color))
GHG_name_dict = dict(zip(GHG_list, GHG_name))
#endregion

#region figure 8
fig8 = px.choropleth(Covid_df, locations="Code", color="CO2_variation", range_color=[-20.0,0.0], 
                    color_continuous_scale=px.colors.sequential.YlOrRd, animation_frame="DATE")
fig8.update_layout(margin={'r':0, 't':30, 'l':0, 'b':0}, coloraxis_colorbar=dict(title="CO2 Variation (%)"))

formatMap(fig8)
#endregion

#region figure 9a
# Plotting Glaciers mass variations:
world_1966_2001_df = world_df.loc[(world_df['Year']>1966) & (world_df['Year']<2001)]

fig9a = make_subplots(specs=[[{"secondary_y": True}]])

fig9a.add_trace(go.Scatter(x=world_1966_2001_df.Year, y=world_1966_2001_df.Glacier_mass_value,
                    mode='markers',
                    marker={'color':world_1966_2001_df.Glacier_mass_value, 'colorscale':px.colors.sequential.Blues, 'size':13, 'cmid':0, 'cmin':-400000, 'cmax':0}
                    ),secondary_y=False)

fig9a.update_layout(#title='Variation of glaciers mass',
                   xaxis_title='Years',
                   plot_bgcolor='rgba(0,0,0,0.05)')
fig9a.update_yaxes(title_text="Glaciers mass variation (compared to 1966)", secondary_y=False)

formatScatter(fig9a)
#endregion

#region figure 9b
# Slicing the df to select only the World values:
world_1900_df = world_df[world_df['Year']>1900]

# Plotting sea leval variations:
fig9b = make_subplots(specs=[[{"secondary_y": True}]])

fig9b.add_trace(go.Scatter(x=world_1900_df.Year, y=world_1900_df.Sea_level,
                    mode='markers',
                    marker={'color':world_1900_df.Sea_level, 'colorscale':px.colors.sequential.Blues, 'size':13, 'cmid':0, 'cmin':-200, 'cmax':100}
                    ),secondary_y=False)

fig9b.update_layout(title='Variation of sea-level',
                   xaxis_title='Years',
                   plot_bgcolor='rgba(0,0,0,0.05)')
fig9b.update_yaxes(title_text="Global sea_level variation (cm, compared to 1990)", secondary_y=False)

formatScatter(fig9b)
#endregion

#region figure 10
# Slicing the df to avoid Nan values
df_count_2000 = df_count[df_count['Year']>1999]

# Cloropeth map using values from the biodiversity column
fig10 = px.choropleth(df_count_2000, 
                    locations="Code", 
                    color="biodiversity", 
                    hover_name="Country", 
                    color_continuous_scale=px.colors.sequential.Greens, 
                    animation_frame="Year", 
                    range_color=[0,100] 
                    #title='Worldwide biodiversity evolution'
                    )
fig10.update_layout(margin={'r':0, 't':30, 'l':0, 'b':0}, coloraxis_colorbar=dict(title="Temperature Variation"))
formatMap(fig10)
#endregion

#region figure 11
fig11 = go.Figure()

fig11.add_trace(go.Scatter(x=world_df['Year'], y=world_df['temperature_variations'],
                    mode='markers',
                    name='Past Temperature Variation',
                    marker={'color':'grey',
                            'size':7, 'cmid':0, 'cmin':-1, 'cmax':0.5}
                    ))
fig11.add_trace(go.Scatter(x=predictions_df.Year, y=predictions_df.temp_mod1,
                    mode='markers',
                    marker={'color':'#820000'},
                    name='Predictive Model 1'))
fig11.add_trace(go.Scatter(x=predictions_df.Year, y=predictions_df.temp_mod2,
                    mode='markers',
                    marker={'color':'#da8200'},
                    name='Predictive Model 2'))
fig11.add_trace(go.Scatter(x=predictions_df.Year, y=predictions_df.temp_mod3,
                    mode='markers',
                    marker={'color':'#e7b000'},
                    name='Predictive Model 3'))
fig11.add_trace(go.Scatter(x=predictions_df.Year, y=predictions_df.temp_mod4,
                    mode='markers',
                    marker={'color':'#30a4ca'},
                    name='Predictive Model 4'))
formatScatter(fig11)
#endregion

#endregion

#region sidebar
#sidebar components, contains all the link of the
#different paragraphs 
controls = dbc.FormGroup(
    [
        html.Ul(className="list-unstyled", children=
        [
            html.Li(
                html.A('Part 1 - Global Warming',href='', style={'textAlign': 'center','text-decoration': 'underline','color': '#191970'}),
            ),
            html.Li(
                html.A('Figure 1 : Global temperature variation from 1850 to 2015',href='',style={'font-size':'11px','color': '#191970'}),
            ),
            html.Li(
                html.A('Figure 2. Worldwide temperature variations by country from 1850 to 2015.',href='',style={'font-size':'11px','color': '#191970'}),
            ),
            html.Br(),
            html.Li(
                html.A('Part 2 - Impact of humans’ activities on global warming (Greenhouse Gas Emissions, Solar radiations) ',href='', style={'textAlign': 'center','text-decoration': 'underline','color': '#191970'}),
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
                html.A('Part 3 - Impact of Global Warming on Life on Earth',href='', style={'textAlign': 'center','text-decoration': 'underline','color': '#191970'}),
            ),
            html.Li(
                html.A('Figure 9. Make me melt',href='', style={'font-size':'11px','color': '#191970'})
            ),
            html.Li(
                html.A('Figure 10. Impact on biodiversity (protected area)',href='', style={'font-size':'11px','color': '#191970'})
            ),
            html.Br(),
             html.Li(
                html.A('Part 4 - Projections: Forecasting the evolution of variables in play in the years to come ',href='', style={'textAlign': 'center','text-decoration': 'underline','color': '#191970'}),
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
#endregion

#region main content

#Main title
main_title = html.Div(
    [ 
        html.H1('A data centered view on Global Warming', style=TEXT_STYLE),
        "by Valérie Didier, Esperence Moussa, Colin Verhille, Christophe Duruisseau © TV-Freedom",
    ]
)

introduction = dbc.Row([
    tc_introduction
])

#part1 title 
part1_title = dbc.Row(align="center",justify="center",children=
    [
        dbc.Col(width="auto", children=[
        html.H2('Part 1 - Global warming')
        ] 
        )
    ]
)

#fig1 title 
fig1_title = dbc.Row([
    html.H4(tc_title_fig1),
    html.Div()]
)

#row fig1-txt1 content : 
fig1_txt1 = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_1',
            config = {
            'displayModeBar' : True
                    },
            figure = fig1
            )],md=7),
        dbc.Col(
            html.Div('''As defined by IPCC, climate in a narrow sense that is usually defined as the average weather, or more rigorously, as the statistical description in terms of the mean and variability of relevant quantities over a period of time ranging from months to thousands or millions of years. The relevant quantities are most often surface variables such as temperature, precipitation and wind. The history of climate change science began in the early 19th when the natural greenhouse effect was discovered by the french physicist Jospeh Fourier. During the 1990s, the increase of technology allowed to develop better models, then a consensus began to form : greenhouse gases were deeply involved in most climate changes and human-caused emissions were bringing discernible global warming. Since then, researchs was continued and the question of climate change and it's impact in short term on the environment is more and more at the hearts of today. Public opinion is also divided on this question and we'll try to provide answers on somes questions below in this document.''')
        ,md=5),  
        dbc.Row(
            html.Div('''As defined by IPCC, climate in a narrow sense that is usually defined as the average weather, or more rigorously, as the statistical description in terms of the mean and variability of relevant quantities over a period of time ranging from months
to thousands or millions of years. The relevant quantities are most often surface variables such as temperature, precipitation and wind.''')
        )
    ]
)

#fig2 title 
fig2_title = dbc.Row([
    html.H4('Worldwide temperature'),
    html.Div()]
)

#row fig2-txt2 content : 
fig2_txt2 = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_2',
            config = {
            'displayModeBar' : True
                    },
            figure = fig2
            )],md=7),
        dbc.Col(
            html.Div()
        ,md=5),  
        dbc.Row(
            html.Div()
        )
    ]
)

#fig3a title 
fig3a_title = dbc.Row([
    html.H4('Worldwide temperature'),
    html.Div()]
)

#row fig3a-txt3a content : 
fig3a_txt3a = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_3a',
            config = {
            'displayModeBar' : True
                    },
            figure = fig3a
            )],md=7),
        dbc.Col(
            html.Div()
        ,md=5),  
        dbc.Row(
            html.Div()
        )
    ]
)

#fig3b title 
fig3b_title = dbc.Row([
    html.H4('Worldwide temperature'),
    html.Div()]
)

#row fig3b-txt3b content : 
fig3b_txt3b = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_3b',
            config = {
            'displayModeBar' : True
                    },
            figure = fig3b
            )],md=7),
        dbc.Col(
            html.Div()
        ,md=5),  
        dbc.Row(
            html.Div()
        )
    ]
)

part2_title = dbc.Row(align="center",justify="center",children=
    [
        dbc.Col(width="auto", children=[
        html.H2('Part 2 - Impact of humans’ activities on global warming')
        ] 
        )
    ]
)

#fig4 title 
fig4_title = dbc.Row([
    html.H4('Worldwide temperature'),
    html.Div()]
)

#row fig4-txt4 content : 
fig4_txt4 = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_4',
            config = {
            'displayModeBar' : True
                    },
            figure = fig4
            )],md=7),
        dbc.Col(
            html.Div()
        ,md=5),  
        dbc.Row(
            html.Div()
        )
    ]
)

#fig5 title 
fig5_title = dbc.Row([
    html.H4('Worldwide temperature'),
    html.Div()]
)

#row fig5-txt5 content : 
fig5_txt5 = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_5',
            config = {
            'displayModeBar' : True
                    },
            figure = fig5
            )],md=7),
        dbc.Col(
            html.Div()
        ,md=5),  
        dbc.Row(
            html.Div()
        )
    ]
)

#fig6 title 
fig6_title = dbc.Row([
    html.H4('Worldwide temperature'),
    html.Div()]
)

#row fig6-txt6 content : 
fig6_txt6 = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_6',
            config = {
            'displayModeBar' : True
                    }
            )],md=7),
        dbc.Col(
            html.Div()
        ,md=5),  
        html.Div(
           #row 4 content : radio button for fig6
            dcc.RadioItems(inputStyle={"margin-right": "10px","margin-left":"20px"},
                id='radio_button_fig6',
                options=[{'label': j, 'value': i} for i,j in GHG_cat_name_dict.items()],
                value='GHG_cat'
            
)
        )
    ]
)

#fig7 title 
fig7_title = dbc.Row([
    html.H4('Worldwide temperature'),
    html.Div()]
)

#row fig7-txt7 content : 
fig7_txt7 = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_7',
            config = {
            'displayModeBar' : True
                    }
            )],md=7),
        dbc.Col(
            html.Div()
        ,md=5),  
    
        #row 4 content : radio button for fig6
       html.Div(
        dcc.RadioItems(inputStyle={"margin-right": "10px","margin-left":"20px"},
                id='radio_button_fig7',
                options=[{'label': j, 'value': i} for i,j in GHG_name_dict.items()],
                value='Total GHG',
            )) 


       
    ]
)

#fig6 title 
fig8_title = dbc.Row([
    html.H4('Worldwide temperature'),
    html.Div()]
)

#row fig8-txt8 content : 
fig8_txt8 = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_8',
            config = {
            'displayModeBar' : True
                    },
            figure = fig8
            )],md=7),
        dbc.Col(
            html.Div()
        ,md=5),  
        dbc.Row(
            html.Div()
        )
    ]
)

part3_title = dbc.Row(align="center",justify="center",children=
    [
        dbc.Col(width="auto", children=[
        html.H2('Part 3 - Impact of Global Warming on Life on Earth')
        ] 
        )
    ]
)

#fig9a title 
fig9a_title = dbc.Row([
    html.H4('Worldwide temperature'),
    html.Div()]
)

#row fig9a-txt9a content : 
fig9a_txt9a = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_9a',
            config = {
            'displayModeBar' : True
                    },
            figure = fig9a
            )],md=7),
        dbc.Col(
            html.Div()
        ,md=5),  
        dbc.Row(
            html.Div()
        )
    ]
)

#fig9b title 
fig9b_title = dbc.Row([
    html.H4('Worldwide temperature'),
    html.Div()]
)

#row fig9a-txt9a content : 
fig9b_txt9b = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_9b',
            config = {
            'displayModeBar' : True
                    },
            figure = fig9b
            )],md=7),
        dbc.Col(
            html.Div()
        ,md=5),  
        dbc.Row(
            html.Div()
        )
    ]
)

#fig10 title 
fig10_title = dbc.Row([
    html.H4('Worldwide temperature'),
    html.Div()]
)

#row fig9a-txt9a content : 
fig10_txt10 = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_10',
            config = {
            'displayModeBar' : True
                    },
            figure = fig10
            )],md=7),
        dbc.Col(
            html.Div()
        ,md=5),  
        dbc.Row(
            html.Div()
        )
    ]
)

part4_title = dbc.Row(align="center",justify="center",children=
    [
        dbc.Col(width="auto", children=[
        html.H2('Part 4 - Projections : Forecasting the evolution of variables in play in the years to come ')
        ] 
        )
    ]
)

#fig9b title 
fig11_title = dbc.Row([
    html.H4('Worldwide temperature'),
    html.Div()]
)

#row fig11-txt11 content : 
fig11_txt11 = dbc.Row(align="right", children=
    [
        dbc.Col(align='left',children=[
            dcc.Graph(id='graph_11',
            config = {
            'displayModeBar' : True
                    },
            figure = fig11
            )],md=7),
        dbc.Col(
            html.Div()
        ,md=5),  
        dbc.Row(
            html.Div()
        )
    ]
)

conclusion_title = dbc.Row(align="center",justify="center",children=
    [
        dbc.Col(width="auto", children=[
        html.H2('Conclusion')
        ] 
        )
    ]
)

conclusion = dbc.Row(align="center",justify="center",children=
    [   
        html.Div()
    ]
)

#Main content
content = html.Div(
    [
        main_title,
        html.Br(),
        introduction,
        html.Hr(),
        part1_title,
        html.Hr(),
        fig1_title,
        fig1_txt1,
        html.Br(),
        fig2_title,
        fig2_txt2,
        html.Br(),
        html.Br(),
        fig3a_title,
        fig3a_txt3a,
        fig3b_title,
        fig3b_txt3b,
        html.Hr(),
        part2_title,
        html.Hr(),
        fig4_title,
        fig4_txt4,
        fig5_title,
        fig5_txt5,
        fig6_title,
        fig6_txt6,
        fig7_title,
        fig7_txt7,
        fig8_title,
        fig8_txt8,
          html.Hr(),
        part3_title,
        html.Hr(),
        fig9a_title,
        fig9a_txt9a,
        fig9b_title,
        fig9b_txt9b,
        fig10_title,
        fig10_txt10,
        html.Hr(),
        part4_title,
        html.Hr(),
        fig11_title,
        fig11_txt11,
        html.Hr(),
        conclusion_title,
        html.Hr(),
        conclusion
    ],
    style=CONTENT_STYLE
)

#endregion

#use bootstrap stylesheet
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
#define page layout, which contains sidebar and content
app.layout = html.Div([sidebar, content])

#region callbacks

# Code for the clorepleth maps for Worldwide Greenhouse Gas Emissions:
@app.callback(
    Output('graph_6', 'figure'),
    [Input('radio_button_fig6', 'value')])
def update_graph_6(col_value):
  fig6 = px.choropleth(df_count_1990, 
                    locations="Code", 
                    color=col_value, 
                    hover_name="Country", 
                    color_continuous_scale=GHG_color_dict[col_value],
                    animation_frame="Year", 
                    range_color=[df_count_1990[col_value].min(),df_count_1990[col_value].max()], 
                    title=f'Worldwide {GHG_cat_name_dict[col_value]} emissions (tonnes of CO2 equivalent)'
                    )
  fig6.update_layout(margin={'r':0, 't':30, 'l':0, 'b':0}, coloraxis_colorbar=dict(title=f"{GHG_cat_name_dict[col_value]} emissions"))
  fig6.layout.coloraxis.colorbar = dict(
        title=f"{GHG_cat_name_dict[col_value]} emissions",
        tickvals=list(df_count_1990[col_value].unique()),
        ticktext=list(df_count_1990[GHG_label_dict[col_value]].unique()))
  # Disable auto for coloraxis setup:
  fig6.layout.coloraxis.cauto=False
  # Center the labels on the colorbar:
  fig6.layout.coloraxis.cmin = 0.5
  fig6.layout.coloraxis.cmax = (len(GHG_color_dict[col_value])/2)+0.5
  formatMap(fig6)
  return fig6


#Callback for fig7
@app.callback(
    Output('graph_7', 'figure'),
    [Input('radio_button_fig7', 'value')])
def update_graph(col_value):
  fig7 = px.scatter(world_1990_df, x=col_value, y='temperature_variations', trendline='ols')
  fig7.update_traces(marker={'color':GHG_disc_color_dict[col_value], 'size':7})
  fig7.update_layout(#title=f'Correlation between Temperature variation and {GHG_name_dict[col_value]} emissions',
                   xaxis_title=f'{GHG_name_dict[col_value]} emissions (tonnes)',
                   yaxis_title='Temperature Variation (degrees C)', 
                   plot_bgcolor='rgba(0,0,0,0.05)')
  formatScatter(fig7)
  return fig7

#endregion

#Run the server at port 8085
#Accessible through : http://localhost:8085
if __name__ == '__main__':
    app.run_server(port='8085')
