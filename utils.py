import csv
from SPARQLWrapper import SPARQLWrapper, JSON
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict, OrderedDict
import pickle
from rdflib import Graph, RDF, Literal
from dateutil import parser
import sys
import queries

sparql = SPARQLWrapper("http://sparql.fii800.lod.labs.vu.nl/sparql")

WIKIDATA_BDATE="http://www.wikidata.org/entity/P569c"
WIKIDATA_DDATE="http://www.wikidata.org/entity/P570c"
WIKIDATA_START_ACTIVITY="http://www.wikidata.org/entity/P2031c"
WIKIDATA_END_ACTIVITY="http://www.wikidata.org/entity/P2032c"

WIKIDATA_IDS="http://www.wikidata.org/entity/Q19847637"
WIKIDATA_PEOPLE_IDS="http://www.wikidata.org/entity/Q19595382"

"""
def parse_date_literal(l):
#    print(l)
    cleanl=l.replace('^^<http://www.w3.org/2001/XMLSchema#date', '').replace('^^<http://www.w3.org/2001/XMLSchema#gYearMonth', '').replace('^^<http://www.w3.org/2001/XMLSchema#gYear', '')
    try:
        return parser.parse(cleanl).year
    except ValueError:
        return int(cleanl[:4])
"""
def sets_to_dates(myjson):
    for attr in [WIKIDATA_BDATE, WIKIDATA_DDATE]:
        if attr in myjson and isinstance(myjson[attr], set):
            myjson[attr]=myjson[attr].pop()
    return myjson
         

def infer_lifespan(myjson, key):    
    if WIKIDATA_BDATE in myjson and WIKIDATA_DDATE in myjson:
        if not isinstance(myjson[WIKIDATA_DDATE], set) and not isinstance(myjson[WIKIDATA_BDATE], set):
            try:
                return myjson[WIKIDATA_DDATE].year-myjson[WIKIDATA_BDATE].year
            except:
                print(myjson[WIKIDATA_DDATE], myjson[WIKIDATA_BDATE])
                sys.exit(-1)
        else:
            print(key, myjson[WIKIDATA_DDATE], myjson[WIKIDATA_BDATE], "SET")
    else:
        return ""

def get_professional_years(myjson):
    if WIKIDATA_START_ACTIVITY in myjson and WIKIDATA_END_ACTIVITY in myjson:
        if not isinstance(myjson[WIKIDATA_START_ACTIVITY], set) and not isinstance(myjson[WIKIDATA_END_ACTIVITY], set):
            return myjson[WIKIDATA_END_ACTIVITY].year-myjson[WIKIDATA_START_ACTIVITY].year
    else:
        return ""

def get_first_activity_age(myjson):
    if WIKIDATA_BDATE in myjson and WIKIDATA_START_ACTIVITY in myjson:
        if not isinstance(myjson[WIKIDATA_START_ACTIVITY], set) and not isinstance(myjson[WIKIDATA_BDATE], set):
            return myjson[WIKIDATA_START_ACTIVITY].year-myjson[WIKIDATA_BDATE].year
    else:
        return ""

def get_last_activity_age(myjson):
    if WIKIDATA_END_ACTIVITY in myjson and WIKIDATA_DDATE in myjson:
        if not isinstance(myjson[WIKIDATA_DDATE], set) and not isinstance(myjson[WIKIDATA_END_ACTIVITY], set):
            return myjson[WIKIDATA_DDATE].year-myjson[WIKIDATA_END_ACTIVITY].year
    else:
        return ""

def infer_properties(myjson, key):
    lifespan=infer_lifespan(myjson, key) 
    proyears=get_professional_years(myjson)
    firstactivity=get_first_activity_age(myjson)
    lastactivity=get_last_activity_age(myjson)
    inferred_data=[lifespan, proyears, firstactivity, lastactivity]
    return inferred_data

def normalize_freebase(fb1):
    return fb1.replace("http://rdf.freebase.com/ns/m.", "/m/")

def normalize_url(u):
    return u.lstrip('<').rstrip('>')

def clean_and_label_relations(rels):
    newrels={}
    for r in rels:
        if not queries.check_if_instance(r.rstrip('c'), WIKIDATA_PEOPLE_IDS) and not queries.check_instance_or_subclass(r.rstrip('c'), WIKIDATA_IDS):
            newrels[r]=queries.get_label(r.rstrip('c')) or r
    return newrels

def normalize_numeric(o):
    if "^^<http://www.w3.org/2001/XMLSchema#decimal>" in o:
        o=float(o.replace("^^<http://www.w3.org/2001/XMLSchema#decimal>", ""))
    return o

def normalize_date(o):
    if '^^<http://www.w3.org/2001/XMLSchema#date>' in o or '^^<http://www.w3.org/2001/XMLSchema#gYearMonth>' in o or '^^<http://www.w3.org/2001/XMLSchema#gYear>' in o:
        clean_date=o.replace('^^<http://www.w3.org/2001/XMLSchema#date>', '').replace('^^<http://www.w3.org/2001/XMLSchema#gYearMonth>', '').replace('^^<http://www.w3.org/2001/XMLSchema#gYear>', '')
        try:
            return parser.parse(clean_date)
        except ValueError:
            print("Date not correct and can not be parsed: %s" % clean_date)
            return None
#parser.parse(clean_date[:4])
    else:
        return o

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

                obj=normalize_numeric(row[2])
                if not isinstance(obj, float):
                    obj=normalize_date(obj)
                if obj==row[2]:
                    obj=normalize_url(obj)
                if obj is None:
                    continue
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

