import utils
import conflicts
import classes

from KafNafParserPy import *
import glob
import sys
import pickle
from collections import defaultdict

PATH="../data/aida/naf_processed/"
ANNOTATOR='dbp'
TRAIN_DEV_FOLDER='traindev/'
TESTA_FOLDER='testa/'
TESTB_FOLDER='testb/'

topics_pickle=pickle.load(open('../data/aida/topics.pickle', 'rb'))

only_sports=False

title_distribution=defaultdict(int)

if __name__=="__main__":
	entities_with_tmx={'PER':0, 'MISC':0, 'ORG':0, 'LOC':0}
	all_entities={'PER':0, 'MISC':0, 'ORG':0, 'LOC':0}
	cnt_files=0
	for f in glob.glob(PATH + TRAIN_DEV_FOLDER + '*.naf'):
		filename=f.split('/')[-1][:-4]
		topic=topics_pickle[filename]
		if only_sports and topic['Low']!='SPORTS':
			continue
		title_distribution[topic['title']]+=1
		parser=KafNafParser(f)
		utils.terms_to_tokens(parser, ['t2', 't3'])
		all_chains=utils.get_coref_chains(parser.get_corefs())
		all_tmxs=utils.get_tmxs(parser.get_timeExpressions())
		for entity in parser.get_entities():
			t=entity.get_type()
			terms=utils.get_entity_terms(entity)
			tokens=utils.terms_to_tokens(parser, terms)
			tmxs=utils.get_entity_tmx_from_srl(parser, tokens, all_tmxs, parser.get_predicates())
			entity_chains=utils.get_entity_chain(terms, all_chains)
			disambiguation=utils.get_most_confident_link(entity, ANNOTATOR)
			ent_obj = classes.EntityMention(terms=terms, tokens=tokens, tmxs=tmxs, chains=entity_chains, meaning=disambiguation, the_type=t)
			# print(terms, [one_tmx.value for one_tmx in entity_tmxs])
			if t:
				all_entities[t]+=1
				if len(tmxs):
					entities_with_tmx[t]+=1
		cnt_files+=1
		print(cnt_files, entities_with_tmx, all_entities)
#	print(title_distribution)
