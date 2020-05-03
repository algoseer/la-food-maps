import folium
import sys
import json
import numpy as np
import collections


#Load the categories in each zip code
with open('data/cuisines.json') as fin:
	cats = json.load(fin)

with open('categories.txt') as fin:
	red_cats = [a.rstrip().split('\t') for a in fin.readlines()]		#Reduced set of categories

allzips = list(cats.keys())

#Map down the restaurants in the reduced number of categories
table = {}
cuisine_maps ={}
cuisine_all ={}
for z in allzips:	
	cats_this_zip = cats[z]['all']
	count=np.zeros(len(red_cats))
	
	for i,cl in enumerate(red_cats):
		cnt = sum([cats_this_zip[a] for a in cats_this_zip if a in cl])
		count[i]+=cnt
	table[z] = count.argmax()
	cuisine_maps[z] = red_cats[count.argmax()][0]
	cuisine_all[z] = {k[0]:count[i] for i,k in enumerate(red_cats)}


with open('data/la-zip-code-areas-2012.json') as fin:
	data = json.load(fin)

geozips = []
for i in range(len(data['features'])):
	if data['features'][i]['properties']['name'] in allzips:
		dd = data['features'][i]
		dd['properties']['cuisine'] = cuisine_maps[dd['properties']['name']]
		dd['properties']['cats'] = cuisine_all[dd['properties']['name']]
		geozips.append(dd)

new_json = dict.fromkeys(['type','features'])
new_json['type'] = 'FeatureCollection'
new_json['features'] = geozips


la_geo = 'data/data.json'
with open(la_geo,'w') as fout:
	json.dump(new_json, fout, sort_keys=True, indent=4, separators=(',',': '))



		

m = folium.Map(location = [34.0522, -118.2437], zoom_start = 11)
cuisine  = folium.Choropleth(geo_data = la_geo,
		fill_opacity = 0.7,
		line_opactiy = 0.2,
		name="cuisines",
		data = table,
		key_on = 'feature.properties.name',
		fill_color = 'Paired',
		bins=12
		)
cuisine.add_to(m)

cuisine.geojson.add_child(folium.features.GeoJsonTooltip(fields=['name','cuisine'], aliases=["Zipcode","Cuisine"],labels = True))

folium.LayerControl().add_to(m)

m.save(outfile = 'index.html')


