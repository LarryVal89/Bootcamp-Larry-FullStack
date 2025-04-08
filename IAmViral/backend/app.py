from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from PIL import Image
import requests
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Configuración de rutas
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Cargar modelo de predicción
model = tf.keras.models.load_model('models/viralidad_model.h5')

@app.route('/predict', methods=['POST'])
def predict_viralidad():
    try:
        data = request.json
        content_type = data.get('type')
        content = data.get('content')
        
        if content_type == 'text':
            # Procesamiento de texto
            prediction = process_text(content)
        elif content_type == 'image':
            # Procesamiento de imagen
            prediction = process_image(content)
        elif content_type == 'video':
            # Procesamiento de video
            prediction = process_video(content)
        else:
            return jsonify({'error': 'Tipo de contenido no soportado'}), 400
            
        return jsonify({
            'prediction': float(prediction),
            'viral_score': calculate_viral_score(prediction)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/trends', methods=['GET'])
def get_trends():
    try:
        # Obtener tendencias de Twitter
        twitter_trends = get_twitter_trends()
        
        # Obtener tendencias de Google
        google_trends = get_google_trends()
        
        return jsonify({
            'twitter_trends': twitter_trends,
            'google_trends': google_trends
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def process_text(text):
    # Implementar procesamiento de texto
    return 0.75  # Ejemplo

def process_image(image_data):
    # Implementar procesamiento de imagen
    return 0.65  # Ejemplo

def process_video(video_data):
    # Implementar procesamiento de video
    return 0.85  # Ejemplo

def calculate_viral_score(prediction):
    return prediction * 100

def get_twitter_trends():
    # Implementar conexión con API de Twitter
    return ["#Trend1", "#Trend2", "#Trend3"]

def get_google_trends():
    # Implementar conexión con API de Google Trends
    return ["Trend1", "Trend2", "Trend3"]

if __name__ == '__main__':
    app.run(debug=True) 