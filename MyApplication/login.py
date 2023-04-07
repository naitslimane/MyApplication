import streamlit as st
import sqlite3

# Connexion à la base de données SQLite
conn = sqlite3.connect('userss.db')
c = conn.cursor()

# Création de la table des utilisateurs si elle n'existe pas
c.execute('''CREATE TABLE IF NOT EXISTS userss
             (username TEXT PRIMARY KEY, password TEXT)''')

# Fonction d'inscription
def register():
    st.subheader("Inscription")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("S'inscrire",key="Sinscrire"):
        try:
            c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
            conn.commit()
            st.success("Vous êtes maintenant inscrit.")
        except:
            st.warning("Ce nom d'utilisateur existe déjà.")

# Fonction de connexion
def login():
    st.subheader("Connexion")
    username = st.text_input("Nom d'utilisateur", key='username')
    password = st.text_input("Mot de passe", type="password", key='password')
    if st.button("Se connecter", key="Seconnecter"):
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        if user:
            st.success("Vous êtes maintenant connecté.")
            session_id = st.session_state.get("session_id", 0) + 1
            st.session_state["session_id"] = session_id
            st.session_state["username"] = username
            st.session_state["password"] = password
            st.session_state["logged_in"] = True
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

# Fonction de déconnexion
def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.session_state["password"] = None
    st.success("Vous êtes maintenant déconnecté.")

# Vérification de la session utilisateur
def verify_session():
    if not st.session_state.get("logged_in"):
        st.warning("Veuillez vous connecter pour continuer.")
        st.stop()

# Page d'accueil
def home():
    st.title("Page d'accueil")
    st.write("Bienvenue, {}.".format(st.session_state["username"]))

# Barre latérale
st.sidebar.title("Menu")
if st.sidebar.button("Accueil"):
    st.session_state["page"] = "home"
if st.sidebar.button("S'inscrire"):
    st.session_state["page"] = "register"
if st.sidebar.button("Se connecter"):
    st.session_state["page"] = "login"
if st.sidebar.button("Se déconnecter"):
    logout()

# Page en fonction de la sélection dans la barre latérale
if st.session_state.get("page") == "register":
    register()
elif st.session_state.get("page") == "login":
    login()
elif st.session_state.get("page") == "logout":
    logout()
elif st.session_state.get("page") == "home":
    home()