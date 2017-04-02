import pandas as pd
import sys
from collections import defaultdict

filename="instance_data/tabular_person_data.tsv"
df=pd.read_csv(filename, '\t')

print("Data frame loaded. Now iterating ...")

attributes=df.columns
nonnils=defaultdict(int)

for index, row in df.iterrows():
    for key in attributes:
        if row[key] and not pd.isnull(row[key]):
            nonnils[key]+=1
      
print(nonnils)
#print('%d non-NIL values for %s' % (c, key))

