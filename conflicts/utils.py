from KafNafParserPy import *
from dateutil import parser
import classes

def get_entity_terms(entity):
	for ref in entity.get_references():
		terms=ref.get_span().get_span_ids()
	return terms

def get_most_confident_link(e, annotator):
	maxconf=-0.1
	maxref=None
	for ref in e.get_external_references():
		try:
			if ref.get_resource()==annotator and float(ref.get_confidence())>maxconf:
				maxconf=float(ref.get_confidence())
				maxref=ref.get_reference()
		except:
			maxref=None
			break
	return maxref

def get_entity_tmx_from_srl(parser, terms, all_tmxs, predicates):
	entity_tmxs=set()
	for pred in predicates:
		ts=set()
		entity_found=False
		for role in pred.get_roles():
			span_ids=terms_to_tokens(parser, role.get_span().get_span_ids())
			if role.get_sem_role()=='AM-TMP':
				for a_tmx in all_tmxs:
					if a_tmx.spans.issubset(span_ids):
						ts.add(a_tmx)
			elif terms.issubset(span_ids):
				entity_found=True
		if entity_found and len(ts)>0:
			entity_tmxs |= ts
	return entity_tmxs

def terms_to_tokens(parser, terms):
	tokens=set()
	for t in terms:
		tokens |= set(parser.get_term(t).get_span().get_span_ids())
	return tokens

def get_tmxs(naf_tmxs):
	tmxs=set()
	for tmx in naf_tmxs:
		if tmx.get_span():
			try:
				t_obj=classes.Tmx(id=tmx.get_id(), value=parser.parse(tmx.get_value()), spans=set(tmx.get_span().get_span_ids()))
				tmxs.add(t_obj)
			except:
				continue
	return tmxs

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
