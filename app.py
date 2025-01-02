from flask import Flask, request, jsonify, render_template
from main import get_text_response  # Import the function from main.py

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/get-messages', methods=['POST', 'GET'])
def handle_text_message():
    user_input = request.json.get('user-prompt')
    if not user_input:
        return jsonify({'response': "No input provided"}), 400

    ai_response = get_text_response(user_input)
    return jsonify({'response': ai_response})

if __name__ == '__main__':
    app.run(debug=True)
