from flask import Flask, request, jsonify
import json
from chatbot_model import get_response  # Función que usará tu modelo entrenado

app = Flask(__name__)

@app.route('/get_response', methods=['POST'])
def respond():
    user_message = request.json['message']
    bot_response = get_response(user_message)  # Llama tu modelo aquí
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
