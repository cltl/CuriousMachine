import pickle
from rdflib import Graph, RDF
from rdflib.namespace import Namespace

DBPEDIADIR="dbpedia_data"
ontology_file="%s/instance_types.ttl" % DBPEDIADIR

INSTANCEDIR="instance_data"
people_file="%s/list_of_persons.p" % INSTANCEDIR

DBO = Namespace('http://dbpedia.org/ontology/')

g=Graph()
g.parse(ontology_file, format='nt')
all_people=set()

for person in g.subjects(RDF.type, DBO.Person):
    print(person)
    all_people.add(person)
    #input('continue')

pickle.dump(all_people, open(people_file, 'wb'))