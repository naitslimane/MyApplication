import sqlite3
import streamlit as st
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import folium


# Connection à la base de données SQLite3
conn = sqlite3.connect('ma_base.db')
c = conn.cursor()

# Fonction pour récupérer les informations de géolocalisation du client
def get_client_location(client_id):
    c.execute("SELECT Latitude, Longitude FROM ma_table WHERE client_id=?", (client_id,))
    result = c.fetchone()
    return result

# Création de la carte centrée sur l'Algérie
carte = folium.Map(location=[36.7602, 5.0554], zoom_start=10)

# Affichage de la carte dans le navigateur
carte.save('bejaia.html')


# Récupération de l'id du client saisi par l'utilisateur
client_id = st.text_input('Saisir l\'ID du client :')

# Si l'utilisateur a saisi un ID de client, on affiche la localisation du client sur la carte
if client_id:
    client_location = get_client_location(client_id)
    if client_location:
        folium.Marker(location=client_location, tooltip="Client").add_to(carte)
    else:
        st.warning("Le client n'a pas de géolocalisation enregistrée dans la base de données.")

# Affichage de la carte
st.write(carte._repr_html_(), unsafe_allow_html=True)

# Fermeture de la connexion à la base de données
conn.close()
