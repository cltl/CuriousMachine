import csv
from SPARQLWrapper import SPARQLWrapper, JSON
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict, OrderedDict
import pickle
from rdflib import Graph, RDF

import queries

sparql = SPARQLWrapper("http://sparql.fii800.lod.labs.vu.nl/sparql")

WIKIDATA_BDATE="https://www.wikidata.org/wiki/Property:P569"
WIKIDATA_DDATE="https://www.wikidata.org/wiki/Property:P570"
WIKIDATA_START_ACTIVITY=""
WIKIDATA_END_ACTIVITY=""

WIKIDATA_PEOPLE_IDS="http://www.wikidata.org/entity/Q19595382"

def infer_lifespan(myjson):
    
    if WIKIDATA_BDATE in myjson and WIKIDATA_DDATE in myjson:
        return WIKIDATA_DDATE-WIKIDATA_BDATE
    else:
        return None

def get_professional_years(myjson):
    return None

def get_first_activity_age(myjson):
    return None

def get_last_activity_age(myjson):
    return None

def infer_properties(myjson):
    lifespan=infer_lifespan(myjson) 
    proyears=get_professional_years(myjson)
    firstactivity=get_first_activity_age(myjson)
    lastactivity=get_last_activity_age(myjson)
    if lifespan:
        myjson['lifespan']=lifespan
    if proyears:
        myjson['proyears']=proyears
    if firstactivity:
        myjson['firstactivity']=firstactivity
    if lastactivity:
        myjson['lastactivity']=lastactivity
    return myjson

def normalize_url(u):
    return u.lstrip('<').rstrip('>')

def clean_and_label_relations(rels):
    newrels={}
    for r in rels:
        if not queries.check_if_instance(r.rstrip('c'), WIKIDATA_PEOPLE_IDS):
            newrels[r]=queries.get_label(r.rstrip('c')) or r
    return newrels

def extract_relations_from_files(file_list, people_set, attribute_set, outdir):
    biggies=[]
    for input_file in file_list:
        biggie=defaultdict(str)

        previous_subj=''
        subj_json={}

        with open(input_file, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='"')
            for row in spamreader:
                subj=normalize_url(row[0])
                if subj not in people_set: # if this is not a person
                    continue

                pred=normalize_url(row[1]) 
                if pred not in attribute_set: # if the attribute is not of interest
                    continue

                obj=normalize_url(row[2])
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
            
            # Add the last one too
            biggie[previous_subj]=subj_json   
            biggies.append(biggie) 
            pickle.dump(biggie, open('%s/%s.p' % (outdir, input_file.split('/')[1].split('.')[0]), 'wb'))
            print('done with %s' % input_file)
    return biggies 


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
    data=OrderedDict(sorted(d.items()))
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
   
    to_return=OrderedDict()
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

def sparql_select_one(query):
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        return result["label"]["value"]

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

