#https://realpython.com/python-folium-web-maps-from-data/
import folium

#m = folium.Map()
#https://python-visualization.github.io/folium/latest/reference.html
#m = folium.Map(tiles="cartodb positron")
#m = folium.Map(location=(49.25, -123.12), tiles="cartodb positron")
huco_geojson = (
   r"C:\Users\capel\PyCharmProjs\HuCoPRC\MyProject\s_PDLscrape_FeaturesToJSON.geojson"
)
m = folium.Map(location=(40, -100), tiles='Cartodb dark_matter', zoom_start=3)
folium.GeoJson(huco_geojson,
                    marker = folium.CircleMarker(radius = 3, # Radius in metres
                                           weight = 1, #outline weight,
                                           color = 'white',
                                           fill_color = '#cc0000',
                                           fill_opacity = 1),
               popup=folium.GeoJsonPopup(fields=["PRC_Name", "Address", "Phone_Number", "Services"]),
               ).add_to(m)

m.save("PregnancyResourceCenters.html")
