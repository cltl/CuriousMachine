import pickle
store_me={}
path='data/aida/'
outfile='%stopics.pickle' % path
for level in ['Low', 'Top']:
	infile='%sAIDA-YAGO2-dataset_topics%slevel.tsv' % (path, level)
	with open(infile, 'r') as f:
		for line in f:
			if 'DOCSTART' in line:
				line=line.strip()
				base, topic=line.split('\t')
				clean_base=base.split('(')[1].rstrip(')')
				file_id, title=clean_base.split(' ')
				if file_id not in store_me:
					store_me[file_id]={'title': title.upper()}
				store_me[file_id][level]=topic.upper()
				#print(topic)
pickle.dump(store_me, open(outfile, 'wb'))
