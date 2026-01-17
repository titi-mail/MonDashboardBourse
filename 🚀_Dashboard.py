# ----------------------------------------
# --- Création de la page Dashboard.py ---
# ----------------------------------------
"""

Sommaire du fichier : 

    - 00.1 - Importation des librairies
    - 00.2 - Importation de nos fonctions
    - 00.3 - Réglage de notre page
    - 1 - BARRE LATÉRALE DE RECHERCHE
    - 2 - AFFICHAGE PRINCIPAL

"""
# -----------------------------------------
# --- 00.1 - Importation des librairies ---
# -----------------------------------------
import streamlit as st
import yfinance as yf
from streamlit_searchbox import st_searchbox

# -------------------------------------------
# --- 00.2 - Importation de nos fonctions ---
# -------------------------------------------
from utils.Barre_de_recherche import search_wrapper
from utils.Styles import style_CSS
from utils.Fonctions_Autre import get_currency_symbol, translate_sector
from utils.Indicateurs import calculate_rsi, calculate_ytd_performance
from utils.Graphiques import create_gauge

# ------------------------------------
# --- 00.3 - Réglage de notre page ---
# ------------------------------------
st.set_page_config(page_title="Dashboard", page_icon="🚀", layout="wide") 
st.title("Dashboard")
style_CSS() # Application de notre style CSS

# ---------------------------------------
# --- 1 - BARRE LATÉRALE DE RECHERCHE ---
# ---------------------------------------
with st.sidebar:
    st.header("Chercher un actif")
    
    # Utilisation de notre fonction wrapper
    selected_ticker = st_searchbox(
        search_wrapper, 
        key="asset_search_box",
        placeholder="Rechercher...",
        clear_on_submit=False
    )

# -------------------------------
# --- 2 - AFFICHAGE PRINCIPAL ---
# -------------------------------
if selected_ticker:
    # Appel à yfinance pour vérifier que tout marche
    with st.spinner('Chargement des données...'):
        try:
            stock = yf.Ticker(selected_ticker)
            info = stock.info # On récupère toutes les infos de l'actif (ticker) sélectionné
            
            # --------------------------------------------------
            # --- RÉCUPÉRATION INFORMATIONS (PRÉ-TRAITEMENT) ---
            # --------------------------------------------------
            # - 1. Prix et Devise -
            price = info.get('currentPrice', info.get('regularMarketPrice'))
            currency_code = info.get('currency', 'USD')
            symbole = get_currency_symbol(currency_code)

            # - 2. Performance YTD (Année en cours) - 
            ytd_perf = calculate_ytd_performance(stock, price)

            # -----------------
            # --- AFFICHAGE ---
            # -----------------
            # -------------------------------------------------
            # --- Premier bandeau de données : Nom, secteur ---
            # -------------------------------------------------
            nom = info.get('shortName', selected_ticker).upper() # Nom de l'actif transformé en majuscule
            secteur = translate_sector(info.get('sector', 'Indéfini')) # Récupération et traduction du secteur d'activité (utilisation de notre fonction)
            st.markdown(f"""
                <b><span style='color: #FFFFFF; font-size: 2em'> {nom} </b>
                <i><span style='color: #B2B5BE; font-size: 1.5em'> - {secteur} 
                        """, unsafe_allow_html=True)
            
            # ------------------------------------------------------------------------
            # --- Deuxième bandeau de données : Prix/variation YTD, Capitalisation ---
            # ------------------------------------------------------------------------
            c1, c2, c_vide = st.columns([1.5, 1.5, 7])
            # Colonne 1 : Prix avec variation colorée (Delta)
            c1.metric(
                label="Prix",
                value=f"{price} {symbole}", 
                delta=f"{ytd_perf:.2f} % (YTD)" # Attention streamlit gère le rouge/vert automatiquement ici
            )
            # Colonne 2 : Capitalisation 
            mcap = info.get('marketCap', 0)
            c2.metric("Capitalisation", f"{mcap / 1e9:.1f} Md {symbole}")

            # ---------------------------------------------------------------
            # --- Troisième bandeau de données : Jauges : PER, PEG, P/FCF ---
            # ---------------------------------------------------------------
            col_g1, col_g2, col_g3 = st.columns(3)

            # --- JAUGE 1 : PER ---
            # Récupération de la valeur du PER
            per_val = info.get('trailingPE', 0) 
            if per_val is None: per_val = 0 # on met 0 si l'info est absente (None)

            # Ajout des bornes de seuil PER en fonction des secteurs 
            SECTOR_PER_THRESHOLDS = {
                "Technology": [20, 35],
                "Financial Services": [12, 18],
                "Healthcare": [15, 25],
                "Consumer Cyclical": [15, 25],
                "Consumer Defensive": [18, 25],
                "Industrials": [12, 20],
                "Energy": [10, 15],
                "Real Estate": [12, 20],
                "Basic Materials": [10, 15],
                "Utilities": [12, 18]
            }
            thresholds = SECTOR_PER_THRESHOLDS[info.get('sector', 'Indéfini')]

            with col_g1:
                # Création de la jauge à partir de notre fonction 
                fig_per, color_per = create_gauge(
                    value=per_val,
                    title="PER",
                    min_val=0,
                    max_val=40,
                    thresholds=thresholds,
                    metric_mode="lower_is_better" # Indicateur à minimiser
                )
                st.plotly_chart(fig_per, use_container_width=True, config={'displayModeBar': False})
                # Détermination du texte 
                if per_val == 0:
                     status = "(Non rentable)"
                elif color_per == "#37C36C": # Vert = bon marché
                    status = "(Bon marché)"
                elif color_per == "#FACF3D": # Jaune = correct
                    status = "(Correct)"
                else:
                    status = "(Cher)"
                # Affichage du texte de statut coloré sous la jauge
                st.markdown(f"""
                    <div style='text-align: center; color: {color_per}; margin-top: -15px; font-size: 14px;'>
                        {status}
                    </div>
                    """, unsafe_allow_html=True)
                        
        except Exception as e:
            st.error(f"Erreur de chargement des détails : {e}")

else:
    st.info("👈 Commencez à taper dans la barre latérale.")


