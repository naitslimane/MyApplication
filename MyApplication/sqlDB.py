import streamlit as st
import sqlite3
from datetime import datetime
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd
from pandas import datetime


# Chargement des données des clients
def parser(x):
    return datetime.strptime(x,'%m%Y')
data = pd.read_csv('ts_bruttt22.csv', sep=";",index_col=1,parse_dates=[1], squeeze=True, date_parser=parser, encoding='ISO-8859-1')
data['valeur']=data.valeur.fillna(0)

# Créer une connexion à la base de données
conn = sqlite3.connect('ma_base.db')

# Ajouter les colonnes du DataFrame à la base de données
data.to_sql('ma_table', conn, if_exists='replace', index=True)


# Fermer la connexion à la base de données
conn.close()

# Ouvrir une nouvelle connexion à la base de données
conn = sqlite3.connect('ma_base.db')

# Récupérer les données de la base de données dans un DataFrame Pandas
data = pd.read_sql('SELECT * FROM ma_table', conn)

# Fermer la connexion à la base de données
conn.close()

# Afficher les données dans Streamlit
st.write(data)
