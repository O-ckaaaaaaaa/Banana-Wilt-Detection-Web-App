import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'your-secret-key'  # Needed for flash messages

# Load both models
health_model = load_model('banana_plant_classifier.h5')
verification_model = load_model('banana_leaf_classifier.h5')  # New model for verification
def preprocess_image(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image
app.secret_key = 'your_secret_key'
# Initialize database
def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
init_db()
# Home
@app.route('/')
def home():
    return redirect(url_for('login'))
# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        with sqlite3.connect('database.db') as conn:
            try:
                conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                return "Username already exists."

    return render_template('register.html')
# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cur.fetchone()

            if user and check_password_hash(user[2], password):
                session['user_id'] = user[0]
                session['username'] = user[1]
                return render_template('home.html')
                #return redirect(url_for('dashboard'))
            else:
                return "Invalid username or password."
    return render_template('login.html')
# Dashboard (Protected Route)
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))
# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
@app.route('/index')
def index():
    return render_template('home.html')
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))

    file = request.files['image']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    # First verify if it's a banana leaf
    image = preprocess_image(filepath)
    verification_result = verification_model.predict(image)[0][0]

    if verification_result < 0.5:  # Adjust threshold as needed
        return render_template('banana.html')
        #return render_template('result.html',
    # error="The uploaded image doesn't appear to be a banana leaf. Please upload a clear image of a banana leaf.")
    # If verification passes, proceed with health prediction
    health_prediction = health_model.predict(image)[0][0]
    label = "Wilt-Affected" if health_prediction < 0.5 else "Healthy"
    confidence = round(health_prediction * 100, 2) if health_prediction >= 0.5 else round((1 - health_prediction) * 100,
                                                                                          2)
    # Treatment tips based on prediction
    if label == "Wilt-Affected":
        tips = [
            "Remove and destroy infected plants immediately.",
            "Use disease-free planting materials.",
            "Avoid using contaminated tools between plants.",
            "Practice crop rotation and improve soil drainage.",
            "Apply appropriate bio-control agents or fungicides."
        ]
    else:
        tips = [
            "Continue regular monitoring.",
            "Maintain good field hygiene.",
            "Use clean tools for pruning or harvesting.",
            "Avoid waterlogging around banana plants.",
            "Fertilize appropriately to maintain plant health."
        ]
    return render_template('result.html',
                           label=label,
                           confidence=confidence,
                           filename=filename,
                           tips=tips,
                           is_banana_leaf=True)


    """
@app.route('/predict', methods=['POST'])
def predict():
    if 'imageData' not in request.form:
        return "No image data", 400

    data_url = request.form['imageData']
    header, encoded = data_url.split(',', 1)
    binary_data = base64.b64decode(encoded)

    # Save the image temporarily
    image = Image.open(BytesIO(binary_data))
    filename = 'captured.jpg'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(filepath)

    # Process the image as before
    image_input = preprocess_image(filepath)
    verification_result = verification_model.predict(image_input)[0][0]

    if verification_result < 0.5:
        return render_template('banana.html')

    health_prediction = health_model.predict(image_input)[0][0]
    label = "Wilt-Affected" if health_prediction < 0.5 else "Healthy"
    confidence = round(health_prediction * 100, 2) if health_prediction >= 0.5 else round((1 - health_prediction) * 100, 2)

    tips = [
        "Remove and destroy infected plants immediately.",
        "Use disease-free planting materials.",
        "Avoid using contaminated tools between plants.",
        "Practice crop rotation and improve soil drainage.",
        "Apply appropriate bio-control agents or fungicides."
    ] if label == "Wilt-Affected" else [
        "Continue regular monitoring.",
        "Maintain good field hygiene.",
        "Use clean tools for pruning or harvesting.",
        "Avoid waterlogging around banana plants.",
        "Fertilize appropriately to maintain plant health."
    ]

    return render_template('result.html',
                           label=label,
                           confidence=confidence,
                           filename=filename,
                           tips=tips,
                           is_banana_leaf=True)"""

@app.route('/camera')
def camera():
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)