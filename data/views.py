from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.io as pio
from .models import SBPRI, WorldBorder

class DataView(ListView):
    template_name = 'data/data.html'
    model = SBPRI
    context_object_name = 'SBPRI'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        x = [date.strftime('%Y-%m-%d') for date in SBPRI.objects.values_list('date',flat=True)]
        y = SBPRI.objects.values_list('Bolivia',flat=True)
        countrylist = list(SBPRI.objects.values().last())[2:]
        latestSBPRI = list( map(SBPRI.objects.values().last().get, countrylist) )
        iso3s = []
        for cty in countrylist:
            qs = WorldBorder.objects.filter(name=cty)
            iso3 = qs.values('iso3')
            iso3s += [iso3[0]['iso3']]


        fig2 = go.Figure()
        fig2.add_trace(go.Choropleth(
                        locations = iso3s, #borders to use
                        z = latestSBPRI, #data
                        text = countrylist, #text when hovering
                        colorscale = 'Blues',
                        autocolorscale=False,
                        reversescale=True,
                        marker_line_color='darkgray',
                        marker_line_width=0.5,
                        colorbar_tickprefix = '',
                        colorbar_title = 'SBPRI<br>Index',
                       
                    ))

        fig2.update_layout(
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

        fig = go.Figure()
        fig.update_layout(height=400)
        fig.add_trace(go.Scatter(x=x, y=list(y), name='Bolivia', opacity=0.8))
        fig.add_trace(go.Scatter(x=x, y=list(SBPRI.objects.values_list('Colombia',flat=True)), name='Colombia', opacity=0.8))
        
        worldmap = plot(fig2, output_type='div', include_plotlyjs=False)
        context['worldmap'] = worldmap

        linegraph = plot(fig, output_type='div', include_plotlyjs=False)
        context['linegraph'] = linegraph
        return context

# Create your views here.
