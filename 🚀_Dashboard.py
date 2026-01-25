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
st.set_page_config(page_title="Dashboard", page_icon="🚀", layout="wide") 


import yfinance as yf
from streamlit_searchbox import st_searchbox

# -------------------------------------------
# --- 00.2 - Importation de nos fonctions ---
# -------------------------------------------
from utils.Barre_de_recherche import search_wrapper
from utils.Styles import style_CSS
from utils.Fonctions_Autre import get_currency_symbol, translate_sector
from utils.Indicateurs import calculate_ytd_performance
from utils.Graphiques import create_gauge
from utils.Analyse_Financiere import afficher_onglet_finance

# ------------------------------------
# --- 00.3 - Réglage de notre page ---
# ------------------------------------
st.title("Dashboard")
style_CSS() # Application de notre style CSS

# ---------------------------------------
# --- 1 - BARRE LATÉRALE DE RECHERCHE ---
# ---------------------------------------
with st.sidebar:
    st.header("Chercher un actif")

    selected = st_searchbox(
        search_wrapper,
        key="asset_search_box",
        placeholder="Rechercher...",
        clear_on_submit=False
    )
# Gestion anti-crash (écran blanc lors du chargement des données)
if "ticker" not in st.session_state:
    st.session_state.ticker = None

if selected and isinstance(selected, str) and selected.strip():
    st.session_state.ticker = selected.strip()

ticker = st.session_state.ticker

if not ticker:
    st.info("👈 Commencez à taper dans la barre latérale.")
    st.stop()

# ----------------------------------
# --- 2 - Chargement des données ---
# ----------------------------------
with st.spinner('Chargement des données...'):
    try:
        stock = yf.Ticker(ticker) # Appel à yfinance pour vérifier que tout marche
        info = stock.info or {} # On récupère toutes les infos de l'actif (ticker) sélectionné
        if not info:
            st.warning("Données indisponibles pour cet actif.")
            st.stop()
        # --------------------------------------------------
        # --- RÉCUPÉRATION INFORMATIONS (PRÉ-TRAITEMENT) ---
        # --------------------------------------------------
        # - 1. Prix et Devise -
        price = info.get('currentPrice', info.get('regularMarketPrice'))
        currency_code = info.get('currency', 'USD')
        symbole = get_currency_symbol(currency_code)

        # - 2. Performance YTD (Année en cours) - 
        ytd_perf = calculate_ytd_performance(stock, price)

        # - 3. Nom de l'actif + secteur
        nom = info.get("shortName", ticker).upper()
        secteur_brut = info.get("sector")
        secteur = translate_sector(secteur_brut or "Indéfini")

    except Exception as e:
        st.error(f"Erreur de chargement : {e}")
        st.stop()

# ---------------------
# --- 4 - AFFICHAGE ---
# ---------------------
# ----------------------------
# --- CRÉATION DES ONGLETS ---
# ----------------------------
tab_dashboard, tab_finance = st.tabs(["📈 Tableau de Bord", "📚 Analyse fondamentale"])
# ----------------------------------
# --- PREMIER ONGLET : DASHBOARD ---
# ----------------------------------
with tab_dashboard:
    # -------------------------------------------------
    # --- Premier bandeau de données : Nom, secteur ---
    # -------------------------------------------------
    st.markdown(f"""
        <b><span style='color: #FFFFFF; font-size: 2em'> {nom} </b>
        <i><span style='color: #B2B5BE; font-size: 1.5em'> - {secteur} 
                """, unsafe_allow_html=True)
    # ------------------------------------------------------------------------
    # --- Deuxième bandeau de données : Prix/variation YTD, Capitalisation ---
    # ------------------------------------------------------------------------
    c1, c2, c3, c4, c5 = st.columns(5)
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
    per_val = info.get('trailingPE', 0) # Récupération de la valeur du PER de la librairie de Yahoo Finance
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
    thresholds = SECTOR_PER_THRESHOLDS.get(secteur_brut, [15, 25])

    with c3:
        # Création de la jauge à partir de notre fonction 
        fig_per, color_per = create_gauge(
            value=per_val,
            title="PER TTM",
            min_val=0,
            max_val=50,
            thresholds=thresholds,
            metric_mode="lower_is_better" # Indicateur à minimiser
        )
        st.plotly_chart(fig_per, width="stretch", config={'displayModeBar': False})
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
            <b><div style='text-align: center;margin-top: -30px; font-size: 16px;'>  PER TTM </div>
            <div style='text-align: center; color: {color_per}; margin-top: -20px; font-size: 14px;'>{status}</div>
            """, unsafe_allow_html=True)
    # --- JAUGE 2 : PEG ---
    # Calcul du PEG
    peg_val = info.get("pegRatio") # On tente de récupérer le PEG officiel (Basé sur la croissance future, le plus précis)
    # Si pas dispo on le calcul à la main mais moins précis
    if peg_val is None: 
        growth = info.get("earningsGrowth") 
        if per_val and growth and growth > 0:
            peg_val = per_val / (growth * 100)
        else:
            peg_val = 0 

    PEG_THRESHOLDS = [1, 2]  # Seuils PEG :  <1 = bon marché, 1-2 = correct, >2 = cher

    with c4:
        fig_peg, color_peg = create_gauge(
            value=peg_val,
            title="PEG",
            min_val=0,
            max_val=3,
            thresholds=PEG_THRESHOLDS,
            metric_mode="lower_is_better"
        )
        st.plotly_chart(fig_peg, width="stretch", config={'displayModeBar': False})

        if peg_val == 0:
            status_peg = "(Non disponible)"
        elif color_peg == "#37C36C":
            status_peg = "(Bon marché)"
        elif color_peg == "#FACF3D":
            status_peg = "(Correct)"
        else:
            status_peg = "(Cher)"

        st.markdown(f"""
            <b><div style='text-align: center;margin-top: -30px; font-size: 16px;'>PEG</div>
            <div style='text-align: center; color: {color_peg}; margin-top: -20px; font-size: 14px;'>{status_peg}</div>
            """, unsafe_allow_html=True)

# --------------------------------------------
# --- DEUXIEME ONGLET : ANALYSE FINANCIÈRE ---
# --------------------------------------------
with tab_finance:
    afficher_onglet_finance(stock, info)





