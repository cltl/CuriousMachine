import pickle

import pandas as pd

INSTANCEDIR='instance_data'
try:
    vectors=pickle.load(open('%s/freebase_vectors.p' % INSTANCEDIR, 'rb'))
except:
    freebase_txt="%s/freebase/test-freebase.txt" % INSTANCEDIR
    filename="%s/tabular_person_data.tsv" % INSTANCEDIR
    df=pd.read_csv(filename, '\t')

    freebase_attr="http://www.wikidata.org/entity/P646-freebase"

    freebase_people_uris=[row[freebase_attr] for index, row in df.iterrows() if not pd.isnull(row[freebase_attr])]
    print(len(freebase_people_uris))

    vector_json={}
    with open(freebase_txt , 'r') as freebase_raw_file:
        for line in freebase_raw_file:
            fid, *numbers=line.split()
            if len(numbers)>10 and fid in freebase_people_uris:
                vector_json[fid]=numbers

    pickle.dump(vector_json, open('%s/freebase_vectors.p' % INSTANCEDIR, 'wb'))
            
