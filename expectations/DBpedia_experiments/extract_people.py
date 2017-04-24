from rdflib.namespace import Namespace
import sys
sys.path.insert(0,'..')

import utils 

DBPEDIADIR="data"
ontology_file="%s/instance_types_en.ttl" % DBPEDIADIR

INSTANCEDIR="instance_data"
people_file="%s/list_of_persons.p" % INSTANCEDIR

DBO = Namespace('http://dbpedia.org/ontology/')
PERSON=DBO.Person

utils.extract_all_dudes(PERSON, ontology_file, people_file)

############# The rest should be general enough ##############
