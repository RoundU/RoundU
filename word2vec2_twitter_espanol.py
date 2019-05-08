# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 18:47:20 2017
@author: sergio
"""
from numpy import  zeros, float32 as REAL
from gensim.models import keyedvectors
import codecs

# this function was build using code excerpts from:
# https://github.com/RaRe-Technologies/gensim/blob/develop/gensim/models/keyedvectors.py
def load_vectors_from_csv(fname,vocab_size=973265,vector_size=100):
    print("Loading vectors from file:",fname)
    result=keyedvectors.KeyedVectors()
    result.syn0 = zeros((vocab_size, vector_size), dtype=REAL)
    result.vecor_size=vector_size
    counts=None   
    def add_word(word, weights):
        word_id = len(result.vocab)
        if word in result.vocab:
            print("duplicate word '%s' in %s, ignoring all but first", word, fname)
            return
        if counts is None:
            # most common scenario: no vocab file given. just make up some bogus counts, in descending order
            result.vocab[word] = keyedvectors.Vocab(index=word_id, count=vocab_size - word_id)
        elif word in counts:
            # use count from the vocab file
            result.vocab[word] = keyedvectors.Vocab(index=word_id, count=counts[word])
        else:
            # vocab file given, but word is missing -- set count to None (TODO: or raise?)
            print("vocabulary file is incomplete: '%s' is missing", word)
            result.vocab[word] = keyedvectors.Vocab(index=word_id, count=None)
        result.syn0[word_id] = weights
        result.index2word.append(word)   
    file=codecs.open(fname,"r","utf-8")
    i=0
    for line in file:
        i+=1
        if i==1: #ommit header
            continue
        parts=line.strip().split(",")
        word,weights=parts[1],[REAL(x) for x in parts[2:]]
        add_word(word,weights)
        if i%100000==0:
            print(i,"word vectors loaded so far ...")
    file.close()
    print(i-1,"word vectors loaded!")
    return result
    

    
model=load_vectors_from_csv("WORD2VEC-Twitter-Espa_ol_para_Latinoam_rica__Espa_a_y_Estados_Unidos.csv")

print('RAZONAMIENTO ANALÓGICO')
print('¿Cómo se le dice a una mujer que es rey?')
print(model.wv.most_similar(positive=["mujer","rey"],negative=["hombre"]))
print('¿Cómos de le dice a un parcero que es una mujer?')
print(model.wv.most_similar(positive=["mujer","parcero"],negative=["hombre"]))
print('Si el "pozole" es a "Mexico", X es a "Colombia". i.e. ¿Cual es la sopa tradicional de Colombia?')
print(model.wv.most_similar(positive=["colombia","pozole"],negative=["mexico"]))
print()
print('RAZONAMIENTO COMPOSICIONAL')
print("¿Qué usas con una chaqueta en Argentina?")
print(model.wv.most_similar(positive=["chaqueta","argentina"]))
print("¿Qué es lo más parecido en Bogotá a un metro?")
print(model.wv.most_similar(positive=["bogotá","metro"]))
print()
print('EVALUACION DE LA SIMILITUD')
print('¿Colombia se parece más a Ecuador o a Corea?')
print("Colombia vs. Ecuador",model.wv.similarity("colombia","ecuador"))
print("Colombia vs. Corea",model.wv.similarity("colombia","corea"))
print()
print("EVALUACION DE LA PERTENENCIA A UN GRUPO")
print('¿Cual pais no hace parte del grupo Colombia, Ecuador, China. Venezuela?')
print(model.wv.doesnt_match(["colombia","ecuador","china","venezuela"]))
print('¿Cual palabra no pertenece al grupo "comer","bailar","jugar" y "edificio"?')
print(model.wv.doesnt_match(["comer","bailar","jugar","edificio"]))



