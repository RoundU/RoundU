import pandas as pd
import gensim as gns

import nltk
#nltk.download()

def lemmatize_stemming(text):
    lexematizacion = pd.read_csv("LexemasEspanol", sep="\t", header=None, names=['lexema', 'palabra'])
    return lexematizacion.loc[lexematizacion["palabra"] == text].iloc[0].get("lexema") if sum(lexematizacion["palabra"] == text) > 0 else text
    #return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

# Tokenize and lemmatize
def preprocess(text):
    result=[]
    for token in gns.utils.simple_preprocess(text) :
        #if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
        if token not in nltk.corpus.stopwords.words('spanish') and len(token) > 3:
            result.append(lemmatize_stemming(token))
            
    return result

def toDictionary(lista):
    diccionario = {}
    for elemento in lista:
        if elemento in diccionario.keys():
            diccionario[elemento] += 1
        else:
            diccionario[elemento] = 1
    return diccionario

text = "Se nos aseguro que para 2020 ya no habría coches diesel, ya que más de 100.000 personas mueren al año por contaminación, estamos ya a las puertas de los felices años 20 y la única medida que se le ocurre es subir 3.8 décimas el diesel. Señor Sánchez, no queremos ninguna subida ridícula del diesel, queremos que solo los camiones y furgonetas puedan usar el diesel y que este se prohíba para los turismos. Y si por ley no puede prohibir los vehículos diesel, se sube a 20 € el litro para todo aquel que no sea camionero o transportista. Y se acaba con la contaminación y polución que producen estos vehículos."
tokens = preprocess(text)
print(tokens)

dictionary = toDictionary(tokens)

print(dictionary)