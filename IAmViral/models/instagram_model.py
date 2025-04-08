import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from datetime import datetime

def create_instagram_model():
    model = models.Sequential([
        layers.Dense(256, activation='relu', input_shape=(100,)),
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

def prepare_instagram_features(df):
    features = pd.DataFrame()
    
    # Estadísticas básicas
    features['likes'] = df['likes']
    features['comments'] = df['comments']
    features['is_video'] = df['is_video'].astype(int)
    features['video_views'] = df['video_view_count']
    
    # Calcular ratios
    features['engagement_rate'] = (features['likes'] + features['comments']) / features['likes'].max()
    features['comment_ratio'] = features['comments'] / features['likes']
    
    # Características temporales
    features['time_since_post'] = (datetime.now() - pd.to_datetime(df['timestamp'])).dt.total_seconds()
    
    # Características de texto
    features['caption_length'] = df['caption'].str.len()
    features['has_hashtags'] = df['caption'].str.contains('#').astype(int)
    
    return features

def train_instagram_model():
    # Cargar datos de ejemplo (reemplazar con datos reales)
    X = np.random.rand(1000, 100)
    y = np.random.randint(0, 2, size=(1000,))
    
    # Dividir datos
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # Escalar datos
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Crear y entrenar modelo
    model = create_instagram_model()
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
    model.save('instagram_model.h5')
    joblib.dump(scaler, 'instagram_scaler.pkl')
    
    return model, scaler

if __name__ == '__main__':
    model, scaler = train_instagram_model()
    print("Modelo de Instagram entrenado y guardado exitosamente") 