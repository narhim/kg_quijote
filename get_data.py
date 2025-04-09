
import requests
from bs4 import BeautifulSoup
import re
from unidecode import unidecode
import operator

def split_text(texto_lista,lista):
	for c in texto_lista:
		p = re.split('[.]|[?]|[!]|[\)]',c) #Sentence breaker
		for s in p:
			sen = re.split(",|;|:",s)#Phrase breaker
			for ph in sen:
				ws = re.split(" ",ph)#Word splitter
				for w in ws:
					if re.search("¿|-|¡|\(",w):
						w = re.split("¿|-|¡|\(",w)[-1]
					if re.search("—",w):
						if re.match("—",w):
							try:
								w = re.split("—",w)[-1]
							except:
								continue
						else:
							w = re.split("—",w)[0]
					if re.search("\r",w):
						s = re.split("\r",w)
						lista.append(s[0].lower())
						lista.append(s[1].lower())

					elif len(w) >= 1:
						lista.append(unidecode(w.lower()))
	lista = [w.strip('<*') for w in lista]
	lista = [w.strip('>*') for w in lista]
	lista = [w.strip('\n') for w in lista if len(w)>1]
	lista = [w.strip('\'*') for w in lista]
	lista = [w.strip('»') for w in lista]
	lista = [w.strip('«') for w in lista]
	lista = [w.strip('\"') for w in lista if len(w)>1]	
	return lista
def freq_sort(list_ngrams):
	freq_tokens = {}
	for t in list_ngrams:
		if t in freq_tokens:
			freq_tokens[t] += 1
		else:
			freq_tokens[t] = 1
	sorted_freq_tokens = sorted(freq_tokens.items(), key=operator.itemgetter(1))
	sorted_freq_tokens.reverse()
	dict_sort_freq = {}
	for t in sorted_freq_tokens:
		dict_sort_freq[t[0]] = t[1]
	return dict_sort_freq
def write_freq(name,dictionary):
	f = open(name,"w")
	for k,v in dictionary.items():
		f.write(str(k) + "\t" + str(v) + "\n")
#Preprocessing
url = "https://www.gutenberg.org/cache/epub/2000/pg2000-images.html"
rget = requests.get(url)
soup = BeautifulSoup(rget.text, "lxml")
section_titles_raw = soup.findAll("h2")
section_titles = [t.text for t in section_titles_raw[2:-1]]
chapters_raw = soup.findAll("h3")
chapters = [t.text for t in chapters_raw[6:]]#Capítulo I
paragraphs_raw = soup.findAll("p")
paragraphs = [t.text for t in paragraphs_raw[65:]]#Comienza "En un lugar de la Mancha..."
#1-grams
titles = []
titles = split_text(chapters,titles)
text = []
text = split_text(paragraphs,text)
tokens = titles + text
freq_tokens = freq_sort(tokens)
write_freq("freq_tokens.tsv",freq_tokens)
#2-grams
bigrams = [(t,tokens[n+1]) for n,t in enumerate(tokens[:-1])]#build
freq_bigrams = freq_sort(bigrams)
write_freq("freq_bigrams.tsv",freq_bigrams)
#3-grams
trigrams = [(t,tokens[n+1],tokens[n+2]) for n,t in enumerate(tokens[:-2])]#build
freq_trigrams = freq_sort(trigrams)
write_freq("freq_trigrams.tsv",freq_trigrams)
#4-grams
tetragrams = [(t,tokens[n+1],tokens[n+2],tokens[n+3]) for n,t in enumerate(tokens[:-3])]#build
freq_tetragrams = freq_sort(tetragrams)
write_freq("freq_tetragrams.tsv",freq_tetragrams)
#5-grams
pentagrams = [(t,tokens[n+1],tokens[n+2],tokens[n+3],tokens[n+4]) for n,t in enumerate(tokens[:-4])]#build
freq_pentagrams = freq_sort(pentagrams)
write_freq("freq_pentagrams.tsv",freq_pentagrams)
#Write raw text for NER
f = open("quijote.txt","w")
for p in paragraphs:
	f.write(p + "\n")