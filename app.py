from flask import Flask, request, jsonify
import chatbot  # Importa tu lógica desde chatbot.py

app = Flask(__name__)

@app.route('/')
def home():
    return "¡Chatbot desplegado con Render!"

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_message = data.get('message')
    bot_response = chatbot.respuesta(user_message)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
