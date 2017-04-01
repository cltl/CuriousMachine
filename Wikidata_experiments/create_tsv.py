import pickle
import sys
sys.path.insert(0,'..')

import queries
import utils
import pandas as pd

person_ontology_uri="http://www.wikidata.org/entity/Q5"
NUMATTR=100

INDIR='data'
INSTANCEDIR='instance_data'
TSVFILENAME='tabular_person_data.tsv'

statements_file="%s/wikidata-simple-statements.nt" % INDIR

people_file="%s/list_of_persons.p" % INSTANCEDIR
all_people=set(pickle.load(open(people_file, 'rb')))

person_common_attributes=queries.get_most_frequent_attributes(person_ontology_uri, NUMATTR)
clean_attributes=utils.clean_and_label_relations(person_common_attributes)

header=clean_attributes.values()

files=[statements_file]
try:
    people_data=pickle.load(open('%s/wikidata-simple-statements.p' % INSTANCEDIR, 'rb'))
except:
    people_datas=utils.extract_relations_from_files(files, all_people, clean_attributes.keys(), INSTANCEDIR)
    people_data=people_datas[0]


people_for_pandas=[]
for person_uri in people_data:
    person_from_json=people_data[person_uri]
    person_for_pandas=[]
    for attruri, attrlabel in clean_attributes.items():
        if attruri in person_from_json:
            person_for_pandas.append(person_from_json[attruri])
        else:
            person_for_pandas.append("")
    people_for_pandas.append(person_for_pandas)

frame=pd.DataFrame(people_for_pandas)
frame.columns=header

for i, row in frame.iterrows():
    print(row['occupation'])
    print(row['religion'])

frame.to_csv('%s/%s' % (INSTANCEDIR, TSVFILENAME), '\t')

