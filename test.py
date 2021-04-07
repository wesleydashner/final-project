import pandas as pd
import numpy as np
print(np.version.version)
assert np.version.version == '1.19.5'
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow import keras
import sklearn
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

df_true = pd.read_csv('data/True.csv')
df_false = pd.read_csv('data/Fake.csv')

df_true['label'] = 1
df_false['label'] = 0

df = pd.concat([df_false, df_true])

df = df.drop('title', axis = 1)
df = df.drop('subject', axis = 1)
df = df.drop('date', axis = 1)

df = sklearn.utils.shuffle(df)

data = df['text']
labels = df['label']

stop_words = list(stopwords.words('english'))

filterd_data = []
for words in data:
    if words not in stop_words:
        filterd_data.append(words)

max_len = 500
max_features = 10000

tokenizer = Tokenizer(num_words=max_features)
tokenizer.fit_on_texts(filterd_data)
sequence = tokenizer.texts_to_sequences(filterd_data)
ready_data = pad_sequences(sequence, maxlen=max_len)

train_data = ready_data[:25000]
train_labels = labels[:25000]

validation_data = ready_data[25000:35000]
validation_labels = labels[25000:35000]

test_data = ready_data[35000:]
test_labels = labels[35000:]
model = keras.models.load_model('model')
print(model.evaluate(test_data, test_labels))

