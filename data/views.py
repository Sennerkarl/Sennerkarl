from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.io as pio
from .models import SBPRI, WorldBorder
import pandas as pd

class DataView(ListView):
    template_name = 'data/data.html'
    model = SBPRI
    context_object_name = 'SBPRI'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    # open context data which is sent to frontend  
        countrylist = list(SBPRI.objects.values().last())[2:] # get country list from database
        countrylist_space = [x.replace('_', ' ') for x in countrylist] #replace _ with spaces for each element of the countrylist

        iso3s = [] # empty list
        for cty in countrylist_space:
            qs = WorldBorder.objects.filter(name=cty) #queryset of country row
            iso3 = qs.values('iso3')                    #queryset of iso3 in that row
            iso3s += [iso3[0]['iso3']]                  #grab first value (only value) in new qs
        
        #build trendmap monthly
        fig4 = go.Figure()
        second = list(SBPRI.objects.values_list().order_by('-id')[1:2][0])[2:] #grab second last row from database by ordering by -id and picking the second one [1:2] and running it [0]
        last = list(SBPRI.objects.values_list().last())[2:] #grab last row
        diff = [((new / sec) - 1)*100 for (new, sec) in zip(last, second)] # divide the last and the second last value and rescale
        fig4.add_trace(go.Choropleth(
                            locations = iso3s, #borders to use
                            z = diff, #data with clever mapping function to get the data 
                            text = countrylist_space, #text when hovering
                            autocolorscale=True,
                            reversescale=True,
                            marker_line_color='darkgray',
                            marker_line_width=0.5,
                            colorbar_tickprefix = '',
                            colorbar_title = 'SBPRI<br>Month<br>Trend',
                            zmin = -30,
                            zmax = 30,
                        ))

        fig4.update_layout(
                        template='plotly',
                        autosize=True,
                        height=600,
                        geo=dict(
                            showframe=False,
                            showcoastlines=False,
                            projection_type='equirectangular'
                        ),
                        annotations = [dict(
                            x=0.55,
                            y=0.1,
                            xref='paper',
                            yref='paper',
                            text='Source: <a href="">Google Trend Analysis by Senne & Reinthaler</a>',
                            showarrow = False
                        )]
                    )

        #build trendmap annually
        fig5 = go.Figure()
        second = list(SBPRI.objects.values_list().order_by('-id')[11:12][0])[2:]
        last = list(SBPRI.objects.values_list().last())[2:]
        diff = [((new / sec) - 1)*100 for (new, sec) in zip(last, second)]
        fig5.add_trace(go.Choropleth(
                            locations = iso3s, #borders to use
                            z = diff, #data with clever mapping function to get the data 
                            text = countrylist_space, #text when hovering
                            autocolorscale=True,
                            reversescale=True,
                            marker_line_color='darkgray',
                            marker_line_width=0.5,
                            colorbar_tickprefix = '',
                            colorbar_title = 'SBPRI<br>Annual<br>Trend',
                            zmin = -30,
                            zmax = 30,
                        ))

        fig5.update_layout(
                        template='plotly',
                        autosize=True,
                        height=600,
                        geo=dict(
                            showframe=False,
                            showcoastlines=False,
                            projection_type='equirectangular'
                        ),
                        annotations = [dict(
                            x=0.55,
                            y=0.1,
                            xref='paper',
                            yref='paper',
                            text='Source: <a href="">Google Trend Analysis by Senne & Reinthaler</a>',
                            showarrow = False
                        )]
                    )

        #build worldmap
        fig2 = go.Figure()
        for datepoints in SBPRI.objects.values():   # SBPRI.objects.values() are the rows for each date
            fig2.add_trace(go.Choropleth(
                            locations = iso3s, #borders to use
                            z = list( map(datepoints.get, countrylist) ), #data with clever mapping function to get the data 
                            text = countrylist_space, #text when hovering
                            autocolorscale=True,
                            reversescale=True,
                            marker_line_color='darkgray',
                            marker_line_width=0.5,
                            colorbar_tickprefix = '',
                            colorbar_title = 'SBPRI<br>Index',
                            zmin = 0,
                            zmax = 50,
                        ))

        

        # Create and add slider 
        steps = [] #https://plotly.com/python/sliders/
        for i in range(len(fig2.data)):
            step = dict(
                method="update",
                args=[{"visible": [False] * len(fig2.data)},
                    {"title":"SBPRI in " + SBPRI.objects.values_list('date', flat=True).get(id=i+1).strftime("%Y, %B")}],  # layout attribute list(SBPRI.objects.filter(id=i).values('date'))[0]['date'])
                label=SBPRI.objects.values_list('date', flat=True).get(id=i+1).strftime("%Y, %B") # +1 because id starts at 1 not 0
            )
            step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
            steps.append(step)

        sliders = [dict(
            active=len(fig2.data)-1,
            currentvalue={"prefix": "Date: "},
            pad={"t": 50},
            steps=steps
        )]

        fig2.update_layout(
                        template='plotly',
                        autosize=True,
                        height=600,
                        sliders=sliders,
                        geo=dict(
                            showframe=False,
                            showcoastlines=False,
                            projection_type='equirectangular'
                        ),
                        annotations = [dict(
                            x=0.55,
                            y=0.1,
                            xref='paper',
                            yref='paper',
                            text='Source: <a href="">Google Trend Analysis by Senne & Reinthaler</a>',
                            showarrow = False
                        )]
                    )

        fig3 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 450,
        title = {'text': "Trend"},
        domain = {'x': [0, 1], 'y': [0, 1]}
        ))


        fig = go.Figure()
        fig.update_layout(height=400, template='plotly_white')

        x = [date.strftime('%Y-%m-%d') for date in SBPRI.objects.values_list('date',flat=True)]

        for cty in countrylist:
            fig.add_trace(go.Scatter(x=x, y=list(SBPRI.objects.values_list(cty,flat=True)), name=cty, opacity=0.8))
        
        worldmap = plot(fig2, output_type='div', include_plotlyjs=False, config={'displayModeBar': False, 'displaylogo': False})
        context['worldmap'] = worldmap

        linegraph = plot(fig, output_type='div', include_plotlyjs=False, config={'displayModeBar': False, 'displaylogo': False})
        context['linegraph'] = linegraph

        trend =  plot(fig3, output_type='div', include_plotlyjs=False, config={'displayModeBar': False, 'displaylogo': False})
        context['trend'] = trend

        trendmap =  plot(fig4, output_type='div', include_plotlyjs=False, config={'displayModeBar': False, 'displaylogo': False})
        context['trendmap'] = trendmap

        trendmapannual =  plot(fig5, output_type='div', include_plotlyjs=False, config={'displayModeBar': False, 'displaylogo': False})
        context['trendmapannual'] = trendmapannual

        #testing
        context['array'] = SBPRI.objects.values_list('date', flat=True).get(id=1)
        
        return context

# Create your views here.
