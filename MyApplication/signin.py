import streamlit as st
import sqlite3
import hashlib
import secrets
import visualisationTab
import comp
import VisualisationGraph
import dashb
import prevision

# Fonctions pour la base de données

def create_usertable():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(
        'CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, salt TEXT)')
    conn.commit()
    conn.close()


def add_userdata(username, password, salt):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users(username, password, salt) VALUES (?,?,?)', (username, password, salt))
    conn.commit()
    conn.close()


def get_userdata(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    data = c.fetchone()
    conn.close()
    return data


# Fonction de hachage de mot de passe

def hash_password(password, salt):
    hash_object = hashlib.sha256(salt.encode() + password.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig


# Fonction de création de sel

def create_salt():
    return secrets.token_hex(16)




def login():

    st.title("Page de connexion")

    # Création de la table utilisateurs
    create_usertable()

    # Création du formulaire de connexion
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type='password')

    if st.button("Se connecter"):
        user_data = get_userdata(username)
        if user_data:
            hashed_password = hash_password(password, user_data[3])
            if hashed_password == user_data[2]:
                st.success("Connecté en tant que {}".format(username))

                return True
            else:
                st.warning("Nom d'utilisateur ou mot de passe incorrect")
        else:
            st.warning("Nom d'utilisateur ou mot de passe incorrect")
            st.experimental_rerun()
    return False


# Fonction pour la page d'inscription

def signup():
    st.title("Page d'inscription")

    # Création de la table utilisateurs
    create_usertable()

    # Création du formulaire d'inscription
    new_username = st.text_input("Nom d'utilisateur", key='new_username')
    new_password = st.text_input("Mot de passe", type='password', key='new_password')

    if st.button("S'inscrire"):
        salt = create_salt()
        hashed_password = hash_password(new_password, salt)
        add_userdata(new_username, hashed_password, salt)
        st.success("Compte créé avec succès")
        st.info("Veuillez vous connecter pour accéder à l'application")

        # Une fois le compte créé, on affiche la page de connexion pour que l'utilisateur puisse se connecter
        login()
        st.experimental_rerun()


# Fonction pour la page dashboard

# Fonction pour la page dashboard

def dashboard():

    dashb.main()


    # Vérification de l'état de connexion de l'utilisateur
    is_logged_in = st.session_state.get('is_logged_in', False)

    # Si l'utilisateur n'est pas connecté, on affiche la page de connexion ou d'inscription
    if not is_logged_in:
        st.warning("Veuillez vous connecter ou vous inscrire pour accéder à l'application")

        # Affichage des boutons pour se connecter ou s'inscrire
        menu = ["Visualisation", "Comparaison", "VisualisationGraphe", "Prevision"]
        choix = st.sidebar.selectbox("Menu", menu)

        if choix == "Visualisation":
            visualisationTab.main()

        elif choix == "Comparaison":
            comp.main()
        elif choix == "VisualisationGraphe":
            VisualisationGraph.main()
        elif choix == "Prevision":
            prevision.main()

    # Si l'utilisateur est connecté, on affiche le dashboard
    else:
        # Menu de navigation
        menu = ["Visualisation", "Comparaison", "VisualisationGraphe", "Prevision"]
        choix = st.sidebar.selectbox("Menu", menu)

        if choix == "Visualisation":
            visualisationTab.main()

        elif choix == "Comparaison":
            comp.main()


        elif choix == "VisualisationGraphe":

            VisualisationGraph.main()




        elif choix == "Prevision":

            prevision.main()

            prevision.main()
            st.session_state['is_logged_in'] = False
            st.warning("Vous êtes maintenant déconnecté")
def main():
    st.set_page_config(page_title="Mon application Streamlit", page_icon=":guardsman:", layout="wide")
    st.set_option('deprecation.showfileUploaderEncoding', False)

    # Vérification de l'authentification de l'utilisateur
    if 'user' not in st.session_state:
        st.session_state['user'] = False

    # Affichage de la page de connexion si l'utilisateur n'est pas connecté
    if not st.session_state['user']:
        if login():
            st.session_state['user'] = True
        else:
            signup()

    # Si l'utilisateur est connecté, affichage du dashboard
    if st.session_state['user']:
        dashboard()

if __name__ == "__main__":
    main()
