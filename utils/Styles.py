import streamlit as st

def style_CSS():
    """
    Fonction qui injecte le CSS personnalisé pour le thème sombre "Pro".
    """
    st.markdown("""
    <style>
        /* Fond principal de l'application (Gris très foncé / Bleu nuit) */
        .stApp {
            background-color: #131722;
        }
        
        /* Fond de la barre latérale */
        [data-testid="stSidebar"] {
            background-color: #1E222D;
        }
        
        /* Titres en blanc cassé */
        h1, h2, h3 {
            color: #E0E3EB !important;
            font-family: 'Helvetica Neue', sans-serif;
        }

        /* Métriques (Gros chiffres) */
        [data-testid="stMetricValue"] {
            color: #FFFFFF !important;
            font-size: 26px;
        }
        [data-testid="stMetricLabel"] {
            color: #B2B5BE !important;
        }
        
        /* Cacher/Colorer le bandeau du haut (Header) */
        header[data-testid="stHeader"] {
            background-color: #131722 !important; /* Même couleur que le fond */
        }

        /* Remonter tout le contenu vers le haut */
        /* Streamlit met par défaut un gros padding en haut, on le réduit */
        .block-container {
            padding-top: 3rem !important; 
            padding-bottom: 1rem !important;
        }
        
        /* Cacher le menu Hamburger et le bouton Deploy */
        /* #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        */            

    </style>
    """, unsafe_allow_html=True)