import numpy as np
import plotly.express as px

#get some continous color scales from plotly
continous_color_scales = px.colors.sequential.swatches()
#create dict with color name
color_dict = {}
for i in range(len(continous_color_scales['data'])):
    color_dict[continous_color_scales['data'][i]['y'][0]]=i

#Color specifications for CO2 
color_fig6_co2 = 'YlOrRd'
rangecolor_fig6_co2 = list(range(0,10))

#Color specifications for total greenhouse gas 
color_fig6_ghg = 'YlOrBr'
rangecolor_fig6_ghg = list(range(2,10))

#Color specifications for methane
color_fig6_meth = 'Reds'
rangecolor_fig6_meth = list(range(2,7))

#Color specification for nitrous oxide
color_fig6_no = 'OrRd'
rangecolor_fig6_no = list(range(2,7))

#Define intervals from number of category 
def getIntervalForMap(max_cat):
    return np.linspace(0,1,max_cat)

#Get custom color Pal based on defined var above
def getColorPal(pal,pal_range,intervalMap):
    customColor = []
    i = 0
    j = 0
    while j < len(intervalMap)-1:
        customColor.append((intervalMap[j],continous_color_scales['data'][color_dict[pal]]['marker']['color'][i]))
        j += 1
        customColor.append((intervalMap[j],continous_color_scales['data'][color_dict[pal]]['marker']['color'][i]))
        i += 1
    return customColor