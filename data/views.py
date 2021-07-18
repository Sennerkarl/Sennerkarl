import webbrowser
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
import re
import wbgapi as wb

class DataView(ListView):
    template_name = 'data/data.html'
    model = SBPRI
    context_object_name = 'SBPRI'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    # open context data which is sent to frontend  
        countries = sorted(list(Data.objects.values_list('country', flat=True).distinct())) # get country list from database
        context['title'] = 'Uncertainty Data'

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
                            customdata = ['https://google.com']
                        ))


        figmonth.update_layout(
                        template='plotly',
                        autosize=True,
                        margin=dict(l=0, r=0, b=10, t=10),
                        geo=dict(
                            showframe=False,
                            showcoastlines=False,
                            projection_type='equirectangular'
                        ),
                        
                    )

        trendmapmonth =  plot(figmonth, output_type='div', include_plotlyjs=False, config={'displayModeBar': False, 'displaylogo': False})
        context['trendmapmonth'] = trendmapmonth

        # Trends Diverging Deltas
        def trends(date1, date2):
            dates = list(Data.objects.order_by('-date').values_list('date', flat=True).distinct()[date1:date2])
            diff = []
            for country in countries:
                diff += [format(((Data.objects.filter(country=country, date=dates[0], category=category).values_list('value', flat=True)[0] / Data.objects.filter(country=country, date=dates[-1], category=category).values_list('value', flat=True)[0] - 1)*100), '.2f')]
            diff2 = [float(x) for x in diff] # convert strings in list to float
            trenddata = dict(zip(countries, diff2))
            trending = list(dict(sorted(trenddata.items(), key=lambda item: item[1])).items()) # sort values in dict
            return trending

        context['trendingmonth'] = trends(0,2)
        context['trendingannual'] = trends(0,13)
        

        #trendmap political regulation
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
                        margin=dict(l=0, r=0, b=10, t=10),
                        geo=dict(
                            showframe=False,
                            showcoastlines=False,
                            projection_type='orthographic'
                        ),
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
                        margin=dict(l=0, r=0, b=10, t=10),
                        geo=dict(
                            showframe=False,
                            showcoastlines=False,
                            projection_type='orthographic'
                        ),
                    )

        #trendmap political situation
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
                        margin=dict(l=0, r=0, b=10, t=10), 
                        geo=dict(
                            showframe=False,
                            showcoastlines=False,
                            projection_type='equirectangular'
                        ),
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
                        autosize=True, #responsive
                        margin=dict(l=0, r=0, b=10, t=10), #sizing
                        geo=dict(
                            showframe=False,
                            showcoastlines=False,
                            projection_type='equirectangular',
                        ),
                    )

        fig3 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 450,
        title = {'text': "Trend"},
        domain = {'x': [0, 1], 'y': [0, 1]}
        ))


        fig = go.Figure()
        fig.update_layout(
                        template='plotly_white',
                        autosize=True,
                        margin=dict(l=0, r=0, b=40, t=10),
                        )

        x = [date.strftime('%Y-%m-%d') for date in Data.objects.values_list('date', flat=True).distinct().order_by('date')]

        for cty in countries:
            if cty in ['Argentina', 'Austria', 'India']:
                fig.add_trace(go.Scatter(x=x, y=list(Data.objects.filter(country=cty, category='SBPRI').order_by('date').values_list('value', flat=True)), name=cty, opacity=0.8))
            else:
                fig.add_trace(go.Scatter(x=x, y=list(Data.objects.filter(country=cty, category='SBPRI').order_by('date').values_list('value', flat=True)), name=cty, opacity=0.8, visible = "legendonly" ))
        

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

        context['countries'] = countries

        #testing
        
        
        return context




# DataDetail.

