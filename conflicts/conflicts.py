

def pos_ner_conflicts():
	return None

def srl_ner_conflicts():
	return None

def coref_el_conflicts(entities):
	conflicts=[]
	for e1 in entities:
		for e2 in entities:
			if e1.chain != e2.chain and e1.meaning == e2.meaning:
				c=Conflict(desc="Same meaning, different coreferential chain", actors=[e1,e2])
				conflicts.append(c)
			elif e1.chain == e2.chain and e1.meaning != e2.meaning:
				c=Conflict(desc="Different meaning, same coreferential chain", actors=[e1,e2])
				conflicts.append(c)
	return conflicts

def typing_el_conflicts():
	return None

def cross_system_conflicts(entity_set1, entity_set2):
	return None


