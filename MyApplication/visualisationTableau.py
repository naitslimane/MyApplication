import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Connexion à la base de données
conn = sqlite3.connect('ma_base.db')


# Fonction pour récupérer les données du client pour une année donnée
def get_customer_data_for_year(client_id, year):
    query = f"SELECT * FROM ma_table WHERE client_id={client_id} AND strftime('%Y', date)='{year}'"
    data = pd.read_sql(query, conn)
    return data


# Fonction pour calculer les consommations mensuelles pour une année donnée
def get_monthly_consumptions_for_year(data):
    monthly_consumptions = data.groupby(['annee', 'mois'])['valeur'].sum()
    return monthly_consumptions


# Interface Streamlit
st.title('Visualisation des consommations des clients par année')

# Sélection de l'id du client
client_id = st.text_input('Entrez l\'ID du client')

# Sélection de l'année
now = datetime.now()
selected_year = st.selectbox('Sélectionnez une année', range(now.year - 17, now.year + 1))

if client_id:
    # Récupération des données du client pour l'année sélectionnée
    data = get_customer_data_for_year(client_id, str(selected_year))

    # Ajout des colonnes 'annee' et 'mois' à partir de la colonne 'date'
    data['annee'] = pd.DatetimeIndex(data['date']).year
    data['mois'] = pd.DatetimeIndex(data['date']).month

    # Calcul des consommations mensuelles pour l'année sélectionnée
    monthly_consumptions = get_monthly_consumptions_for_year(data)

    # Affichage des consommations annuelles et mensuelles
    st.write(f'Consommations pour l\'année {selected_year} :')
    st.write(monthly_consumptions)
