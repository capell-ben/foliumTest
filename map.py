#https://realpython.com/python-folium-web-maps-from-data/
import folium

#m = folium.Map()
#https://python-visualization.github.io/folium/latest/reference.html
#m = folium.Map(tiles="cartodb positron")
#m = folium.Map(location=(49.25, -123.12), tiles="cartodb positron")
states = (
   "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_1_states_provinces_shp.geojson"
)

huco_geojson = (
   r"C:\Users\capel\PyCharmProjs\HuCoPRC\MyProject\s_PDLscrape_FeaturesToJSON.geojson"
)

m = folium.Map(location=(40, -100), tiles='Cartodb dark_matter', zoom_start=3)

# https://leafletjs.com/reference.html#path-color
folium.GeoJson(states,
               style_function=lambda feature: {
        "fill": False,
        "color": "white",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.9,
    }).add_to(m)

folium.GeoJson(huco_geojson,
                    marker = folium.CircleMarker(radius = 3, # Radius in metres
                                           weight = 1, #outline weight,
                                           color = 'white',
                                           fill_color = '#cc0000',
                                           fill_opacity = 1),
               popup=folium.GeoJsonPopup(fields=["PRC_Name", "Address", "Phone_Number", "Services"]),
               ).add_to(m)

title = 'Pregnancy Resource Center in the US'
title_html = '''
             <h3 align="center" style="font-size:16px"><b>{}</b></h3>
             '''.format(title)
m.get_root().html.add_child(folium.Element(title_html))

m.save("PregnancyResourceCenters.html")
