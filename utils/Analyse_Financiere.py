# -----------------------------------------------
# --- Création de l'onglet analyse financière ---
# -----------------------------------------------

"""

Sommaire : 

    - Partie 1 -> Rentabilité : marge nette, ROE, ROIC

"""

import streamlit as st
import pandas as pd
from utils.Indicateurs import  calculate_nopat

def safe_get(data, key, default=0):
    """Récupère une valeur en sécurité (évite les crashs si None)"""
    val = data.get(key)
    return val if val is not None else default

def couleur_seuil(valeur, seuil_haut, seuil_bas):
    """Retourne la couleur et l'emoji selon tes critères (Plus c'est haut, mieux c'est)"""
    if valeur > seuil_haut: return "green", "🔥"
    elif valeur > seuil_bas: return "orange", "👍"
    else: return "red", "⚠️"

def afficher_onglet_finance(stock, info):
    
    # =========================================
    # 0. PRÉPARATION DES DONNÉES LIVE (CALCULS)
    # =========================================
    # ------------------------------
    # --- Partie 1 : Rentabilité ---
    # ------------------------------

    # Données brutes : 
    net_margin = safe_get(info, 'profitMargins', 0)
    roe = safe_get(info, 'returnOnEquity', 0)
    
    # Calcul du NOPAT (à l'aide de notre fonction)
    current_nopat, nopat_history = calculate_nopat(stock)
    # Calcul du ROIC : NOPAT / (Dette + Equity - Cash)
    total_debt = safe_get(info, 'totalDebt', 0)
    total_cash = safe_get(info, 'totalCash', 0)
    equity = safe_get(info, 'bookValue', 1) * safe_get(info, 'sharesOutstanding', 1)
    invested_capital = total_debt + equity - total_cash
    roic = (current_nopat / invested_capital) if invested_capital > 0 else 0    

    # ==============================================================================
    # 1. RENTABILITÉ (MARGE, ROE, ROIC)
    # ==============================================================================
    st.subheader("1️⃣ Rentabilité du Business")
    st.caption("Capacité de l'entreprise à générer des profits avec l'argent investi.")

    # --- A. AFFICHAGE DES 3 INDICATEURS CLÉS ---
    col1, col2, col3 = st.columns(3)

    # 1. Marge Nette
    c_nm, i_nm = couleur_seuil(net_margin, 0.25, 0.10)
    col1.metric("Marge Nette", f"{net_margin:.1%}")
    col1.markdown(f":{c_nm}[{i_nm} Rentabilité pure]")

    # 2. ROE
    c_roe, i_roe = couleur_seuil(roe, 0.20, 0.10)
    col2.metric("ROE (Actionnaires)", f"{roe:.1%}")
    col2.markdown(f":{c_roe}[{i_roe} Rendement Capitaux]")

    # 3. ROIC
    c_roic, i_roic = couleur_seuil(roic, 0.10, 0.06)
    col3.metric("ROIC (Global)", f"{roic:.1%}")
    col3.markdown(f":{c_roic}[{i_roic} Qualité Business]")

    st.write("") # Petit espace

    # --- B. TABLEAU HISTORIQUE DÉPLIANT (5 ANS) ---
    try:
        # Récupération des DataFrames financiers
        fin = stock.financials
        bs = stock.balance_sheet
        
        # On s'assure qu'on a des données
        if not fin.empty and not bs.empty:
            # On aligne les colonnes (dates) qui existent dans les deux tableaux
            cols = [c for c in fin.columns if c in bs.columns]
            fin = fin[cols]
            bs = bs[cols]

            # Extraction des séries (en gérant les clés manquantes potentielles)
            # On utilise .get() sur les lignes pour éviter les crashs si une ligne manque
            net_income = fin.loc['Net Income'] if 'Net Income' in fin.index else pd.Series(0, index=cols)
            revenue = fin.loc['Total Revenue'] if 'Total Revenue' in fin.index else pd.Series(1, index=cols)
            stock_equity = bs.loc['Stockholders Equity'] if 'Stockholders Equity' in bs.index else pd.Series(1, index=cols)
            
            # Pour le ROIC Historique
            ebit_hist = fin.loc['EBIT'] if 'EBIT' in fin.index else (fin.loc['Pretax Income'] if 'Pretax Income' in fin.index else pd.Series(0, index=cols))
            debt_hist = bs.loc['Total Debt'] if 'Total Debt' in bs.index else pd.Series(0, index=cols)
            cash_hist = bs.loc['Cash And Cash Equivalents'] if 'Cash And Cash Equivalents' in bs.index else pd.Series(0, index=cols)

            # --- CALCULS VECTORIELS (Sur toutes les années d'un coup) ---
            
            # 1. Historique Marge Nette
            hist_margin = net_income / revenue

            # 2. Historique ROE
            hist_roe = net_income / stock_equity

            # 3. Historique ROIC
            # Invested Capital = Dette + Capitaux Propres - Cash
            hist_invest_cap = debt_hist + stock_equity - cash_hist
            # NOPAT approx = EBIT * (1 - 25% tax)
            aligned_nopat = nopat_history.reindex(hist_invest_cap.index, fill_value=0)
            hist_roic = aligned_nopat / hist_invest_cap

            # --- CRÉATION DU TABLEAU ---
            # On crée un DataFrame propre
            df_hist = pd.DataFrame({
                "Marge Nette": hist_margin,
                "ROE": hist_roe,
                "ROIC": hist_roic
            })
            
            # Formatage : On transpose (Années en colonnes) pour la lisibilité
            df_final = df_hist.T 
            
            # On ne garde que les 5 premières colonnes (5 dernières années)
            df_final = df_final.iloc[:, :5]
            
            # On renomme les colonnes pour avoir juste l'année (ex: 2023)
            df_final.columns = [d.strftime('%Y') for d in df_final.columns]

            # Affichage dans l'expander
            with st.expander("📅 Voir l'historique sur 5 ans (Tableau détaillé)", expanded=False):
                st.markdown("Comparatif de la performance sur les derniers exercices :")
                # On utilise le style Pandas pour mettre en % et colorer
                st.dataframe(
                    df_final.style.format("{:.1%}")
                    .background_gradient(cmap="RdYlGn", axis=1, vmin=0.05, vmax=0.25),
                    use_container_width=True
                )
                
                # Petit commentaire automatique sur la tendance
                last_roic = df_final.iloc[2, 0] # ROIC année la plus récente
                old_roic = df_final.iloc[2, -1] # ROIC année la plus ancienne
                if last_roic > old_roic:
                    st.caption("📈 **Tendance Positive :** Le ROIC s'est amélioré sur la période.")
                else:
                    st.caption("📉 **Attention :** La rentabilité des capitaux a baissé par rapport à il y a 5 ans.")

        else:
            st.info("Historique détaillé non disponible pour cet actif.")

    except Exception as e:
        st.warning(f"Impossible de reconstituer l'historique complet ({e})")

    st.divider()

    st.caption("""
    Liste des choses à faire et effectuées lors des derniers travaux : 
        - Le calcul de la marge nette et du ROE est bon
        - Cependant le résultat du ROIC n'est pas bon, il faut le retravailler et chercher à trouver le même résultat que la fiche de NVIDIA de l'analyste currieux (71.9%) en 2025.
            -> https://analystecurieux.fr/articles/nvidia-2025-11-23-9360
    Ensuite il faut bien que je comprenne comment ces indicateurs fonctionnent (mettre des clés de lectures ...)
               """)
    
               