import utils
import conflicts

from KafNafParserPy import *
import glob

PATH="../data/aida/naf_processed/"
ANNOTATOR='dbp'
TRAIN_DEV_FOLDER='traindev/'
TESTA_FOLDER='testa/'
TESTB_FOLDER='testb/'
if __name__=="__main__":

	for f in glob.glob(PATH + TRAIN_DEV_FOLDER + '*.naf'):
		parser=KafNafParser(f)
		for entity in parser.get_entities():
			t=entity.get_type()
			terms=utils.get_entity_terms(entity)
			disambiguation=utils.get_most_confident_link(entity, ANNOTATOR)
			print(t, terms, disambiguation)
