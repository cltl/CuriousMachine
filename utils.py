from SPARQLWrapper import SPARQLWrapper, JSON
import matplotlib.pyplot as plt
import numpy as np
import collections
import pickle
from rdflib import Graph, RDF

sparql = SPARQLWrapper("http://sparql.fii800.lod.labs.vu.nl/sparql")

def extract_all_dudes(persontype, infile, outfile):

    g=Graph()
    print("Graph loading...")
    g.parse(infile, format='nt')
    all_people=set()
    print("Graph loaded")
    for person in g.subjects(RDF.type, persontype):
        all_people.add(person.toPython())
        #input('continue')

    pickle.dump(all_people, open(outfile, 'wb'))

def make_storable(url):
    return url.split('/')[-1]

def remove_outliers(indata, m = 1.5):
    if not len(indata):
        return indata
    if len(indata)==1:
        return indata
    data=np.array(indata)
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else 0.
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
        try:
            if int(result["agg"]["value"])>=0:
                to_return[int(result["agg"]["value"])]=int(result["cnt"]["value"])
        except:
            to_return[result["agg"]["value"]]=int(result["cnt"]["value"])
    return to_return

def sparql_set(query):
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
   
    to_return=set()
    for result in results["results"]["bindings"]:
            to_return.add(result["agg"]["value"])
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

