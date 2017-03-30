import csv
import utils
import queries
import pickle
from collections import defaultdict
import time

person_ontology_uri="http://dbpedia.org/ontology/Person"
NUMATTR=50

DBPEDIADIR="dbpedia_data"
literals_file="%s/mappingbased_literals_en.ttl" % DBPEDIADIR
objects_file="%s/mappingbased_objects.ttl" % DBPEDIADIR
test_file="%s/test.ttl" % DBPEDIADIR

INSTANCEDIR="instance_data"
people_file="%s/list_of_persons.ttl" % INSTANCEDIR

person_common_attributes=queries.get_most_frequent_attributes(person_ontology_uri, NUMATTR)
all_people=pickle.load(open(people_file, 'rb'))

t1=time.time()

biggie=defaultdict(str)

previous_subj=''
subj_json={}

for input_file in [literals_file, objects_file]:
    with open(input_file, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='"')
        for row in spamreader:
            subj=row[0].lstrip('<').rstrip('>')
            #if subj not in all_people: # if this is not a person
            #    continue

            pred=row[1].lstrip('<').rstrip('>')
            if pred not in person_common_attributes: # if the attribute is not of interest
                continue

            obj=row[2].strip('.').lstrip('<').rstrip('>')
            if previous_subj: # if there has been a previous subject (any row after the first)
                if previous_subj==subj: # if the subject is still the same, just extend the json
                    subj_json[pred]=obj
                    else: # if this subject is not the same as the previous one, store the old one and start a fresh one
                        biggie[previous_subj]=subj_json
                        subj_json={}
                        subj_json[pred]=obj
                        previous_subj=subj
            else: # if this is the first row
                previous_subj=subj
                subj_json[pred]=obj
            
            #biggie[subj][pred]=obj
        
            if len(biggie)%10000:
                print('%d instances!' % len(biggie))
            
        # Add the last one too
        biggie[previous_subj]=subj_json    
        
        #input('continue?')
t2=time.time()
print(biggie)
print(t2-t1)