import pandas as pd
import sys

top10={"politician": "http://www.wikidata.org/entity/Q82955", "association football player": "http://www.wikidata.org/entity/Q937857", "actor": "http://www.wikidata.org/entity/Q33999", "writer" : "http://www.wikidata.org/entity/Q36180", "painter": "http://www.wikidata.org/entity/Q1028181", "journalist": "http://www.wikidata.org/entity/Q1930187", "university teacher": "http://www.wikidata.org/entity/Q1622272", "singer": "http://www.wikidata.org/entity/Q177220", "lawyer": "http://www.wikidata.org/entity/Q40348", "composer": "http://www.wikidata.org/entity/Q36834"}

if len(sys.argv)<2 or sys.argv[1] not in top10:
    occupation='http://www.wikidata.org/entity/Q82955'
    occupation_tsv='tabular_politician_data.tsv'
else:
    occupation_tsv='tabular_%s_data.tsv' % sys.argv[1]
    occupation=top10[sys.argv[1]]

INSTANCEDIR='instance_data'

filename="%s/tabular_person_data.tsv" % INSTANCEDIR
df=pd.read_csv(filename, '\t')

new_rows=[]
for index, row in df.iterrows():
    if row['occupation']:
        if row['occupation']==occupation:
            new_rows.append(row)
        else:
            try:
                if occupation in set(row['occupation']):
                    new_rows.append(row)
            except:
                continue
print(len(new_rows))
frame=pd.DataFrame(new_rows)
frame.columns=df.columns

print('%d columns before removing NIL columns' % len(frame.columns))
frame=frame.dropna(axis=1, how='all')
print('%d columns after removing NIL columns' % len(frame.columns))

frame.to_csv('%s/%s' % (INSTANCEDIR, occupation_tsv), '\t')
#print(df['occupation'].str.contains('http://www.wikidata.org/entity/Q82955'))
