#build worldmap
        fig2 = go.Figure()
        for datepoints in SBPRI.objects.values():   # SBPRI.objects.values() are the rows for each date
            fig2.add_trace(go.Choropleth(
                            locations = iso3s, #borders to use
                            z = list( map(datepoints.get, countrylist) ), #data with clever mapping function to get the data 
                            text = countrylist_space, #text when hovering
                            colorscale='agsunset',
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

        