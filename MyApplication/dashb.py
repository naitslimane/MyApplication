import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
def main():
# Connexion à la base de données SQLite
 conn = sqlite3.connect('ma_base.db')
 cur = conn.cursor()

# Requête pour récupérer les données de consommation d'électricité avec la colonne "date"
 query1 = "SELECT * FROM ma_table"
 df_consommation = pd.read_sql(query1, conn)

# Création de deux nouvelles colonnes "année" et "mois" à partir de la colonne "date"
 df_consommation["année"] = pd.DatetimeIndex(df_consommation["date"]).year
 df_consommation["mois"] = pd.DatetimeIndex(df_consommation["date"]).month_name()

# Exécution de la commande SQL pour calculer la somme des clients
 cur.execute("SELECT SUM(client_id) FROM ma_table")

# Récupération du résultat
 result = cur.fetchone()

# Requête pour récupérer le nombre total de consommations d'électricité
 query3 = "SELECT COUNT(valeur) FROM ma_table"
 nombre_consommations = cur.execute(query3).fetchone()[0]

# Création d'un DataFrame pour les statistiques annuelles de la consommation d'électricité
 df_consommation_annuelle = df_consommation.groupby('année').sum().reset_index()


# Création d'un line graph pour les statistiques annuelles de la consommation d'électricité
 fig1 = px.line(df_consommation_annuelle, x='année', y='valeur', title='Statistiques annuelles de la consommation d\'électricité en graphique linéaire')

# Création d'un bar graph pour les statistiques annuelles de la consommation d'électricité
 fig2 = px.bar(df_consommation_annuelle, x='année', y='valeur', title='Statistiques annuelles de la consommation d\'électricité en graphique à barres')

# Création d'un DataFrame pour les statistiques mensuelles de la consommation d'électricité
 df_consommation_mensuelle = df_consommation.groupby(['année', 'mois']).sum().reset_index()

# Affichage du tableau de bord
 st.title("Dashboard")

# Affichage du nombre total de clients et de consommations d'électricité annuelles et mensuelles
 st.write("Somme des clients : ", result[0])
#st.write(f'Nombre total de clients : {nombre_clients}')
 st.write(f'Nombre total des consommations : {nombre_consommations}')
 st.plotly_chart(fig1)
 st.plotly_chart(fig2)


# Fermeture de la connexion à la base de données SQLite
 cur.close()
 conn.close()

if __name__ == '__main__':
    main()