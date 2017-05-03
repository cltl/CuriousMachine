from KafNafParserPy import *

def get_entity_terms(entity):
	for ref in entity.get_references():
		terms=ref.get_span().get_span_ids()
	return terms

def get_most_confident_link(e, annotator):
	maxconf=-0.1
	maxref=None
	print(annotator)
	for ref in e.get_external_references():
		try:
			if ref.get_resource()==annotator and float(ref.get_confidence())>maxconf:
				maxconf=float(ref.get_confidence())
				maxref=ref.get_reference()
		except:
			maxref=None
			break
	return maxref

def get_coref_chains(corefs):
	chains={}
	for c in corefs:
		if c.get_type() !='event':
			chains[c.get_id()]=[s.get_span_ids() for s in c.get_spans()]
			#print(c.get_id(), c.get_type(), [s.get_span_ids() for s in c.get_spans()])
	return chains

def get_entity_chain(terms, chains):
	my_chains=set()
	for cid, termslist in chains.items():
		if terms in termslist:
			my_chains.add(cid)
	return my_chains
