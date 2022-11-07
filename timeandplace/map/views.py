from django.shortcuts import render
from .models import place
import folium 
from folium import plugins, raster_layers
from django_pandas.io import read_frame
# Create your views here.

def index(request):
    m = folium.Map(location=[40.79028, -73.95972], zoom_start=12)
    map1 = raster_layers.TileLayer(tiles='CartoDB Dark_Matter').add_to(m)
    map2 = raster_layers.TileLayer(tiles='CartoDB Positron').add_to(m)
    map3 = raster_layers.TileLayer(tiles='Stamen Terrain').add_to(m)
    map4 = raster_layers.TileLayer(tiles='Stamen Toner').add_to(m)
    map5 = raster_layers.TileLayer(tiles='Stamen Watercolor').add_to(m)
    folium.LayerControl().add_to(m)
    qs = place.objects.all()
    df = read_frame(qs, fieldnames=['DBA', 'BORO', 'BUILDING', 'STERRT','ZIPCODE','PHONE','CUISION','LATITUDE','LONGTITUDE'])
    # print(df)
    for (index, rows) in df.iterrows():
        html="""
            <b>Name: </b> {} </br>
            <b>Phone: </b> {} </br>
            <b>Cuision: </b> {}
            """.format(rows.loc['DBA'],rows.loc['PHONE'],rows.loc['CUISION'])

        iframe = folium.IFrame(html,
                            width=150,
                            height=90)

        popup = folium.Popup(iframe,
                            max_width=150)


        folium.Marker(location=[rows.loc['LATITUDE'],
                                rows.loc['LONGTITUDE']], popup=popup).add_to(m)

    plugins.Fullscreen().add_to(m)
    m = m._repr_html_()
    context = {
        'm': m
    }
    return render(request, 'map/index.html',context)
    