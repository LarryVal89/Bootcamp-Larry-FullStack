import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from datetime import datetime

def create_model():
    model = models.Sequential([
        layers.Dense(256, activation='relu', input_shape=(150,)),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def prepare_tiktok_features(df):
    # Extraer características específicas de TikTok
    features = pd.DataFrame()
    
    # Estadísticas básicas
    features['play_count'] = df['stats'].apply(lambda x: x['play_count'])
    features['digg_count'] = df['stats'].apply(lambda x: x['digg_count'])
    features['share_count'] = df['stats'].apply(lambda x: x['share_count'])
    features['comment_count'] = df['stats'].apply(lambda x: x['comment_count'])
    
    # Calcular ratios
    features['engagement_rate'] = (features['digg_count'] + features['comment_count'] + features['share_count']) / features['play_count']
    features['share_ratio'] = features['share_count'] / features['play_count']
    features['comment_ratio'] = features['comment_count'] / features['play_count']
    
    # Características temporales
    features['time_since_post'] = (datetime.now() - pd.to_datetime(df['create_time'])).dt.total_seconds()
    
    return features

def train_model():
    # Cargar datos de ejemplo (reemplazar con datos reales)
    X = np.random.rand(1000, 150)  # Aumentado a 150 características
    y = np.random.randint(0, 2, size=(1000,))
    
    # Dividir datos
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # Escalar datos
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Crear y entrenar modelo
    model = create_model()
    model.fit(
        X_train, y_train,
        epochs=20,  # Aumentado el número de épocas
        batch_size=32,
        validation_data=(X_test, y_test),
        callbacks=[
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True
            )
        ]
    )
    
    # Guardar modelo y scaler
    model.save('viralidad_model.h5')
    joblib.dump(scaler, 'scaler.pkl')
    
    return model, scaler

if __name__ == '__main__':
    model, scaler = train_model()
    print("Modelo entrenado y guardado exitosamente") 