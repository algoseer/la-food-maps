import folium
import sys
import json
import numpy as np

keywords = sys.argv[1:]

with open('inspections.json') as fin:
	insp = json.load(fin)

allzips = list(set([a['FACILITY ZIP'].split('-')[0] for a in insp]))

with open('la-zip-code-areas-2012.json') as fin:
	data = json.load(fin)

geozips = []

for i in range(len(data['features'])):
	if data['features'][i]['properties']['name'] in allzips:
		geozips.append(data['features'][i])

new_json = dict.fromkeys(['type','features'])
new_json['type'] = 'FeatureCollection'
new_json['features'] = geozips

la_geo = 'data.json'
with open(la_geo,'w') as fout:
	json.dump(new_json, fout, sort_keys=True, indent=4, separators=(',',': '))

print(len(allzips))

#Collate the data to plot
table = {"count":{},"score":{}}
table["kw"]={k:{} for k in keywords}

print(table)

for zipcode in allzips:
	print(zipcode)
	avg_score = np.array([a['SCORE'] for a in insp if a['FACILITY ZIP'].startswith(zipcode)],dtype='float').mean()
	count = len([a['SCORE'] for a in insp if a['FACILITY ZIP'].startswith(zipcode)])
	table["count"][zipcode] = count
	table["score"][zipcode] = avg_score
	for keyword in keywords:
		kwcount =len([a['SCORE'] for a in insp if a['FACILITY ZIP'].startswith(zipcode) and keyword in a['FACILITY NAME']])
		table["kw"][keyword][zipcode] = kwcount


print("Finished writing data for plotting..")

m = folium.Map(location = [34.0522, -118.2437], zoom_start = 11)

#folium.Choropleth(geo_data = la_geo,
#		fill_opacity = 0.7,
#		line_opactiy = 0.2,
#		name="score",
#		data = table["score"],
#		key_on = 'feature.properties.name',
#		fill_color = 'RdYlGn'
#		).add_to(m)
#
#folium.Choropleth(geo_data = la_geo,
#		fill_opacity = 0.7,
#		line_opactiy = 0.2,
#		name="count",
#		data = table["count"],
#		key_on = 'feature.properties.name',
#		fill_color = 'RdYlGn'
#		).add_to(m)

#Store each keyword in a different layer
for kw in keywords:
	folium.Choropleth(geo_data = la_geo,
			fill_opacity = 0.7,
			line_opactiy = 0.2,
			name=kw,
			data = table["kw"][kw],
			key_on = 'feature.properties.name',
			fill_color = 'RdYlGn'
			).add_to(m)

folium.LayerControl().add_to(m)

m.save(outfile = 'out/index.html')


