import numpy as np
import plotly.express as px

#region Text elements
tc_introduction = '''As defined by IPCC, climate in a narrow sense that is usually defined as the average weather, or more rigorously, as the statistical description in terms of the mean and variability of relevant quantities over a period of time ranging from months
to thousands or millions of years. The relevant quantities are most often surface variables such as temperature, precipitation and wind.

The history of climate change science began in the early 19th when the natural greenhouse effect was discovered by the french physicist Jospeh Fourier.

During the 1990s, the increase of technology allowed to develop better models, then a consensus began to form : greenhouse gases were deeply involved in most climate changes and human-caused emissions were bringing discernible global warming.

Since then, researchs was continued and the question of climate change and it's impact in short term on the environment is more and more at the hearts of today.

Public opinion is also divided on this question and we'll try to provide answers on somes questions below in this document.'''

tc_title_fig1 = 'Fig 1. Global temperature : Deviation from the mean'
tc_title_fig2 = 'Worldwide temperatures variations'
tc_title_fig3a = 'Global temperature since -19 000 (TraCE-21ka simulation)'
tc_title_fig3b = 'Global temperature since JC'
tc_title_fig4 = 'Temperature variations compared to solar activity variation (deviation from period 1961-1990)'
tc_title_fig5 = 'Global Greenhouse Gas Emissions'
tc_title_fig6 = 'Worldwide Carbone Dioxide emissions (tonnes of CO2 equivalent)'
tc_title_fig7 = 'Correlation between Temperature variation and Carbone Dioxide emissions'
tc_title_fig8 = 'CO2 Variation (%)'
tc_title_fig9a = 'Global sea level variation (cm, compared to 1990)'
tc_title_fig9b = 'Glaciers mass variation (compared to 1966)'
tc_title_fig10 = 'Worldwide biodiversity evolution'
tc_title_fig11 = 'Projected temperature evolution'



#endregion

#region Graph color

#get some continous color scales from plotly
continous_color_scales = px.colors.sequential.swatches()
#create dict with color name
color_dict = {}
for i in range(len(continous_color_scales['data'])):
    color_dict[continous_color_scales['data'][i]['y'][0]]=i

#Define intervals from number of category 
def getIntervalForMap(max_cat):
    return np.linspace(0,1,max_cat)

#Get custom color Pal based on defined var above
# Function to get the color scale for the different maps:

# Creating a dictionnary with the plotly scales colors values:
continous_color_scales = px.colors.sequential.swatches()
color_dict = {}
for i in range(len(continous_color_scales['data'])):
  color_dict[continous_color_scales['data'][i]['y'][0]]=i

#Get custom color Pal based on defined var above
def getColorPal(pal, pal_start_range, max_cat):
  '''This function return a list of tuples with the interval range and its associated color to display the side color bar.
  The function takes in 3 arguments:
  pal =  Palette name, 
  pal_start_range = index of the first color wanted from the palette,
  max_cat = number of categories needed'''
  customColor = []
  intervalMap = np.linspace(0,1,max_cat+1)
  i = pal_start_range
  j = 0
  while j+1 <= max_cat:
    customColor.append((intervalMap[j],continous_color_scales['data'][color_dict[pal]]['marker']['color'][i]))
    j += 1
    customColor.append((intervalMap[j],continous_color_scales['data'][color_dict[pal]]['marker']['color'][i]))
    i += 1
  return customColor

#endregion