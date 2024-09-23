from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
from keras import layers
import keras
import urllib.parse as parse
import re
import json
from gensim.models import Word2Vec

def preprocess_url(url):
    # Preprocess URL before inference
    decoded_url = parse.unquote(url).lower()
    pattern = r'[^a-zA-Z0-9\s]'
    clean_url = re.sub(pattern, ' ', decoded_url.strip())
    if(len(clean_url.split()) == 1):  
        return clean_url.split()
    return clean_url.split()[1:]

def load_tokenizer(path):
    # Load the tokenizer used during training
    tokenizer = Tokenizer()
    tokenizer_config = {}
    with open(path, 'r', encoding='utf-8') as f:
        tokenizer_config = json.load(f)
    tokenizer.word_index = tokenizer_config['word_index']
    tokenizer.num_words = tokenizer_config['num_words']
    return tokenizer


Embedding_dimensions = 100
vocab_length = 7000
word2vec = Word2Vec.load('./word2vec.model')
tokenizer = load_tokenizer('./tokenizer_config.json')
embedding_matrix = np.zeros((vocab_length, Embedding_dimensions))

for word, token in tokenizer.word_index.items():
    if word2vec.wv.__contains__(word):
        embedding_matrix[token] = word2vec.wv.__getitem__(word)
max_length = 30

model = keras.Sequential()

model.add(layers.Embedding(input_dim=vocab_length, output_dim=Embedding_dimensions, weights=[embedding_matrix], input_length=max_length, trainable=False))
model.add(layers.Bidirectional(layers.LSTM(units=100, return_sequences=True)))
model.add(layers.Bidirectional(layers.LSTM(units=100, return_sequences=True)))
model.add(layers.Conv1D(100, 5, activation='relu'))
model.add(layers.GlobalMaxPool1D())
model.add(layers.Dense(1, activation='sigmoid'))
model.load_weights('./model.h5')

def predict_single_url(url):
    # Preprocess the URL and prepare it for inference
    
    preprocessed_url = preprocess_url(url)
    if(len(preprocessed_url) == 0):
        return "none"
    tokenized = tokenizer.texts_to_sequences([' '.join(preprocessed_url)])
    padded = pad_sequences(tokenized, maxlen=max_length)

    # Make prediction
    prediction = model.predict(padded)
    if (prediction[0][0] > 0.8):
        return "attack"
    else:
        return "none"
    

        
