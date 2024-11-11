import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer #Para pasar las palabras a su forma raíz

#Para crear la red neuronal
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD, Adam
from keras.callbacks import EarlyStopping

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json', encoding='utf-8').read())


nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '¿', '.', ',']

#Clasifica los patrones y las categorías
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

#Pasa la información a unos y ceros según las palabras presentes en cada categoría para hacer el entrenamiento
training = []
output_empty = [0]*len(classes)
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])
random.shuffle(training)
print(len(training)) 
train_x=[]
train_y=[]
for i in training:
    train_x.append(i[0])
    train_y.append(i[1])

train_x = np.array(train_x) 
train_y = np.array(train_y)

#Creamos la red neuronal
model = Sequential()
model.add(Dense(256, input_shape=(len(train_x[0]),), name="inp_layer", activation='relu'))  # Incrementado a 256
model.add(Dropout(0.5, name="hidden_layer1"))
model.add(Dense(128, name="hidden_layer2", activation='relu'))  # Incrementado a 128
model.add(Dropout(0.5, name="hidden_layer3"))
model.add(Dense(len(train_y[0]), name="output_layer", activation='softmax'))

#Creamos el optimizador y lo compilamos
adam = Adam(learning_rate=0.001)
model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

#Entrenamos el modelo y lo guardamos
early_stop = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)
model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=16, verbose=1, callbacks=[early_stop])
model.save("chatbot_model.h5")