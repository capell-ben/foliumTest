#https://realpython.com/python-folium-web-maps-from-data/
import folium

#m = folium.Map()
#https://python-visualization.github.io/folium/latest/reference.html
#m = folium.Map(tiles="cartodb positron")
#m = folium.Map(location=(49.25, -123.12), tiles="cartodb positron")
political_countries_url = (
    "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
)

m = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")
folium.GeoJson(political_countries_url).add_to(m)

m.save("footprint.html")
