import csv
import sys
sys.path.insert(0,'..')

import utils
import queries
import pickle
from collections import defaultdict
import time

person_ontology_uri="http://www.wikidata.org/entity/Q5"
NUMATTR=50

INDIR="data"
statements_file="%s/wikidata-simple-statements.nt" % INDIR
test_file="%s/test.ttl" % INDIR

INSTANCEDIR="instance_data"
people_file="%s/list_of_persons.p" % INSTANCEDIR

person_common_attributes=queries.get_most_frequent_attributes(person_ontology_uri, NUMATTR)
all_people=set(pickle.load(open(people_file, 'rb')))
print(len(all_people))
print(person_common_attributes)

t1=time.time()

"""
for input_file in [literals_file, objects_file]:
    biggie=defaultdict(str)

    previous_subj=''
    subj_json={}

    with open(input_file, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='"')
        for row in spamreader:
            subj=row[0].lstrip('<').rstrip('>')
            if subj not in all_people: # if this is not a person
                continue

            pred=row[1].lstrip('<').rstrip('>')
            if pred not in person_common_attributes: # if the attribute is not of interest
                continue

            obj=row[2].strip('.').lstrip('<').rstrip('>')
            if previous_subj: # if there has been a previous subject (any row after the first)
                if previous_subj==subj: # if the subject is still the same, just extend the json
                    if pred not in subj_json:
                        subj_json[pred]=obj
                    else:
                        if not isinstance(subj_json[pred], set):
                            tmp=subj_json[pred]
                            subj_json[pred]=set()
                            subj_json[pred].add(tmp)    
                        subj_json[pred].add(obj)
                else: # if this subject is not the same as the previous one, store the old one and start a fresh one
                    biggie[previous_subj]=subj_json
                    subj_json={}
                    if pred not in subj_json:
                        subj_json[pred]=obj
                    else:
                        if not isinstance(subj_json[pred], set):
                            tmp=subj_json[pred]
                            subj_json[pred]=set()
                            subj_json[pred].add(tmp)
                        subj_json[pred].add(obj)

                    previous_subj=subj

                    if len(biggie)%50000==0:
                        print('%d instances!' % len(biggie))
            
            else: # if this is the first row
                previous_subj=subj
                subj_json[pred]=obj
            
            #biggie[subj][pred]=obj
        
        # Add the last one too
        biggie[previous_subj]=subj_json    
        pickle.dump(biggie, open('%s/%s.p' % (INSTANCEDIR, input_file.split('/')[1].split('.')[0]), 'wb'))
        print('done with %s' % input_file)
        #input('continue?')
"""
t2=time.time()
#print(biggie)
print(t2-t1)
print('DONE')
