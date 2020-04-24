import json
import sys

'''
Convert a tsv file to json treating the first row as headers
'''
keys=[]
entries=[]

if sys.argv[1].endswith('.json'):
	with open(sys.argv[1],'r') as fin:
		entries = json.load(fin)
else:
	with open(sys.argv[1],'r') as fin:
		for line in fin:
			fields=line.rstrip().split('\t')
			if not keys:
				keys = fields
			else:
				entries.append(dict(zip(keys, fields)))

with open(sys.argv[2],'w') as fout:
	json.dump(entries,fout,indent=2)
