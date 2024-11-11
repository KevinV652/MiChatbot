import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

lemmatizer = WordNetLemmatizer()

# Definimos variables globales para evitar recargar innecesariamente
model = None
intents = None
words = None
classes = None

def cargar_modelo():
    """
    Función para inicializar los recursos del chatbot, como el modelo y los datos.
    """
    global model, intents, words, classes
    
    # Cargamos el archivo intents.json
    intents = json.loads(open('intents.json', encoding='utf-8').read())
    print(f"Total de intenciones cargadas: {len(intents['intents'])}")
    
    # Cargamos los datos necesarios para el modelo
    words = pickle.load(open('words.pkl', 'rb'))
    classes = pickle.load(open('classes.pkl', 'rb'))
    
    # Cargamos el modelo preentrenado
    model = load_model('chatbot_model.h5')
    print("Modelo cargado correctamente.")

def clean_up_sentence(sentence):
    """
    Procesa la oración de entrada convirtiendo cada palabra a su forma raíz.
    """
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    """
    Convierte la oración en una bolsa de palabras (vector de 0s y 1s).
    """
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    """
    Predice la clase (categoría) de la oración de entrada.
    """
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    max_index = np.where(res == np.max(res))[0][0]
    category = classes[max_index]
    return category

def get_response(tag, intents_json):
    """
    Obtiene una respuesta aleatoria basada en el tag (categoría) predicho.
    """
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i["tag"] == tag:
            return random.choice(i['responses'])
    return "Lo siento, no entiendo tu pregunta."

def respuesta(message):
    """
    Función principal para procesar el mensaje del usuario y devolver una respuesta.
    """
    if not model or not intents or not words or not classes:
        raise ValueError("El modelo o los datos no han sido cargados. Llama primero a `cargar_modelo()`.")
    
    tag = predict_class(message)
    return get_response(tag, intents)
