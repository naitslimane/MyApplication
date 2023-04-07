import sqlite3
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Connexion à la base de données SQLite3
conn = sqlite3.connect('ma_base.db')


# Fonction pour récupérer les données de consommation pour un client donné
def get_data(client_id):
    query = f"SELECT * FROM ma_table WHERE client_id = '{client_id}'"
    data = pd.read_sql_query(query, conn, parse_dates=['date'], index_col='date')
    return data


# Fonction pour prédire la consommation future pour un client donné
def predict_future_consumption(data):
    # Modèle SARIMA
    model = SARIMAX(data, order=(1, 0, 0), seasonal_order=(1, 1, 0, 12))
    result = model.fit()

    # Prédiction des données futures pour les 5 prochaines années
    future_data = result.predict(start=len(data), end=len(data) + 59, dynamic=False)
    future_data.index = pd.date_range(start=data.index[-1], periods=60, freq='M')

    return future_data


# Fonction principale de l'application Streamlit
def main():
    # En-tête de l'application
    st.title("Prédiction de la consommation future des clients")

    # Sélection de l'ID du client
    client_id = st.selectbox("Sélectionner l'ID du client :",
                             ["Client 1", "Client 2", "Client 3", "Client 4", "Client 5"])

    # Récupérer les données de consommation pour le client sélectionné
    data = get_data(client_id)

    # Prédiction de la consommation future pour le client sélectionné
    future_data = predict_future_consumption(data)

    # Affichage des résultats
    st.subheader(f"Prédiction de la consommation future pour le client {client_id}")

    # Graphique des données prévues
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(future_data, label='Données prévues')
    ax.legend()
    ax.set_xlabel('date')
    ax.set_ylabel('valeur')
    st.pyplot(fig)

    # Tableau des données prévues
    st.subheader("Données prévues")
    st.write(future_data)


# Lancement de l'application Streamlit
if __name__ == '__main__':
    main()
