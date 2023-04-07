import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def main():

   # Connexion à la base de données
  conn = sqlite3.connect('ma_base.db')

   # Chargement des données dans un dataframe Pandas
  df = pd.read_sql_query("SELECT *, strftime('%Y-%m', date) as mois FROM ma_table", conn, parse_dates=['date'])

   # Sélection du premier mois
  month1 = st.sidebar.selectbox("Sélectionnez un premier mois :", df['mois'].unique())

   # Filtrage des données pour n'afficher que celles du premier mois sélectionné
  df_month1 = df[df['mois'] == month1]

   # Conversion de la colonne de dates en un objet DatetimeIndex
  df_month1 = df_month1.set_index('date')

  # Extraction des données pour le premier mois sélectionné
  data_month1 = df_month1['valeur']

  # Sélection du deuxième mois
  month2 = st.sidebar.selectbox("Sélectionnez un deuxième mois :", df['mois'].unique())

  # Filtrage des données pour n'afficher que celles du deuxième mois sélectionné
  df_month2 = df[df['mois'] == month2]

  # Conversion de la colonne de dates en un objet DatetimeIndex
  df_month2 = df_month2.set_index('date')

  # Extraction des données pour le deuxième mois sélectionné
  data_month2 = df_month2['valeur']

  # Graphique de comparaison des deux mois
  fig, ax = plt.subplots()
  ax.plot(data_month1, label=month1)
  ax.plot(data_month2, label=month2)
  ax.set_title("Comparaison de la consommation pour deux mois")
  ax.set_xlabel("Jour")
  ax.set_ylabel("Consommation (kWh)")
  ax.legend()
  st.pyplot(fig)

  # Calcul de la différence de consommation entre les deux mois
  diff = data_month2.sum() - data_month1.sum()

  # Affichage de la différence de consommation
  st.write(f"Il y a une différence de {diff} kWh de consommation entre {month1} et {month2}.")


if __name__ == '__main__':
    main()
