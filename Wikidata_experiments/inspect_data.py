import pandas as pd
import sys
from collections import defaultdict

filename="instance_data/tabular_person_data.tsv"
df=pd.read_csv(filename, '\t')

print("Data frame loaded. Now iterating ...")

def count_non_nils():
    attributes=df.columns
    nonnils=defaultdict(int)

    for index, row in df.iterrows():
        for key in attributes:
            if row[key] and not pd.isnull(row[key]):
                nonnils[key]+=1
      
    print(nonnils)
#print('%d non-NIL values for %s' % (c, key))

def infer_types(frame, t):
    d=frame.select_dtypes(include=[t]).head()
    print(d)
    return d

def inspect_dates(df):
    dob="date of birth"
    dod="date of death"
    attr=[dob,dod]
    c=0
    for index, row in df.iterrows():
        for a in attr:
            if not pd.isnull(row[a]) and isinstance(row[a], set):
                print(row['instance uri'], a, row[a])
                c+=1
    print("%d sets in the data for date types" % c)

def inspect_field(df, indexes):
    fields=[]
    for i in indexes:
        fields.append(df.columns[i])

#    df[fields] = df[fields].apply(pd.to_numeric, errors='coerce')

    print(fields)
    c=0
    for index, row in df.iterrows():
        for field in fields:
            if not pd.isnull(row[field]) and not isinstance(row[field], float):
                print(row['instance uri'], field, row[field], type(row[field]))
                c+=1
    print("%d non-floats" % (c))

#infer_types(df, 'str')
count_non_nils()
#inspect_field(df, [8,37])
#inspect_dates(df)
