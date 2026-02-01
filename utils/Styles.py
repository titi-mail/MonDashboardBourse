import streamlit as st

def style_CSS():
    """
    Fonction qui injecte le CSS personnalisé pour le thème sombre "Pro".
    """
    st.markdown("""
    <style>
        /* ----------------------------------------- */
        /* --- 1. CONFIGURATION GÉNÉRALE (Fonds) --- */
        /* ----------------------------------------- */
        
        .stApp {
            background-color: #131722;
        }
        
        [data-testid="stSidebar"] {
            background-color: #1E222D;
        }
        
        header[data-testid="stHeader"] {
            background-color: #131722 !important;
        }

        .block-container {
            padding-top: 3rem !important; 
            padding-bottom: 1rem !important;
        }

        /* -------------------------------------- */
        /* --- 2. TEXTES ET TITRES PRINCIPAUX --- */
        /* -------------------------------------- */

        h1, h2, h3 {
            color: #E0E3EB !important;
            font-family: 'Helvetica Neue', sans-serif;
        }

        p, div, span {
            color: #E0E0E0;
        }

        .stCaption, [data-testid="stCaptionContainer"] {
            color: #B2B5BE !important;
        }

        /* ------------------------------------------------------ */
        /* --- 3. ÉLÉMENTS SPÉCIFIQUES (Métriques, Expanders) --- */
        /* ------------------------------------------------------ */

        [data-testid="stMetricValue"] {
            color: #FFFFFF !important;
            font-size: 26px;
        }
        [data-testid="stMetricLabel"] {
            color: #B2B5BE !important;
        }

        /* ============================================================ */
        /* === CORRECTION EXPANDER (BORDURES ET FONDS) === */
        /* ============================================================ */
        
        /* 1. La barre de titre de l'expander (Fermé ou Ouvert) */
        .streamlit-expanderHeader {
            background-color: #2A2E39 !important; /* Fond gris moyen */
            color: #FFFFFF !important;            /* Texte Blanc */
            border: 1px solid #383F50 !important; /* BORDURE GRISE (et non blanche !) */
            border-radius: 5px;
        }
        
        /* 2. Au survol et au clic (Focus) */
        /* On force la bordure à rester grise, et le fond à rester sombre */
        .streamlit-expanderHeader:hover, 
        .streamlit-expanderHeader:focus, 
        .streamlit-expanderHeader:active {
            background-color: #383F50 !important; /* Un peu plus clair au survol */
            color: #FFFFFF !important;
            border: 1px solid #4A5568 !important; /* Bordure légèrement plus claire mais pas blanche */
        }

        /* 3. Le contenu à l'intérieur (Le tableau) */
        .streamlit-expanderContent {
            background-color: #1E222D !important;
            color: #E0E0E0 !important;
            border: 1px solid #383F50 !important; /* BORDURE GRISE */
            border-top: none !important; /* Pas de double bordure avec le titre */
            border-bottom-left-radius: 5px;
            border-bottom-right-radius: 5px;
        }
        
        /* 4. Enlever la bordure par défaut du conteneur parent (details) */
        details {
            border: none !important;
        }

        /* ----------------------------------- */
        /* --- 4. BARRE LATÉRALE (SIDEBAR) --- */
        /* ----------------------------------- */
        
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div {
            color: #E0E0E0 !important;
        }

        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            color: #FFFFFF !important;
        }

        [data-testid="stSidebar"] label {
            color: #B2B5BE !important;
            font-weight: bold;
        }

        [data-testid="stSidebar"] .stRadio label p {
            color: #E0E0E0 !important;
            font-size: 15px;
        }
        
        [data-testid="stSidebar"] input {
            color: #FFFFFF !important;
            background-color: #2A2E39 !important;
        }

        /* ----------------------------------- */
        /* --- 5. TABLEAUX (DATAFRAMES)    --- */
        /* ----------------------------------- */

        [data-testid="stDataFrame"] th {
            background-color: #2A2E39 !important;
            color: #FFFFFF !important;
            border-bottom: 1px solid #383F50 !important;
        }

        [data-testid="stDataFrame"] {
            border: none !important;
        }

        [data-testid="stDataFrame"] > div {
            background-color: transparent !important;
        }

    </style>
    """, unsafe_allow_html=True)