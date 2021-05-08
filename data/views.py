from django.shortcuts import render
from django.http import HttpResponse
from django.urls.base import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.io as pio
from .models import Data, SBPRI, WorldBorder
import pandas as pd
import webbrowser

class DataView(ListView):
    template_name = 'data/data.html'
    model = SBPRI
    context_object_name = 'SBPRI'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    # open context data which is sent to frontend  
        countries = sorted(list(Data.objects.values_list('country', flat=True).distinct())) # get country list from database
        

        iso3s = [] # empty list
        for cty in countries:
            qs = WorldBorder.objects.filter(name=cty) #queryset of country row
            iso3 = qs.values('iso3')                    #queryset of iso3 in that row
            iso3s += [iso3[0]['iso3']]                  #grab first value (only value) in new qs
        

        #build trendmap monthly with Data Model
        
        figmonth = go.Figure()
        category = 'SBPRI'
        dates = list(Data.objects.order_by('-date').values_list('date', flat=True).distinct()[0:2])
        diff = []
        for country in countries:
            diff += [str((Data.objects.filter(country=country, date=dates[0], category=category).values_list('value', flat=True)[0] / Data.objects.filter(country=country, date=dates[1], category=category).values_list('value', flat=True)[0] - 1)*100)]
        
        figmonth.add_trace(go.Choropleth(
                            locations = iso3s, #borders to use
                            z = diff, #data with clever mapping function to get the data 
                            text = countries, #text when hovering
                            colorscale='agsunset', #https://plotly.com/python/builtin-colorscales/
                            reversescale=True,
                            marker_line_color='darkgray',
                            marker_line_width=0.5,
                            colorbar_tickprefix = '',
                            colorbar_title = 'SBPRI<br>Month<br>Trend',
                            showscale = False,
                            zmin = -30,
                            zmax = 30,
                        ))

        figmonth.update_layout(
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
                            text='Source: <a href="">Google Trend Analysis</a>',
                            showarrow = False
                        )]
                    )

        #trenmap political regulation
        figreg = go.Figure()
        category = 'Regulation'
        dates = list(Data.objects.order_by('-date').values_list('date', flat=True).distinct()[0:2])
        diff = []
        for country in countries:
            diff += [str((Data.objects.filter(country=country, date=dates[0], category=category).values_list('value', flat=True)[0] / Data.objects.filter(country=country, date=dates[1], category=category).values_list('value', flat=True)[0] - 1)*100)]
        
        figreg.add_trace(go.Choropleth(
                            locations = iso3s, #borders to use
                            z = diff, #data with clever mapping function to get the data 
                            text = countries, #text when hovering
                            colorscale='agsunset', #https://plotly.com/python/builtin-colorscales/
                            reversescale=True,
                            marker_line_color='darkgray',
                            marker_line_width=0.5,
                            colorbar_tickprefix = '',
                            colorbar_title = 'SBPRI<br>Month<br>Trend',
                            showscale = False,
                            zmin = -30,
                            zmax = 30,
                        ))

        figreg.update_layout(
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
                            text='Source: <a href="">Google Trend Analysis</a>',
                            showarrow = False
                        )]
                    )

        #trenmap political sanctions
        figsanc = go.Figure()
        category = 'Sanctions'
        dates = list(Data.objects.order_by('-date').values_list('date', flat=True).distinct()[0:2])
        diff = []
        for country in countries:
            diff += [str((Data.objects.filter(country=country, date=dates[0], category=category).values_list('value', flat=True)[0] / Data.objects.filter(country=country, date=dates[1], category=category).values_list('value', flat=True)[0] - 1)*100)]
        
        figsanc.add_trace(go.Choropleth(
                            locations = iso3s, #borders to use
                            z = diff, #data with clever mapping function to get the data 
                            text = countries, #text when hovering
                            colorscale='agsunset', #https://plotly.com/python/builtin-colorscales/
                            reversescale=True,
                            marker_line_color='darkgray',
                            marker_line_width=0.5,
                            colorbar_tickprefix = '',
                            colorbar_title = 'SBPRI<br>Month<br>Trend',
                            showscale = False,
                            zmin = -30,
                            zmax = 30,
                        ))

        figsanc.update_layout(
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
                            text='Source: <a href="">Google Trend Analysis</a>',
                            showarrow = False
                        )]
                    )

        #trenmap political situation
        figsitu = go.Figure()
        category = 'Sanctions'
        dates = list(Data.objects.order_by('-date').values_list('date', flat=True).distinct()[0:2])
        diff = []
        for country in countries:
            diff += [str((Data.objects.filter(country=country, date=dates[0], category=category).values_list('value', flat=True)[0] / Data.objects.filter(country=country, date=dates[1], category=category).values_list('value', flat=True)[0] - 1)*100)]
        
        figsitu.add_trace(go.Choropleth(
                            locations = iso3s, #borders to use
                            z = diff, #data with clever mapping function to get the data 
                            text = countries, #text when hovering
                            colorscale='agsunset', #https://plotly.com/python/builtin-colorscales/
                            reversescale=True,
                            marker_line_color='darkgray',
                            marker_line_width=0.5,
                            colorbar_tickprefix = '',
                            colorbar_title = 'SBPRI<br>Month<br>Trend',
                            showscale = False,
                            zmin = -30,
                            zmax = 30,
                        ))

        figsitu.update_layout(
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
        figannual = go.Figure()
        category = 'SBPRI'
        dates = list(Data.objects.order_by('-date').values_list('date', flat=True).distinct()[0:12])
        diff = []
        for country in countries:
            diff += [str((Data.objects.filter(country=country, date=dates[0], category=category).values_list('value', flat=True)[0] / Data.objects.filter(country=country, date=dates[-1], category=category).values_list('value', flat=True)[0] - 1)*100)]
        
        figannual.add_trace(go.Choropleth(
                            locations = iso3s, #borders to use
                            z = diff, #data with clever mapping function to get the data 
                            text = countries, #text when hovering
                            colorscale='agsunset',
                            reversescale=True,
                            marker_line_color='darkgray',
                            marker_line_width=0.5,
                            colorbar_tickprefix = '',
                            colorbar_title = 'SBPRI<br>Annual<br>Trend',
                            showscale = False,
                            zmin = -30,
                            zmax = 30,
                        ))

        figannual.update_layout(
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

        fig3 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 450,
        title = {'text': "Trend"},
        domain = {'x': [0, 1], 'y': [0, 1]}
        ))


        fig = go.Figure()
        fig.update_layout(height=400, template='plotly_white')

        x = [date.strftime('%Y-%m-%d') for date in Data.objects.values_list('date', flat=True).distinct()]

        for cty in countries:
            if cty in ['Argentina', 'Austria', 'India']:
                fig.add_trace(go.Scatter(x=x, y=list(Data.objects.filter(country=cty, category=category).values_list('value', flat=True)), name=cty, opacity=0.8))
            else:
                fig.add_trace(go.Scatter(x=x, y=list(Data.objects.filter(country=cty, category=category).values_list('value', flat=True)), name=cty, opacity=0.8, visible = "legendonly" ))
        

        linegraph = plot(fig, output_type='div', include_plotlyjs=False, config={'displayModeBar': False, 'displaylogo': False})
        context['linegraph'] = linegraph

        trend =  plot(fig3, output_type='div', include_plotlyjs=False, config={'displayModeBar': False, 'displaylogo': False})
        context['trend'] = trend

        trendmapreg =  plot(figreg, output_type='div', include_plotlyjs=False, config={'displayModeBar': False, 'displaylogo': False})
        context['trendmapreg'] = trendmapreg

        trendmapsanc =  plot(figsanc, output_type='div', include_plotlyjs=False, config={'displayModeBar': False, 'displaylogo': False})
        context['trendmapsanc'] = trendmapsanc

        trendmapsitu =  plot(figsitu, output_type='div', include_plotlyjs=False, config={'displayModeBar': False, 'displaylogo': False})
        context['trendmapsitu'] = trendmapsitu

        trendmapannual =  plot(figannual, output_type='div', include_plotlyjs=False, config={'displayModeBar': False, 'displaylogo': False})
        context['trendmapannual'] = trendmapannual

        trendmapmonth =  plot(figmonth, output_type='div', include_plotlyjs=False, config={'displayModeBar': False, 'displaylogo': False})
        context['trendmapmonth'] = trendmapmonth

        #testing
        context['array'] = SBPRI.objects.values_list('date', flat=True).get(id=1)
        
        return context




