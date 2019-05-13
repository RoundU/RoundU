import pandas as pd
import gensim as gns
import nltk
import re
import pickle


def lemmatize_stemming(text):
    frecuente = False
    for lexemaFrecuente in lexemasFrecuentes:
        if text == lexemaFrecuente[1]:
            return lexemaFrecuente[0]
    if not frecuente:
        lexemaBuscado = lexematizacion.loc[lexematizacion["palabra"] == text].iloc[0].get("lexema") if sum(lexematizacion["palabra"] == text) > 0 else text
        lexemasFrecuentes.append([lexemaBuscado, text])
    return lexemaBuscado


# Tokenize and lemmatize
def preprocess(text):
    result=[]
    resultString = ""
    for token in gns.utils.simple_preprocess(text) :
        #if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
        if token not in nltk.corpus.stopwords.words('spanish') and len(token) > 3:
            lematizado = lemmatize_stemming(token)
            result.append(lematizado)
            resultString += " " + lematizado            
    return (result, resultString)

def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


lexematizacion = pd.read_csv("LexemasEspanol", sep="\t", header=None, names=['lexema', 'palabra'])
lexemasFrecuentes = []

raw_texts = pd.read_csv("data/stream_e.csv", sep="ef5r64i")["Texto"]

texts = []
for raw_text in raw_texts:
    texts.append(re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', raw_text))

listaDeListaDeTokens = [[]]
for text in texts:
    (vector, cadena) = preprocess(text)
    listaDeListaDeTokens.append(vector)

dictionary = gns.corpora.Dictionary(listaDeListaDeTokens)

bow_corpus = [dictionary.doc2bow(listaDeTokens) for listaDeTokens in listaDeListaDeTokens]

from gensim.test.utils import datapath
temp_file2 = datapath("/home/marc/Escritorio/BowPickle")
save_object((bow_corpus, dictionary), temp_file2)

lda_model4 = gns.models.LdaModel(bow_corpus, num_topics=4, id2word=dictionary)

print(lda_model4)