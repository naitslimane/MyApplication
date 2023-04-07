import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import ParameterGrid

# Fonction pour préparer les données
def prepare_data(data, timesteps):
    X, y = [], []
    for i in range(len(data)-timesteps-1):
        X.append(data[i:(i+timesteps), 0])
        y.append(data[i+timesteps, 0])
    return np.array(X), np.array(y)

# Fonction pour entraîner et évaluer un modèle LSTM
def train_model(X_train, y_train, X_test, y_test, timesteps, batch_size, epochs):
    model = Sequential()
    model.add(LSTM(50, input_shape=(timesteps, 1)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    early_stop = EarlyStopping(monitor='loss', patience=5, verbose=1)
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, callbacks=[early_stop], verbose=0)
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    return model, rmse

# Fonction pour effectuer une recherche en grille pour les paramètres LSTM optimaux
def grid_search(X_train, y_train, X_test, y_test):
    batch_sizes = [16, 32, 64]
    timesteps = [30, 60, 90]
    epochs = [50, 100, 150]
    param_grid = {'batch_size': batch_sizes, 'timesteps': timesteps, 'epochs': epochs}
    grid = ParameterGrid(param_grid)
    best_rmse = float('inf')
    best_params = None
    for params in grid:
        batch_size = params['batch_size']
        timesteps = params['timesteps']
        epochs = params['epochs']
        X_train_lstm = np.reshape(X_train, (X_train.shape[0], timesteps, 1))
        X_test_lstm = np.reshape(X_test, (X_test.shape[0], timesteps, 1))
        _, rmse = train_model(X_train_lstm, y_train, X_test_lstm, y_test, timesteps, batch_size, epochs)
        if rmse < best_rmse:
            best_rmse = rmse
            best_params = params
    return best_params

# Connexion à la base de données
conn = sqlite3.connect('ma_base.db')
cursor = conn.cursor()

# Chargement des données
cursor.execute("SELECT * FROM ma_table")
data = cursor.fetchall()
data = pd.DataFrame(data, columns=['client_id', 'date', 'valeur', 'City', 'name', 'Latitude', 'Longitude'])
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)

# Prétraitement des données
scaler = MinMaxScaler(feature_range=(0,1))
data_scaled = scaler.fit_transform(data[['valeur']])

# Sélection de l'ID
client_ids = data['client_id'].unique().tolist()
selected_id = st.selectbox('Sélectionnez l\'ID du client', client_ids)

# Préparation des données pour le modèle LSTM
# Lecture des données de la base de données
df = pd.read_sql_query("SELECT * FROM ma_table", conn)

# Récupération des IDs des clients
clients = pd.read_sql_query("SELECT DISTINCT client_id FROM ma_table", conn)

# Sélection de l'ID du client via une liste déroulante
selected_client = st.selectbox('Sélectionnez un client', clients['client_id'])

# Extraction des données du client sélectionné
df_client = df[df['client_id'] == selected_client].reset_index(drop=True)


timesteps = 30 # Paramètre à optimiser avec la fonction grid_search
batch_size = 64 # Paramètre à optimiser avec la fonction grid_search
epochs = 100 # Paramètre à optimiser avec la fonction grid_search

X, y = prepare_data(df_client, timesteps)
X_train, y_train = X[:-60], y[:-60] # Utilisez les 60 derniers mois pour la validation
X_test, y_test = X[-60:], y[-60:]


# Optimisation des paramètres LSTM
best_params = grid_search(X_train, y_train, X_test, y_test)
timesteps = best_params['timesteps']
batch_size = best_params['batch_size']
epochs = best_params['epochs']

# Entraînement et évaluation du modèle LSTM avec les meilleurs paramètres
X_train_lstm = np.reshape(X_train, (X_train.shape[0], timesteps, 1))
X_test_lstm = np.reshape(X_test, (X_test.shape[0], timesteps, 1))
model, rmse = train_model(X_train_lstm, y_train, X_test_lstm, y_test, timesteps, batch_size, epochs)

# Préparation des données pour la prédiction
last_data_point = df_client[-timesteps:]
predictions = []
for i in range(60):
    x_test = np.reshape(last_data_point, (1, timesteps, 1))
    predicted_value = scaler.inverse_transform(model.predict(x_test))
    predictions.append(predicted_value[0][0])
    last_data_point = np.append(last_data_point[:,1:,:],[[[predicted_value[0][0]/data['valeur'].max()]]],axis=1)

# Préparation des données pour l'affichage
date_range = pd.date_range(df_client.index[-1], periods=61, freq='M')[1:]
predictions = pd.DataFrame(predictions, index=date_range, columns=['valeur'])

# Affichage des résultats
st.title('Prévision de la consommation d\'énergie')
st.write('ID du client :', selected_id)
st.write('RMSE :', rmse)
st.line_chart(df_client.append(predictions))
st.write('La consommation d\'énergie prévue pour les 12 prochains mois est de : ')
st.write(predictions)