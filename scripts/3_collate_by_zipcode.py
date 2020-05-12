import json
from collections import defaultdict

'''
Converts restaurant details sorted by restaurant and collates them by zipcode
'''

cuisines = {}

with open('data/restaurant_details.json','r') as fin:
	rest_details = json.load(fin)

for rid in rest_details:
	
	this_rest = rest_details[rid]

	if this_rest["metadata"] is None:
		continue

	if "price" not in this_rest["metadata"]:
		continue

	zipcode = this_rest['zip_code']

	if zipcode not in cuisines:
		cuisines[zipcode] = {  "cat" : defaultdict(int), "prices" : [] , "ratings" : []}
	
	cats = this_rest['metadata']['categories']
	cats = [a['title'] for a in cats]
	rating = this_rest['metadata']['rating']
	price = len(this_rest['metadata']['price'])

	cuisines[zipcode]["prices"].append(price)
	cuisines[zipcode]["ratings"].append(rating)

	for k in cats:
		cuisines[zipcode]["cat"][k] += 1

with open('data/cuisines.json','w') as fout:
	json.dump(cuisines, fout, indent=2)
