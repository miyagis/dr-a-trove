from flask import Flask, request, jsonify
from chat_engine import front_end_integration

app = Flask(__name__)

@app.route('/answer', methods=['POST'])
@app.route('/api/answer', methods=['POST'])
def get_answer():
    question = request.json.get('question')
    if not question:
        return jsonify({'error': 'Question is required'}), 400

    chat_history = {
                        "1": {
                            "user": "Hi",
                            "assistant": "Hello."
                        }
                    }
    answer = front_end_integration(question, chat_history)

    return answer

if __name__ == '__main__':
    app.run(debug=True)