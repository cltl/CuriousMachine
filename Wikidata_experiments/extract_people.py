from rdflib.namespace import Namespace
import sys
sys.path.insert(0,'..')

import utils 

INDIR="data"
ontology_file="%s/wikidata-instances.nt" % INDIR

INSTANCEDIR="instance_data"
people_file="%s/list_of_persons.p" % INSTANCEDIR

WKD = Namespace('http://www.wikidata.org/entity/')
PERSON=WKD.Q5

utils.extract_all_dudes(PERSON, ontology_file, people_file)

############# The rest should be general enough ##############
