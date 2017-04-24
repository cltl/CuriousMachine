import sys
sys.path.insert(0,'..')

import utils
import queries
import pickle
import time

person_ontology_uri="http://dbpedia.org/ontology/Person"
NUMATTR=200

DBPEDIADIR="data"
literals_file="%s/mappingbased_literals_en.ttl" % DBPEDIADIR
objects_file="%s/mappingbased_objects_en.ttl" % DBPEDIADIR
test_file="%s/test.ttl" % DBPEDIADIR

INSTANCEDIR="instance_data"
people_file="%s/list_of_persons.p" % INSTANCEDIR

person_common_attributes=queries.get_most_frequent_attributes(person_ontology_uri, NUMATTR)
all_people=set(pickle.load(open(people_file, 'rb')))
print(len(all_people))

t1=time.time()

files=[literals_file, objects_file]
utils.extract_relations_from_files(files, all_people, person_common_attributes, INSTANCEDIR)

t2=time.time()
print(t2-t1)
print('DONE')
