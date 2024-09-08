from flask import Flask, request, jsonify, session
from flask_session import Session
from chat_engine import front_end_integration
import uuid

app = Flask(__name__)

# Configure Flask-Session
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a strong, random secret key
app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem for session storage (can be database-based)
Session(app)  # Initialize Flask-Session extension

chat_history = {
                    "session_uuid": {
                        "user": "Hi",
                        "assistant": "Hello."
                    }
                }

@app.route('/answer', methods=['POST'])
@app.route('/api/answer', methods=['POST'])
def get_answer():
    question = request.json.get('question')
    if not question:
        return jsonify({'error': 'Question is required'}), 400

    # Get session ID or create a new session if it doesn't exist
    session_id = session.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())  # Generate a unique session ID using uuid
        session['session_id'] = session_id

    # Access and update chat history for the current session
    chat_history = session.get(session_id, {})  # Get chat history for this session (empty dict if new)
    chat_history["user"] = question
    answer = front_end_integration(question, chat_history)
    chat_history["assistant"] = answer  # Add LLM response to the history

    session[session_id] = chat_history  # Update chat history in the session

    return answer

if __name__ == '__main__':
    app.run(debug=True)