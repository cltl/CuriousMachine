from KafNafParserPy import *

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
