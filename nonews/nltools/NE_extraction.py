'''
Created on 14 Nov 2012

@author: matt
'''
import nltk
from nltk.book import text7, FreqDist


#text7 is the new york times articles
print '\tPOS Tagging...'
tagged=nltk.pos_tag(text7)
print '\tNE chunking...'
chunks=nltk.ne_chunk(tagged,binary=True)
ne_chunks=[]
print '\tNE chunk filtering...'
for chunk in chunks:
    if type(chunk) is nltk.Tree:
        ne_chunks.append(chunk)

print '\tExtracting NE\'s...'
all_nes=[ " ".join([ ne_leaf[0] for ne_leaf in ne_chunk.flatten().leaves() ]) for ne_chunk in ne_chunks ]
uniq_nes=set(all_nes)
uniq_nes_L=list(uniq_nes)
uniq_nes_L.sort()
for ne in uniq_nes_L:
    print ne

FreqDist(all_nes).plot(50)