class DataDetailView(ListView):
    model = SBPRI
    template_name = 'data/data-detail.html' # set new template to look for
    
    # link from country https://community.plotly.com/t/hyperlink-to-markers-on-map/17858

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        country = self.kwargs['country'].replace('_',' ').title()
        context['country'] = country
        context['title'] = f'{country} Uncertainty'

        
        qs = WorldBorder.objects.filter(name=country) #queryset of country row
        iso = qs.values('iso3')
        iso3 = iso[0]['iso3']
        
        # Uncertainty Country Monthly and Anually 
        figctry = go.Figure()
        category = "SBPRI"
        dates = list(Data.objects.order_by('-date').values_list('date', flat=True).distinct()[0:2])
        diff = [str((Data.objects.filter(country=country, date=dates[0], category=category).values_list('value', flat=True)[0] / Data.objects.filter(country=country, date=dates[-1], category=category).values_list('value', flat=True)[0] - 1)*100)]
        dates2 = list(Data.objects.order_by('-date').values_list('date', flat=True).distinct()[0:12])
        diff2 = [str((Data.objects.filter(country=country, date=dates2[0], category=category).values_list('value', flat=True)[0] / Data.objects.filter(country=country, date=dates2[-1], category=category).values_list('value', flat=True)[0] - 1)*100)]

        
        figctry.add_trace(go.Choropleth(
                            locations = [iso3], #borders to use
                            z = diff, #data with clever mapping function to get the data 
                            text = country, #text when hovering
                            colorscale='agsunset',
                            reversescale=True,
                            showscale = False,
                            marker_line_color='darkgray',
                            marker_line_width=0.5,
                            colorbar_tickprefix = '',
                            colorbar_title = 'SBPRI<br>Month<br>Trend',
                            zmin = -30,
                            zmax = 30,
                        ))
        
        button1 =  dict(method = "restyle",
                args = [{'z': [diff] }],
                label = "Monthly Trend")
        button2 =  dict(method = "restyle",
                args = [{'z': [diff2]}],
                label = "Annual Trend")
        

        figctry.update_layout(
                        template='plotly',
                        autosize=True,
                        margin=dict(l=0, r=0, b=20, t=0), 
                        geo_scope=qs.values_list('continent', flat=True)[0], #per country
                        updatemenus=[dict(y=0.9,
                                    x=0.175,
                                    xanchor='right',
                                    yanchor='top',
                                    active=0,
                                    buttons=[button1, button2])
                              ], 
                        geo=dict(
                            showframe=False,
                            showcoastlines=False,
                            projection_type='equirectangular',
                        ),
                    )

        worldmap = plot(figctry, output_type='div', include_plotlyjs=False, config={'displayModeBar': False, 'displaylogo': False})
        context['worldmap'] = worldmap

        # Country Line Graph compared to all? or maybe just continent
        countries = sorted(list(Data.objects.values_list('country', flat=True).distinct())) # get country list from database
        datetimeline = [date.strftime('%Y-%m-%d') for date in Data.objects.values_list('date', flat=True).distinct().order_by('date')]
        
        listSBPRI = list(Data.objects.filter(country=country, category='SBPRI').order_by('date').values_list('value', flat=True))
        listREGULATION = list(Data.objects.filter(country=country, category='Regulation').order_by('date').values_list('value', flat=True))
        listSANCTIONS = list(Data.objects.filter(country=country, category='Sanctions').order_by('date').values_list('value', flat=True))
        listSITUATION = list(Data.objects.filter(country=country, category='Situation').order_by('date').values_list('value', flat=True))

        figline = go.Figure()
        figline.update_layout(
                        template='plotly_white',
                        autosize=True,
                        margin=dict(l=0, r=0, b=40, t=10),
                        )

        
        figline.add_trace(go.Scatter(x=datetimeline, y=listSBPRI, name='Political Uncertainty', opacity=0.8))
        figline.add_trace(go.Scatter(x=datetimeline, y=listREGULATION, name='Investment Uncertainty', opacity=0.4))
        figline.add_trace(go.Scatter(x=datetimeline, y=listSANCTIONS, name='Trade Uncertainty', opacity=0.4 ))
        figline.add_trace(go.Scatter(x=datetimeline, y=listSITUATION, name='Administration Uncertainty', opacity=0.4, visible = "legendonly" ))

        linegraph = plot(figline, output_type='div', include_plotlyjs=False, config={'displayModeBar': False, 'displaylogo': False})
        context['linegraph'] = linegraph
        context['countries'] = countries

        #WorldbankData for Country
        dictforwb = {'CM.MKT.TRAD.CD':'VolumeStocksTraded', 'CM.MKT.TRAD.GD.ZS':'Stocks/GDP', 'NE.EXP.GNFS.KD':'ExportVolume',
         'NE.IMP.GNFS.KD':'ImportVolume','NY.GDP.PCAP.KD':'GDPPC', 'NY.GDP.MKTP.KD.ZG':'Growth',
          'BX.KLT.DINV.CD.WD':'FDI', 'NY.GDP.MKTP.CD':'GDP', 'SP.POP.TOTL':'Population'}
        df = wb.data.DataFrame(list(dictforwb), iso3 , mrnev=2)

        for key, value in dictforwb.items():
            dictvar = df.loc[key].dropna().to_dict()
            df.loc[key, 'Year'] = list(dictvar)[1][2:]
            
            if value in ['FDI', 'Population']:
                df.loc[key, 'Value'] = format(list(dictvar.values())[1]/10**6, ',.0f')
            if value in ['GDP', 'VolumeStocksTraded', 'ExportVolume', 'ImportVolume']:
                df.loc[key, 'Value'] = format(list(dictvar.values())[1]/10**9, ',.2f')
            if value in [ 'Stocks/GDP']:
                df.loc[key, 'Value'] = format(list(dictvar.values())[1]*100, ',.2f')
            if value in ['GDPPC', 'Growth']:
                df.loc[key, 'Value'] = format(list(dictvar.values())[1], ',.2f')
        
            df = df.rename(index={key:value})
        df = df.loc[:, ['Year','Value']]

        #GDP Rank Globally
        rank = wb.data.DataFrame('NY.GDP.MKTP.CD', mrv=1)
        rank['rank'] = rank.rank(ascending=False)
        
        #Data from Database - WorldBorder
        countryimport = WorldBorder.objects.filter(name=country).first()

        context['FDI'] = df.loc['FDI'].to_list()
        context['GDP'] = df.loc['GDP'].to_list()
        context['GDPPC'] = df.loc['GDPPC'].to_list() 
        context['Growth'] = df.loc['Growth'].to_list()
        context['VolumeStocksTraded'] = df.loc['VolumeStocksTraded'].to_list()
        context['Stocks/GDP'] = df.loc['Stocks/GDP'].to_list()
        context['ExportVolume'] = df.loc['ExportVolume'].to_list()
        context['ImportVolume'] = df.loc['ImportVolume'].to_list()
        context['Population'] = df.loc['Population'].to_list()
        context['CountryData'] = countryimport
        context['Rank'] = format(rank['rank'][iso3], '.0f')
        context['df'] = listSBPRI[-1]
        


        return context

