import pickle
from nltk.stem import PorterStemmer 
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords 
import re 
import nltk
from flask import Flask, request, render_template

nltk.download('stopwords')
nltk.download('wordnet')

# Initialize stemmer and lemmatizer
stemmer = PorterStemmer()
lemma = WordNetLemmatizer()

# Load stopwords
stop_words = set(stopwords.words('english'))

# Cleaning the text
def cleantext(text):
    # Removing the "\"
    text = re.sub("'\''", "", text)
    # Removing special symbols
    text = re.sub("[^a-zA-Z]", " ", text)
    # Removing extra whitespaces
    text = ' '.join(text.split())
    # Convert text to lowercase
    text = text.lower()
    return text 

# Removing the stop_words
def remove_top_words(text):
    remove_top_word = [word for word in text.split() if word not in stop_words]
    return ' '.join(remove_top_word)

def lematizing(sentence):
    stemSentence = ""
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
        stemmed_sentence += stem
        stemmed_sentence += " "
    stemmed_sentence = stemmed_sentence.strip()
    return stemmed_sentence 

# Function to predict the genre
def test(text, model, tfidf_vectorizer):
    text = cleantext(text)
    text = remove_top_words(text)
    text = lematizing(text)
    text = stemming(text)
    text_vector = tfidf_vectorizer.transform([text])
    predicted = model.predict(text_vector)
    
    newmapper = {0: 'Fantasy', 1: 'Science Fiction', 2: 'Crime Fiction',
                 3: 'Historical novel', 4: 'Horror', 5: 'Thriller'}
    
    return newmapper[predicted[0]]

# Load the trained model and TF-IDF vectorizer
file = open('bookgenremodel.pkl', 'rb')
model = pickle.load(file)
file.close()

file1 = open('tfdifvector.pkl', 'rb')  # Corrected 'rd' to 'rb'
tfidf_vectorizer = pickle.load(file1)
file1.close()

# Initialize the Flask app
app = Flask(__name__)

# Define a route for the web application
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        mydict = request.form
        text = mydict["summary"]
        prediction = test(text, model, tfidf_vectorizer)
        
        return render_template('index.html', genre=prediction, text=str(text)[:100], showresult=True)
    
    return render_template('index.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
