import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px


conn = sqlite3.connect('ma_base.db')
c = conn.cursor()


# Requête pour récupérer les données de consommation d'électricité avec la colonne "date"
query1 = "SELECT * FROM ma_table"
df_consommation = pd.read_sql(query1, conn)

# Création de deux nouvelles colonnes "année" et "mois" à partir de la colonne "date"
df_consommation["année"] = pd.DatetimeIndex(df_consommation["date"]).year
df_consommation["mois"] = pd.DatetimeIndex(df_consommation["date"]).month_name()

# Fonction pour récupérer le nombre total de clients
def get_total_customers():
    c.execute('SELECT COUNT(DISTINCT client_id) FROM ma_table')
    total_customers = c.fetchone()[0]
    return total_customers

# Requête pour récupérer le nombre total de consommations d'électricité
query3 = "SELECT COUNT(valeur) FROM ma_table"
nombre_consommations = c.execute(query3).fetchone()[0]

# Création d'un DataFrame pour les statistiques annuelles de la consommation d'électricité
df_consommation_annuelle = df_consommation.groupby('année').sum().reset_index()

# Création d'un line graph pour les statistiques annuelles de la consommation d'électricité
fig1 = px.line(df_consommation_annuelle, x='année', y='valeur', title='Statistiques annuelles de la consommation d\'électricité en graphique linéaire')

# Création d'un bar graph pour les statistiques annuelles de la consommation d'électricité
fig2 = px.bar(df_consommation_annuelle, x='année', y='valeur', title='Statistiques annuelles de la consommation d\'électricité en graphique à barres')

# Création d'un DataFrame pour les statistiques mensuelles de la consommation d'électricité
df_consommation_mensuelle = df_consommation.groupby(['mois']).sum().reset_index()

# Affichage du tableau de bord
st.title("Dashboard")

# Affichage du nombre total de clients
total_customers = get_total_customers()
st.write(f'Nombre total de clients : {total_customers}')

st.write(f'Nombre total des consommations : {nombre_consommations}')
st.plotly_chart(fig1)
st.plotly_chart(fig2)


 # Fermeture de la connexion à la base de données SQLite
c.close()
conn.close()