# DataDetail.

class DataDetailView(ListView):
    model = SBPRI
    template_name = 'data/data-detail.html' # set new template to look for
    
    # link from country https://community.plotly.com/t/hyperlink-to-markers-on-map/17858

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        country = self.kwargs['country'].capitalize()
        context['country'] = country
        
        if country in list(SBPRI.objects.values().last())[2:]:
            fig6 = go.Figure()
            iso3 = list(WorldBorder.objects.filter(name=country).values_list('iso3'))[0][0]
            second = list(SBPRI.objects.values_list(country).order_by('-id'))[1:2] #grab second last row from database by ordering by -id and picking the second one [1:2] and running it [0]
            last = list(SBPRI.objects.values_list(country).last()) #grab last row
            diff = ((last[0] / second[0][0]) - 1)*100 # divide the last and the second last value and rescale
            fig6.add_trace(go.Choropleth(
                                locations = [iso3], #borders to use
                                z = [diff], #data with clever mapping function to get the data 
                                text = country, #text when hovering
                                autocolorscale=True,
                                reversescale=True,
                                marker_line_color='darkgray',
                                marker_line_width=0.5,
                                colorbar_tickprefix = '',
                                colorbar_title = 'SBPRI<br>Month<br>Trend',
                                zmin = -30,
                                zmax = 30,
                            ))

            fig6.update_layout(
                            template='plotly',
                            autosize=True, 
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
            worldmap = plot(fig6, output_type='div', include_plotlyjs=False, config={'displayModeBar': False, 'displaylogo': False})
            context['worldmap'] = worldmap

        return context
