import numpy as np
import pandas as pd
from random import randrange, choice
import random
import string # para procesar cadenas de python estándar
import os
import requests

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from gtts import gTTS
from playsound import playsound

from random import randrange, choice

#texto a voz
from gtts import gTTS
from playsound import playsound

#Transforma texto a voz

def txt_voz(texto):
    text2speech = gTTS(text=texto, lang='es')
    text2speech.save('sample.mp3')
    NOMBRE_ARCHIVO = "sample.mp3"
    playsound(NOMBRE_ARCHIVO)
    os.remove(NOMBRE_ARCHIVO)
    
#Traductor de palabras realizado con Python

def Traduccion(source, target, text):
    parametros = {'sl': source, 'tl': target, 'q': text}
    cabeceras = {"Charset":"UTF-8","User-Agent":"AndroidTranslate/5.3.0.RC02.130475354-53000263 5.1 phone TRANSLATE_OPM5_TEST_1"}
    url = "https://translate.google.com/translate_a/single?client=at&dt=t&dt=ld&dt=qca&dt=rm&dt=bd&dj=1&hl=es-ES&ie=UTF-8&oe=UTF-8&inputm=2&otf=2&iid=1dd3b944-fa62-4b55-b330-74909a99969e"
    response = requests.post(url, data=parametros, headers=cabeceras)
    if response.status_code == 200:
        for x in response.json()['sentences']:
            return x['trans']
    else:
        return "Ocurrió un error"

#Leer el archivo de dialogos y separarlo por oraciones y palabras
f=open('chatbot.txt','r',errors = 'ignore')
raw=f.read()
raw=raw.lower()# a minúsculas
nltk.download('punkt', quiet=True, raise_on_error=True)
#punkt Uno de los módulos que vamos a utilizar (y que
#conseguimos con la función download() es punkt.
#Éste módulo contiene modelos para la tokenización
#de textos.
nltk.download('wordnet')

sent_tokens = nltk.sent_tokenize(raw)# se convierte en una lista de oraciones
word_tokens = nltk.word_tokenize(raw)# se convierte en una lista de palabras

lemmer = nltk.stem.WordNetLemmatizer()
#WordNet es un diccionario de inglés incluido en NLTK.
def LemTokens(tokens):
 return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
 return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREETING_INPUTS = ["hello", "hi", "greetings", "what's up"]
GREETING_RESPONSES = ["hi", "hey there", "hi there", "hello", "I am glad!"]
def greeting(sentence): 
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
        
def response(user_response):
    robo_response=''
    
    #Agrego la entrada del usuario al final de la lista 
    #oraciones tokens
    sent_tokens.append(user_response)
    
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    #Ahora calculamos la similitud de coseno entre ellos. 
    #tfidf [-1] se refiere al último documento del archivo 
    #que técnicamente es la respuesta del usuario.
    vals = cosine_similarity(tfidf[-1], tfidf)
    
    #ordena los elementos de una matriz y devuelve la posicion de los indices
    idx=vals.argsort()[0][-2]
    
    #Devuelve una matriz aplanada. Un iterador plano 1-D sobre la matriz.
    flat = vals.flatten()
    
    flat.sort()
    req_tfidf = flat[-2]
    
    if(req_tfidf==0):
        return robo_response+\
                      "Hell, I don't know what to answer, so I better tell you the same thing, so I can learn something new "
    else:
        return robo_response+sent_tokens[idx+1]

flag=True

new_dialogue = pd.read_csv('new_dialogue.csv')

def aumenta_dialogo(new_dialogue):
    archivo = open("chatbot1.txt", "r")
    di=archivo.readlines()
    n=len(new_dialogue)
    for i in range(len(di[1:])):
        new_dialogue.loc[n,'question']=di[i]
        new_dialogue.loc[n,'response']=di[1:][i]
        n+=1
    archivo.close()
    print(di)
    return new_dialogue

#new_dialogue=aumenta_dialogo(new_dialogue)

n_d=len(new_dialogue)

print('¡Si quieres que dejemos de hablar, solo escribe adios!\n')
print("Frankentbot: "+ Traduccion("en", "es", "Hello my name is Frankentbot, \
        I am very happy to talk to you,")+'\nMe gustaria saber ¿Cómo estas?')
txt_voz(Traduccion("en", "es", "Hello my name is Frankentbot \
        I am very happy to talk to you,")+'\nMe gustaria saber ¿Cómo estas?')
old_user_response=''
while(flag==True):
    user_response = input('Amig@: ')
    user_response = Traduccion("es", "en", user_response)
    user_response=user_response.lower()
    if 'error'==user_response:
        txt_voz('Que debi responder')
        print('Frankentbot: ¿Qué debí responder?')
        new_dialogue.loc[n_d,'question']=old_user_response
        new_dialogue.loc[n_d,'response']=input('Amig@: ')
        n_d+=1
        txt_voz('Gracias por ayudarme a aprender algo nuevo')
        print('Gracias por ayudarme a aprender algo nuevo')
        user_response = input('Amig@: ')
        user_response = Traduccion("es", "en", user_response)
        user_response=user_response.lower()
    
    old_user_response=user_response
    try:
        if new_dialogue.loc[n_d,'response']=='xxxxxxxxxx':
            new_dialogue.loc[n_d,'response']= user_response
            n_d+=1
    except:
        pass
    if(user_response not in ['goodbye', 'bye', 'see you', 'see you later', 'I hope to see you soon']):
        query=new_dialogue[new_dialogue['question']==user_response]
        if 0<len(query):
            n=choice(query.index)
            print("Frankentbot: "+Traduccion("en", "es", query.loc[n,'response']))
            txt_voz(Traduccion("en", "es", query.loc[n,'response']))
        else:
            respuesta=greeting(user_response)
            if(respuesta!=None):
                print("Frankentbot: "+Traduccion("en", "es", respuesta))
                txt_voz(Traduccion("en", "es", query.loc[n,'response']))
            else:
                print("Frankentbot: ",end="")
                res=response(user_response)
                print(Traduccion("en", "es", res))
                txt_voz(Traduccion("en", "es", res))
                if res =="Hell, I don't know what to answer, so I better tell you the same thing, so I can learn something new ":
                    print("Frankentbot: "+Traduccion("en", "es",user_response))
                    txt_voz(Traduccion("en", "es",user_response))
                    new_dialogue.loc[n_d,'question']=user_response
                    new_dialogue.loc[n_d,'response']='xxxxxxxxxx'
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("Frankentbot: "+Traduccion("en", "es", "I say goodbye wishing that just like today you never stop smiling"))
        txt_voz(Traduccion("en", "es", "I say goodbye wishing that just like today you never stop smiling"))
    new_dialogue.to_csv('new_dialogue.csv', index=False);
    


