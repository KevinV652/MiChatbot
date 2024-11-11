from flask import Flask, request, jsonify, render_template
import chatbot

app = Flask(__name__, static_folder='static', template_folder='templates')

# Cargamos el modelo y los datos al iniciar el servidor
chatbot.cargar_modelo()

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_message = data.get('message', '')
    bot_response = chatbot.respuesta(user_message)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3245, debug=True)
