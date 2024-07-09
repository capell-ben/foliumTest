#https://realpython.com/python-folium-web-maps-from-data/
import folium
import geopandas as gpd

#m = folium.Map()
#https://python-visualization.github.io/folium/latest/reference.html
#m = folium.Map(tiles="cartodb positron")
#m = folium.Map(location=(49.25, -123.12), tiles="cartodb positron")
states = (
   "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_1_states_provinces_shp.geojson"
)

# symbolize PRCs that provide abortion information vs those that don't.

huco_geojson = (
   r"C:\Users\capel\PyCharmProjs\HuCoPRC\MyProject\s_PDLscrape_FeaturesToJSON.geojson"
)

prcs = gpd.read_file(huco_geojson)
abort = prcs[prcs['Services'].str.contains("Abortion Information", case=False, na=False)| prcs['Services'].isnull()]
nonAbort = prcs[prcs['Services'].str.contains("Abortion Information", case=False)==False]

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

folium.GeoJson(nonAbort.to_json(),
                    marker = folium.CircleMarker(radius = 5, # Radius in metres
                                           weight = 1, #outline weight,
                                           color = 'white',
                                           fill_color = '#cc0000',
                                           fill_opacity = 1),
               popup=folium.GeoJsonPopup(fields=["PRC_Name", "Address", "Phone_Number", "Services"]),
               ).add_to(m)

folium.GeoJson(abort.to_json(),
                    marker = folium.CircleMarker(radius = 5, # Radius in metres
                                           weight = 1, #outline weight,
                                           color = 'white',
                                           fill_color = '#808080',
                                           fill_opacity = 1),
               popup=folium.GeoJsonPopup(fields=["PRC_Name", "Address", "Phone_Number", "Services"]),
               ).add_to(m)


title = 'Pregnancy Resource Centers (PRCs) in the US'
title_html = '''
             <h3 align="center" style="font-size:16px"><b>{}</b></h3>
             '''.format(title)
m.get_root().html.add_child(folium.Element(title_html))

# legend
item_txt = """<br> <i class="fa fa-circle" aria-hidden="true" style="color:{col}"></i> &nbsp; {item} &nbsp; """
html_itms = item_txt.format(item=f"{len(abort)} Provide Abortion Info", col="#808080")
html_itms += item_txt.format(item=f"{len(nonAbort)} Don't Provide Abortion Info", col="#cc0000")

legend_html = """
     <div style="
     position: fixed; 
     bottom: 50px; left: 50px; width: 250px; height: 80px; 
     border:2px solid grey; z-index:9999; 

     background-color:white;
     opacity: .85;

     font-size:14px;
     font-weight: bold;

     ">
     &nbsp; {title} 

     {itm_txt}

      </div> """.format(title=f"Total PRCs: {len(prcs)}", itm_txt=html_itms)
m.get_root().html.add_child(folium.Element(legend_html))

m.save("PregnancyResourceCenters.html")
