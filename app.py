# To run the project  1. cd "c:\Users\sharvil deshmukh\OneDrive\Desktop\Desktop\SHARVIL PROJECT\Kisanmitr"

# 2. .\.venv\Scripts\python.exe app.py

import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
import re, io, base64
from datetime import datetime

#api

os.environ.setdefault('GROQ_API_KEY', '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')


from nlp.responder import generate_response
from database.db import init_db, register_farmer, login_farmer, save_message, get_history

app = Flask(__name__)
app.secret_key = 'kisanmitr-secret-2025-xK9!'   # change in production
CORS(app)
init_db()   # ensure tables exist on every startup


# ── AUTH HELPERS 
def logged_in():
    return 'farmer_id' in session


# ── ROUTES 
@app.route('/')
def index():
    if not logged_in():
        return redirect(url_for('login_page'))
    return render_template('index.html',
                           farmer_name=session.get('farmer_name', 'Farmer'))


@app.route('/login', methods=['GET'])
def login_page():
    if logged_in():
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def do_login():
    data   = request.get_json()
    mobile = data.get('mobile', '').strip()
    pwd    = data.get('password', '').strip()
    if not mobile or not pwd:
        return jsonify({'error': 'Mobile and password are required'}), 400
    farmer = login_farmer(mobile, pwd)
    if not farmer:
        return jsonify({'error': 'Invalid mobile number or password'}), 401
    session['farmer_id']   = farmer['id']
    session['farmer_name'] = farmer['name']
    return jsonify({'success': True, 'name': farmer['name']})


@app.route('/register', methods=['POST'])
def do_register():
    data   = request.get_json()
    name   = data.get('name', '').strip()
    mobile = data.get('mobile', '').strip()
    pwd    = data.get('password', '').strip()
    if not name or not mobile or not pwd:
        return jsonify({'error': 'All fields are required'}), 400
    if len(mobile) != 10 or not mobile.isdigit():
        return jsonify({'error': 'Enter a valid 10-digit mobile number'}), 400
    if len(pwd) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    farmer = register_farmer(name, mobile, pwd)
    if not farmer:
        return jsonify({'error': 'Mobile number already registered. Please login.'}), 409
    session['farmer_id']   = farmer['id']
    session['farmer_name'] = farmer['name']
    return jsonify({'success': True, 'name': farmer['name']})


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))


# ── CHAT 
@app.route('/chat', methods=['POST'])
def chat():
    if not logged_in():
        return jsonify({'error': 'Not logged in'}), 401
    data  = request.get_json()
    text  = data.get('message', '').strip()
    lang  = data.get('language', 'en')
    image = data.get('image', None)   # base64 string, optional

    if not text and not image:
        return jsonify({'error': 'Empty message'}), 400

    if image:
        # Vision path: analyse crop image via Groq multimodal
        from nlp.responder import ask_groq_vision
        response = ask_groq_vision(image, text or None, lang)
        intent   = 'image_analysis'
    else:
        response, intent = generate_response(text, lang)

    save_message(session['farmer_id'], text or '(image)', response, intent)
    return jsonify({
        'response': response,
        'intent':   intent,
        'timestamp': datetime.now().strftime('%I:%M %p')
    })



# ── HISTORY 
@app.route('/history')
def history():
    if not logged_in():
        return jsonify({'error': 'Not logged in'}), 401
    msgs = get_history(session['farmer_id'], limit=50)
    return jsonify({'history': msgs, 'farmer_name': session.get('farmer_name')})


# ── TTS 
@app.route('/tts', methods=['POST'])
def tts():
    from gtts import gTTS
    data = request.get_json()
    text = re.sub(r'\s+', ' ', data.get('text', '')[:400]).strip()
    lang_map = {'en': 'en', 'hi': 'hi', 'mr': 'mr'}
    tts_obj = gTTS(text=text, lang=lang_map.get(data.get('language', 'en'), 'en'))
    buf = io.BytesIO()
    tts_obj.write_to_fp(buf)
    buf.seek(0)
    return jsonify({'audio': base64.b64encode(buf.read()).decode()})


if __name__ == '__main__':
    print('Starting KrishiMitra AI server...')
    print('Open http://localhost:5000 in your browser')
    app.run(debug=True, port=5000)
