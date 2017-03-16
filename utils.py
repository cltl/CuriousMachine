from SPARQLWrapper import SPARQLWrapper, JSON
import matplotlib.pyplot as plt
import numpy as np
import collections

sparql = SPARQLWrapper("http://sparql.fii800.lod.labs.vu.nl/sparql")

def remove_outliers(data, m = 1.5):
    if not len(data):
        return data
    if len(data)==1:
        return data
    data=np.array(data)
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else 0.
    print(data)
    return data[s<m]

def plot_me(d): # plot a dictionary with counts
    data=collections.OrderedDict(sorted(d.items()))
    keys=data.keys()
    values=data.values()
    indexes = np.arange(len(keys))

    width = 1

    plt.bar(indexes, values, width)
    plt.xticks(indexes + width * 0.5, keys)
    plt.show()

def sparql_aggregate(query):
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
   
    to_return=collections.OrderedDict()
    for result in results["results"]["bindings"]:
        if int(result["agg"]["value"])>=0:
            to_return[int(result["agg"]["value"])]=int(result["cnt"]["value"])
    return to_return

def sparql_ask_query(query):
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return results['boolean']

def dict_to_list(d):
    d_as_list=[]
    for element in d.keys():
        cnt=0
        while cnt<d[element]:
            d_as_list.append(element)
            cnt+=1
    return d_as_list

def log_attr_data(t, data):
    try:
        if len(data):
            print(t, data[0], '-', data[-1])
        else:
            print(t, 'UNKNOWN')
    except:
        print(t, 'UNKNOWN')

