import sys
sys.path.insert(0,'..')

import utils
import queries
import pickle
import time

person_ontology_uri="http://www.wikidata.org/entity/Q5"
NUMATTR=100

INDIR="data"
statements_file="%s/wikidata-simple-statements.nt" % INDIR
test_file="%s/test.ttl" % INDIR

INSTANCEDIR="instance_data"
people_file="%s/list_of_persons.p" % INSTANCEDIR

person_common_attributes=queries.get_most_frequent_attributes(person_ontology_uri, NUMATTR)
clean_attributes=utils.clean_and_label_relations(person_common_attributes)

all_people=set(pickle.load(open(people_file, 'rb')))
print(len(all_people))
print(clean_attributes.values())

t1=time.time()

files=[statements_file]
utils.extract_relations_from_files(files, all_people, clean_attributes.keys(), INSTANCEDIR)

t2=time.time()
#print(biggie)
print(t2-t1)
print('DONE')
