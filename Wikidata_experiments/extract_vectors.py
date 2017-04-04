import pickle

import pandas as pd

def normalize_freebase(fb1):
    return fb1.replace("http://rdf.freebase.com/ns/m.", "/m/")

INSTANCEDIR='instance_data'
freebase_txt="%s/freebase-skipgram1000.txt" % INSTANCEDIR
#freebase_txt="%s/freebase/test-freebase.txt" % INSTANCEDIR
filename="%s/tabular_person_data.tsv" % INSTANCEDIR
df=pd.read_csv(filename, '\t')

freebase_attr="http://www.wikidata.org/entity/P646-freebase"


try:
    vector_json=pickle.load(open('%s/freebase_vectors.p' % INSTANCEDIR, 'rb'))
except:

    freebase_people_uris=[normalize_freebase(row[freebase_attr]) for index, row in df.iterrows() if not pd.isnull(row[freebase_attr])]
    #print(len(freebase_people_uris))
    print(freebase_people_uris)
    vector_json={}
    with open(freebase_txt , 'r') as freebase_raw_file:
        for line in freebase_raw_file:
            fid, *numbers=line.split()
    #        print(len(numbers))
            if len(numbers)>10 and fid in freebase_people_uris:
                numbers=list(map(int, numbers))
                vector_json[fid]=numbers

    pickle.dump(vector_json, open('%s/freebase_vectors.p' % INSTANCEDIR, 'wb'))
        
df['embeddings']="" 
for index, row in df.iterrows():
    if not pd.isnull(row[freebase_attr]) and normalize_freebase(row[freebase_attr]) in vector_json:
        row['embeddings']=vector_json[normalize_freebase(row[freebase_attr])]
        print('added a vector')

df.to_csv('%s/tabular_person_data.tsv' % INSTANCEDIR, '\t')
        

