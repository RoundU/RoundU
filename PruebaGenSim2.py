import pandas as pd
import gensim as gns

import nltk
#nltk.download()
lexematizacion = pd.read_csv("LexemasEspanol", sep="\t", header=None, names=['lexema', 'palabra'])

def lemmatize_stemming(text):
    #lexematizacion = pd.read_csv("LexemasEspanol", sep="\t", header=None, names=['lexema', 'palabra'])
    return lexematizacion.loc[lexematizacion["palabra"] == text].iloc[0].get("lexema") if sum(lexematizacion["palabra"] == text) > 0 else text
    #return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

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
            
    return result

def toDictionary(lista):
    diccionario = {}
    for elemento in lista:
        if elemento in diccionario.keys():
            diccionario[elemento] += 1
        else:
            diccionario[elemento] = 1
    return diccionario

texts = ["Se nos aseguro que para 2020 ya no habría coches diesel, ya que más de 100.000 personas mueren al año por contaminación, estamos ya a las puertas de los felices años 20 y la única medida que se le ocurre es subir 3.8 décimas el diesel. Señor Sánchez, no queremos ninguna subida ridícula del diesel, queremos que solo los camiones y furgonetas puedan usar el diesel y que este se prohíba para los turismos. Y si por ley no puede prohibir los vehículos diesel, se sube a 20 € el litro para todo aquel que no sea camionero o transportista. Y se acaba con la contaminación y polución que producen estos vehículos.",
        "Pues resulta que tengo pensado irme del 24 de junio al 1 de julio a Venecia. El vuelo es directo y está muy bien de precio. Además es en familia y hace mucho que no hacemos uno juntos, asi que tengo especiales ganas. El día 24 llegaríamos a Venecia a las 11 de la noche, con lo cual ese día ya sería perdido totalmente. En cambio, el día 1 el avión sale a las 5 de la tarde. Obviamente mi intención no es estar todos los días en Venecia, sino ir también o a Verona y ver también el Lago di Garda (me dijeron que es una pasada) o bien ir a Florencia. Si me comentais que da tiempo para ir a los dos sitios, sería perfecto. Me gustaría que me aconsejaseis al respecto sobre que itinerario realizar, así como donde alojarse, tema de trenes, etc.",
        "Hija primogénita del matrimonio de dos de las familias más ricas de Soria, los Ridruejo y los Brieva, Pitita se trasladó siendo muy pequeña con sus padres a Madrid. En 1957 contrajo matrimonio con José Manuel Stilianópulos Estella, filipino de ascendencia griega, del que adoptó la nacionalidad y con el que tuvo tres hijos. Como pintora, colgó parte de su producción en algunas exposiciones en Roma, y además protagonizó dos películas para la televisión alemana en 1970. En 1971, a petición de Federico Fellini, realizó las pruebas para trabajar en un film a las órdenes del director italiano, pero el traslado de su marido le obligó a abandonar el proyecto. También en aquella época comenzó a interesarse por las filosofías orientales. En 1973 fueron nombrados embajadores de Filipinas en España, etapa en la que acompañaron a los entonces príncipes de España en su viaje por ese país. Posteriormente, al ser nombrado su marido embajador filipino en Londres, desarrolló una intensa actividad social y se introdujo en el mundo de la moda. También inició sus estudios de parapsicología, historia de las religiones y filosofías orientales. En 1983 el matrimonio Stilianópulos decidió abandonar la carrera diplomática e instalarse en España, entre Madrid y Marbella, destacando entre los miembros de la 'jet-set', siendo objeto de crónicas sociales, como las escritas por Francisco Umbral. Alabada por su elegancia, ha recibido numerosos galardones como el Premio Paride, el del diario Pueblo y varios del periódico ABC. Escribió sobre temas de filosofías orientales en varias publicaciones hasta cambiarlos por lo que ella calificó por asuntos de 'designios divinos', que reflejó en un libro sobre la Virgen María. La periodista Beatriz Cortazar se ha hecho eco de su fallecimiento a través de Twitter, catalogándola además como 'una señora estupenda y muy divertida'.",
        "Ahora no estoy leyendo ninguno y hace tiempo que no leo alguna novela...algún consejo sobre alguna que deba leer? Alguno que enganche (los de Dan Brown los leí, me enganchaban los primeros, pero los ultimos son basura en mi opinión). No se, no tengo ni idea de qué leer ahora mismo jajaj me da bastante pereza y necesito un libraco top que me devuelva las ganas de leer ",
        "Ayuda con mi avestruz, animales. Esta perdiendo su pelaje y me estoy preocupando alguien me ayuda que tenga este tipo de animales exoticos en su finca o simalar un saludo. Falta de pelaje se situa por la zona de la 'barriga'. Descarto problemas de alimentacion. Tiene una buena higiene",
        "Llevamos una semanita muy buena con palizas por parte de inmigrantes (el chaval de San Sebastián con muerte cerebral o la anciana a la que le querían robar el bolso por mencionar unos cuantos) y han salido por los medios (mas otras cuantas que no habrán llegado a otros teletipos que no sean los locales). ¿Creéis que la solución está en pedir penas más duras y mayor vigilancia en nombre de la seguridad? ¿Creéis que nos vamos a sentir más seguros con cámaras de seguridad en cada esquina que no aportan nada a la hora de encontrar a un desaparecido? ¿Creéis que la solución está en aislarse de la sociedad en tu habitación con mil alarmas porque crees que es mala y te va a hacer daño? La culpa de todo esto la tienen unos pocos: los delincuentes (sean españoles o inmigrantes o seres de luz o marcianos) que el Estado no castiga como es debido. Sirven de ayuda a la gente poderosa para que nosotros, con una sensación de inseguridad creciente, acabemos pidiendo a nuestro 'salvador el Estado medidas más duras que, si bien parecen controlar más la delincuencia, también nos coarta nuestras libertades y nos hace más esclavos del Estado. No dudéis de que, por nuestra seguridad, acabemos pidiendo un Estado orwelliano estilo 1984 en el que la libertad individual se nota por su ausencia.",
        "El año pasado acabé el bachillerato y la selectividad. Me metí a un CFGS de Comercio Internacional pero lo acabé dejando porque me parecía una mierda, hablando claro. Para no ser un nini y una carga inutil en casa, me puse a buscar curro de recepcionista. Recepcionista porque hablo alemán nativo y mi inglés es bastante bueno también. Encontré curro de recepcionista en el mejor hotel de mi zona, encima a 15 minutos caminando de mi casa. Actualmente soy ayudante de recepción, con dos días libres y turnos de 8h: salario base 1480€ + propinas (les llevamos las maletas a los guiris). Este mes de abril la propina han sido 150€. Vamos, que he cobrado 1630€ en total. Muchísimo mas de lo que esperaba cuando buscaba curro. Mis compañeros que libran solo un día y son una categoría más cobran casi casi 2k limpios (sin contar propinas). Y como me he adaptado muy bien al trabajo, ya me han ofrecido quedarme si quiero... lo que pasa es que en teoría quiero estudiar Derecho en septiembre, en Madrid.",
        "¿puede de alguna manera una web saber si he hecho un pantallazo? Si capturo toda la pantalla, ¿queda algún tipo de registro? ¿O eso sólo podría pasar en los programas? Hablo intentándolo desde el ordenador. ",
        "No me encajan esos ojos en su cara, le quedarían mejor oscuros. La nariz la tiene operada (y a saber que más). Las cejas pintadas no me gustan nada. "
]

listaDeListaDeTokens = [[]]
for text in texts:
    listaDeListaDeTokens.append(preprocess(text))

print(listaDeListaDeTokens)

dictionary = gns.corpora.Dictionary(listaDeListaDeTokens)
#dictionary = gns.corpora.Dictionary(processed_docs.encode(encoding='Unicode',errors='strict'))
#dictionary = gns.corpora.Dictionary(unicode(processed_docs, "utf-8"))
#dictionary = toDictionary(tokens)

print(dictionary)

bow_corpus = [dictionary.doc2bow(listaDeTokens) for listaDeTokens in listaDeListaDeTokens]
print(bow_corpus)

# lda_model =  gns.models.LdaMulticore(bow_corpus, 
#                                    num_topics = 2, 
#                                    id2word = dictionary,                                    
#                                    passes = 10,
#                                    workers = 2)

lda_model = gns.models.LdaModel(bow_corpus, num_topics=2)

# from gensim.test.utils import datapath
# temp_file = datapath("/home/marc/Escritorio/LDAModel")
# lda_model.save(temp_file)

print(lda_model.get_term_topics())
print(lda_model.get_topic_terms())

print(lda_model.get_topics())
print(lda_model.get_document_topics())
print(lda_model.top_topics())
print(lda_model.top())