class EntityMention:
    """
    class containing information about an entity mention
    """
    def __init__(self, mention="", 
                 terms=[], meaning=None,
		 the_type=None, sentence=None, chains=set()):
        self.sentence = sentence         # e.g. 4 -> which sentence is the entity mentioned in
        self.mention = mention           # e.g. "John Smith" -> the mention of an entity as found in text
        self.the_type = the_type         # e.g. "Person" | "http://dbpedia.org/ontology/Person"
        self.terms = terms		 # e.g. ["t1", "t2"]
        self.meaning = meaning           # e.g. "http://dbpedia.org/resource/France"
        self.chain = chain               # e.g. {'co3'}

class Conflict:
    """
    class describing a conflict
    """
    def __init___(self, desc="", actors=[]):
        self.desc = desc                   # e.g. "Different meaning, same coreferential chain"
        self.actors = actors               # e.g. [entity1, entity2]
