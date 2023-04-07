import sqlite3
import pandas as pd
import streamlit as st

# Connexion à la base de données
conn = sqlite3.connect('ma_base.db')

# Chargement des données dans un dataframe Pandas
df = pd.read_sql_query("SELECT * FROM ma_table", conn)

# Sélection d'un client spécifique
client = st.sidebar.selectbox("Sélectionnez un client :", df['client_id'].unique())

# Filtre les données pour n'afficher que celles du client sélectionné
df_client = df[df['client_id'] == client]

# Conversion de la colonne de dates en un objet DatetimeIndex
df_client['date'] = pd.to_datetime(df_client['date'])
df_client = df_client.set_index('date')

# Calcul de la somme des consommations pour chaque mois
monthly_data = df_client.resample('M')['valeur'].sum()

# Calcul de la variation de consommation par rapport au mois précédent
variation = monthly_data.pct_change()

# Affichage des données mensuelles et de la variation
st.write(f"Consommation mensuelle pour le client {client} :")
st.write(monthly_data)
st.write(f"Taux de variation de consommation mensuelle pour le client {client} :")
st.write(variation)
