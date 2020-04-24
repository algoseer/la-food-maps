import sys, json
'''
Since there are multiple inspections for each restaurant we want to only unique calls to Yelp Fusion API
'''
inspections_dict = sys.argv[1]

with open(inspections_dict, 'r') as fin:
	insp = json.load(fin)

rest={}

for ent in insp:

	fid = ent["FACILITY ID"]
	date = ent["ACTIVITY DATE"]
	name = ent["FACILITY NAME"]
	address = ent["FACILITY ADDRESS"]
	city = ent["FACILITY CITY"]
	zipcode = ent["FACILITY ZIP"]
	score = ent["SCORE"]
	grade = ent["GRADE"]

	if fid not in rest:
		rest[fid]={'name':name, 'address1':address, 'city':city, 'zip_code': zipcode, 'score' : [score], 'grade' : [grade]}
	else:
		rest[fid]['score'].append(score)
		rest[fid]['grade'].append(grade)
	
print(len(rest))

with open('data/by_restaurants.json','w') as fout:
	json.dump(rest, fout, indent=2)
