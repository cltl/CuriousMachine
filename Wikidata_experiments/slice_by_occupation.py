import pandas as pd

filename="instance_data/tabular_person_data.tsv"
df=pd.read_csv(filename, '\t')

occupation='http://www.wikidata.org/entity/Q82955'

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
frame.columns=header
#print(df['occupation'].str.contains('http://www.wikidata.org/entity/Q82955'))
