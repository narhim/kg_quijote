#Extracts proper nouns from ner parsed results and transform them into relations
f = open("ner_quijote.txt","r")
t = f.read()
print(type(t))#str