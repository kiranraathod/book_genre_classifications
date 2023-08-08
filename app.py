import pickle
from nltk.stem import PorterStemmer 
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords 
import re 
import nltk
from flask import Flask, request, render_template

nltk.download('stopwords')
nltk.download('wordnet')


# cleaning the text 
def cleantext(text):
    
    # removing the "\"
    text = re.sub("'\''","",text)
    
    # removing special symbols 
    text = re.sub("[^a-zA-Z]"," ",text)
    
    # removing the whitespaces
    text = ' '.join(text.split())
    
    # convert text to lowercase 
    text = text.lower()
    
    return text 


# removing the stop_words 
def remove_top_words(text):
    
    remove_top_word = [word for word in text.split() if word not in stop_words] 
    return ' '.join(remove_top_word)


def lematizing(sentence):
    stemSentence=""
    for word in sentence.split():
        stem = lemma.lemmatize(word)
        stemSentence += stem
        stemSentence += " "
    stemSentence = stemSentence.strip()
    return stemSentence 


def stemming(sentence):
    
    stemmed_sentence = ""
    for word in sentence.split():
        stem = stemmer.stem(word)
        stemmed_sentence+=stem
        stemmed_sentence+=" "
    stemmed_sentence = stemmed_sentence.strip()
    return stemmed_sentence 

