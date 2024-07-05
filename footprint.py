#https://realpython.com/python-folium-web-maps-from-data/
import folium
import pandas as pd
import requests
import json
import pandas_geojson as pdg

eco_footprints = pd.read_csv("footprint.csv")
max_eco_footprint = eco_footprints["Ecological footprint"].max()
political_countries_url = (
    "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
)

political_geojson_response = requests.get(political_countries_url)
political_geojson_d = json.loads(political_geojson_response.text)

m = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")

"""folium.Choropleth(
    geo_data=political_countries_url,
    data=eco_footprints,
    columns=("Country/region", "Ecological footprint"),
    key_on="feature.properties.name",
    bins=(0, 1, 1.5, 2, 3, 4, 5, 6, 7, 8, max_eco_footprint),
    fill_color="RdYlGn_r",
    fill_opacity=0.8,
    line_opacity=0.3,
    nan_fill_color="white",
    legend_name="Ecological footprint per capita",
    name="Countries by ecological footprint per capita",
).add_to(m)"""

political_geojson = pdg.GeoJSON.from_dict(political_geojson_d)
political_df = political_geojson.to_dataframe()
political_df['economy'] = [float(economy[0]) for economy in political_df['properties.economy'].to_list() ]

folium.Choropleth(
    geo_data=political_countries_url,
    data=political_df,
    columns=('properties.name', "economy"),
    key_on="feature.properties.name",
    bins=( 0, 1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1),
    fill_color="RdYlGn_r",
    fill_opacity=0.8,
    line_opacity=0.3,
    nan_fill_color="black",
    legend_name="Economy classification",
    name="Economy classification",
).add_to(m)

popup = folium.GeoJsonPopup(fields=["name", "economy"])
folium.GeoJson(
    political_geojson_d,
    style_function=lambda feature: {
            "fillColor": "#1C00ff00",
            "color": "grey",
            "weight": 0.3,
        },
    highlight_function=lambda feature: {
        "fillColor": (
            "green" if " G7" in feature["properties"]["economy"] else "#1C00ff00"
        ),
    },
    popup=popup,
    popup_keep_highlighted=True,
    name = 'Country Names',
    zoom_on_click = True
).add_to(m)
folium.LayerControl().add_to(m)

m.save("footprint.html")
