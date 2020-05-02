import requests
import sys, time
from pprint import pprint
import os

api_key = os.environ['YELP_API_KEY']

def get_business_category(business_id):

	url = 'https://api.yelp.com/v3/businesses/%s' %business_id
	headers = {'Authorization': 'Bearer %s' %api_key}

	resp = requests.get(url=url, params=None, headers=headers)

	return resp.json()

def get_business_match(name, address, city):

	url = 'https://api.yelp.com/v3/businesses/matches'
	headers = {'Authorization': 'Bearer %s' %api_key}

	params = {'name': name,
	'address1': address,
	'city' : city,
	'state' : 'CA',
	'country' : 'US',
	}

	resp = requests.get(url=url, params=params, headers=headers)
	
	if "businesses" not in resp.json():
		print(resp.json())
	return resp.json()['businesses']

if __name__ == '__main__':

	for line in sys.stdin:
		line = line.rstrip().split('\t')

		name = line[4]
		address = line[10]
		city = line[14]

		resp = get_business_match(name, address, city)
		if not resp:
			continue
		business_id = resp[0]['id']
		cat = get_business_category(business_id)
		pprint(cat["name"])
		pprint(cat)

