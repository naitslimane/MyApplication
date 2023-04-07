import streamlit as st
import sqlite3


def main():


  conn = sqlite3.connect('ma_base.db')
  cur = conn.cursor()

# Interface utilisateur Streamlit

  st.title("Visualisation des consommations annuelles et mensuelles des clients")

# Saisie de l'ID du client
  client_id = st.number_input("Saisir l'ID du client")

# Récupération des consommations annuelles du client
  cur.execute("SELECT strftime('%Y', date), SUM(valeur) FROM ma_table WHERE client_id = ? GROUP BY strftime('%Y', date)", (client_id,))
  rows_an = cur.fetchall()

# Récupération des consommations mensuelles du client
  cur.execute("SELECT strftime('%Y-%m', date), SUM(valeur) FROM ma_table WHERE client_id = ? GROUP BY strftime('%Y-%m', date)", (client_id,))
  rows_mois = cur.fetchall()

# Affichage des consommations annuelles sous forme de tableau
  if rows_an:
    st.write(f"Consommations annuelles du client {client_id}")
    st.table(rows_an)
  else:
    st.warning(f"Aucune consommation annuelle trouvée pour le client {client_id}")

# Affichage des consommations mensuelles sous forme de tableau
  if rows_mois:
    st.write(f"Consommations mensuelles du client {client_id}")
    st.table(rows_mois)
  else:
    st.warning(f"Aucune consommation mensuelle trouvée pour le client {client_id}")

# Fermeture de la connexion à la base de données
  cur.close()
  conn.close()

if __name__ == '__main__':
    main()


    # votre code de visualisation ici
