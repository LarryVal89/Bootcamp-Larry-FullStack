import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from datetime import datetime

def create_tiktok_model():
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
    features['digg_ratio'] = features['digg_count'] / features['play_count']
    
    # Características temporales
    features['time_since_post'] = (datetime.now() - pd.to_datetime(df['create_time'])).dt.total_seconds()
    
    # Características de texto
    features['desc_length'] = df['desc'].str.len()
    features['has_hashtags'] = df['desc'].str.contains('#').astype(int)
    features['has_mentions'] = df['desc'].str.contains('@').astype(int)
    
    # Características de música
    features['has_music'] = df['music'].notna().astype(int)
    
    return features

def train_tiktok_model():
    # Cargar datos de ejemplo (reemplazar con datos reales)
    X = np.random.rand(1000, 150)
    y = np.random.randint(0, 2, size=(1000,))
    
    # Dividir datos
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # Escalar datos
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Crear y entrenar modelo
    model = create_tiktok_model()
    model.fit(
        X_train, y_train,
        epochs=20,
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
    model.save('tiktok_model.h5')
    joblib.dump(scaler, 'tiktok_scaler.pkl')
    
    return model, scaler

if __name__ == '__main__':
    model, scaler = train_tiktok_model()
    print("Modelo de TikTok entrenado y guardado exitosamente") 