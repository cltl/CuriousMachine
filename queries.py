
import utils

def get_most_frequent_attributes(a_type, how_much=10):

    query="""
    SELECT ?agg
        WHERE {
        ?entity a <%s> ;
        ?agg ?value
        } GROUP BY ?agg
         ORDER BY DESC(COUNT(?entity))
        LIMIT %d
    """ % (a_type, how_much)
    return utils.sparql_set(query)

def get_label(rel):
    query="""
    SELECT ?label
    WHERE {
        <%s> rdfs:label ?label .
        FILTER(lang(?label)='en')
    } LIMIT 1
    """ % rel
    return utils.sparql_select_one(query)

def check_if_instance(i1, c1):
    query="""
    ASK WHERE {
        <%s> <http://www.wikidata.org/entity/P31s> ?c .
        ?c <http://www.wikidata.org/entity/P31v> <%s> . 
    } 
    """ % (i1, c1)
    return utils.sparql_ask_query(query)

def check_if_subtype(c1, c2):
    query="""
    ASK WHERE {
        <%s> rdfs:subClassOf* <%s>
    } 
    """ % (c1, c2)
    return utils.sparql_ask_query(query)

def check_instance_or_subclass(i1, c2):
    query="""
    ASK WHERE {
        <%s> <http://www.wikidata.org/entity/P31s> ?c .
        ?c <http://www.wikidata.org/entity/P31v> ?c2 . 
        ?c2 <http://www.wikidata.org/entity/P279c> <%s>
    }
    """ % (i1, c2)
    return utils.sparql_ask_query(query)

# Get distribution for a random attribute of a type
def get_dist_for_type_attribute(a_type, attr):
    query="""
    SELECT ?agg count(?entity) as ?cnt
        WHERE {
        ?entity a <%s> ;
         <%s> ?agg
        } GROUP BY ?agg
        ORDER BY (?cnt)
    """ % (a_type, attr)

    return utils.sparql_aggregate(query)

# Lifespan for dead people
def get_lifespan_for_type_dbpedia(a_type):
    query="""
    SELECT ?agg count(?entity) as ?cnt
        WHERE {
        ?entity a <%s> ;
         <http://dbpedia.org/property/birthDate> ?birthdate ;
         <http://dbpedia.org/property/deathDate> ?deathdate .
        filter (datatype(?birthdate) = xsd:date) .
        filter (datatype(?deathdate) = xsd:date) .
        bind( year(?deathdate)-year(?birthdate) as ?agg )
        } GROUP BY ?agg
        ORDER BY (?agg)
    """ % (a_type)

    return utils.sparql_aggregate(query)

# Active ages
def get_active_ages_for_type_dbpedia(a_type):
    query="""
    SELECT ?agg count(?entity) as ?cnt
        WHERE {
        ?entity a <%s> ;
        <http://dbpedia.org/ontology/activeYearsStartYear> ?birthdate ;
        <http://dbpedia.org/ontology/activeYearsEndYear> ?deathdate .
        bind( year(?deathdate)-year(?birthdate) as ?agg )
        } GROUP BY ?agg
        ORDER BY (?agg)
    """ % (a_type)

    return utils.sparql_aggregate(query)


# age of first activity
def get_age_of_first_activity_dbpedia(a_type):
    query="""
    SELECT ?agg count(?entity) as ?cnt
        WHERE {
        ?entity a <%s> ;
        <http://dbpedia.org/property/birthDate> ?birthdate ;
        <http://dbpedia.org/ontology/activeYearsStartYear> ?startdate .
        filter (datatype(?birthdate) = xsd:date) .
        bind( year(?startdate)-year(?birthdate) as ?agg ) .
        } GROUP BY ?agg
        ORDER BY (?agg)
    """ % (a_type)

    return utils.sparql_aggregate(query)


# age of last activity
def get_age_of_last_activity_dbpedia(a_type):
    query="""
    SELECT ?agg count(?entity) as ?cnt
        WHERE {
        ?entity a <%s> ;
        <http://dbpedia.org/property/birthDate> ?birthdate ;
        <http://dbpedia.org/ontology/activeYearsEndYear> ?enddate .
        filter (datatype(?birthdate) = xsd:date) .
        bind( year(?enddate)-year(?birthdate) as ?agg ) .
        } GROUP BY ?agg
        ORDER BY (?agg)
    """ % (a_type)

    return utils.sparql_aggregate(query)
