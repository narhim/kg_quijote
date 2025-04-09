import re
import spacy
#Read file with entities, build into dict with entity as key and filter out
ent_rel_dict = {}
with open("ner_quijote_hg.txt","r") as f:
	for line in f:
		#Separate relation from entity
		elements = re.split("\t",line)
		entity = elements[1].strip("\n")
		relation = elements[0]
		#Filter out len<4. Filters out "Cid"
		if len(entity) >3:
			ent_rel_dict[entity] = relation
#Lemmatization			 
