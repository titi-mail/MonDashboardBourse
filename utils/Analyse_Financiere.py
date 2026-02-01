# -----------------------------------------------
# --- Création de l'onglet analyse financière ---
# -----------------------------------------------

"""

Sommaire : 

    - Partie 1 -> Rentabilité : marge nette, ROE, ROIC

"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def safe_get(data, key, default=0):
    """Récupère une valeur en sécurité (évite les crashs si None)"""
    val = data.get(key)
    return val if val is not None else default

def get_safe_row(df, possible_names, fill=0):
    """Récupère une ligne dans un DataFrame avec plusieurs noms possibles."""
    for name in possible_names:
        if name in df.index:
            return df.loc[name]
    return pd.Series(fill, index=df.columns)

def style_financial_dataframe(df):
    # Convertir en string formaté pourcentage (cela force l'alignement centré)
    df_str = df.applymap(lambda x: f"{x:.1%}" if pd.notnull(x) else "")

    # Créer un style centré
    return (
        df_str.style
        .set_properties(**{'text-align': 'center'}) 
        .set_table_styles([
            {'selector': 'th', 'props': [('text-align', 'center')]} 
        ])
    )





def calculate_cagr(start_val, end_val, years):
    """Calcule le taux de croissance annuel moyen"""
    if start_val == 0 or years == 0:
        return 0
    # On gère le cas où les valeurs sont négatives (mathématiquement complexe pour CAGR, on simplifie)
    if start_val < 0 and end_val > 0:
        return ((end_val - start_val) / abs(start_val)) / years # Approximation linéaire
    try:
        return (end_val / start_val) ** (1 / years) - 1
    except:
        return 0

def prepare_chart_data(stock, statement_type, row_names):
    """
    Prépare les données : 4 dernières années annuelles + LTM (Last Twelve Months)
    Retourne: dates (liste), valeurs (liste), cagr (float)
    """
    try:
        # Choix du tableau financier
        if statement_type == 'financials':
            annual = stock.financials
            quarterly = stock.quarterly_financials
        elif statement_type == 'cashflow':
            annual = stock.cashflow
            quarterly = stock.quarterly_cashflow
        else:
            return [], [], 0

        # Récupération de la ligne (sécurisée)
        row_annual = get_safe_row(annual, row_names)
        row_quarterly = get_safe_row(quarterly, row_names)

        # 1. Données Annuelles (On inverse pour avoir l'ordre chrono : 2020 -> 2023)
        # On prend les 4 dernières années complètes
        hist_data = row_annual.iloc[:4][::-1] 
        
        # 2. Calcul du LTM (Somme des 4 derniers trimestres)
        ltm_value = row_quarterly.iloc[:4].sum()
        
        # Construction des listes X et Y
        dates = [d.strftime('%Y') for d in hist_data.index] + ['LTM']
        values = list(hist_data.values) + [ltm_value]
        
        # Calcul du CAGR sur 4 ans (entre la 1ère année affichée et le LTM)
        if len(values) >= 2:
            cagr = calculate_cagr(values[0], values[-1], len(values)-1)
        else:
            cagr = 0
            
        return dates, values, cagr
        
    except Exception as e:
        return [], [], 0

def create_bar_chart(title, dates, values, cagr, color, unit="Mds $"):
    """Crée le graphique Plotly style 'Carte'"""
    
    # Couleur du CAGR (Vert si positif, Rouge si négatif)
    cagr_color = "#4CAF50" if cagr >= 0 else "#FF5252"
    cagr_txt = f"+{cagr:.1%}" if cagr >= 0 else f"{cagr:.1%}"

    fig = go.Figure(data=[
        go.Bar(
            x=dates, 
            y=values,
            marker_color=color,
            text=[f"{v/1e9:.1f}" if abs(v) > 1e9 else f"{v:.2f}" for v in values], # Texte sur les barres
            textposition='auto',
        )
    ])

    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b> <br><span style='font-size:14px; color:{cagr_color};'>CAGR 5 ans: {cagr_txt}</span>",
            font=dict(size=20)
        ),
        paper_bgcolor='rgba(0,0,0,0)', # Fond transparent
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=50, b=10),
        height=250,
        yaxis=dict(showgrid=False, visible=False), # On cache l'axe Y pour faire propre
        xaxis=dict(showgrid=False),
        dragmode=False
    )
    return fig












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

    # ==============================================================================
    # 1. RENTABILITÉ (MARGE, ROE, ROIC)
    # ==============================================================================
    st.subheader("1️⃣ Rentabilité")

    # --- A. AFFICHAGE DES 3 INDICATEURS CLÉS ---
    col1, col2, col3 = st.columns(3)

    # 1. Marge Nette
    col1.metric(
        label="Marge Nette", 
        value=f"{net_margin:.1%}",
        help="TTM (12 mois glissant)"
    )
    # 2. ROE
    col2.metric(
        label="ROE", 
        value=f"{roe:.1%}",
        help="TTM (12 mois glissant)"
    )
    # 3. ROIC
    col3.metric(
        label="ROIC (Global)", 
        value="XX",
        help=""
    )

    st.write("") 

    # ---------------------------------
    # Création des tableaux historiques 
    # ---------------------------------
    try:
        # Récupération des données brutes
        fin = stock.financials
        bs = stock.balance_sheet
        q_fin = stock.quarterly_financials
        q_bs = stock.quarterly_balance_sheet

        # --- 1. HISTORIQUE ANNUEL ---
        with st.expander("Historique annuel", expanded=False):
            if not fin.empty and not bs.empty:
                cols = [c for c in fin.columns if c in bs.columns]
                fin, bs = fin[cols], bs[cols]

                # Extraction 
                net_income = get_safe_row(fin, ['Net Income', 'NetIncome'])
                revenue = get_safe_row(fin, ['Total Revenue', 'Revenue', 'totalRevenue'], fill=1)
                stock_equity = get_safe_row(bs, ['Stockholders Equity', 'Total Stockholder Equity'], fill=1)

                # Création du tableau 
                df_hist = pd.DataFrame({
                    "Marge Nette": net_income / revenue,
                    "ROE": net_income / stock_equity
                }).T

                # Garder les 5 dernières années (si possible)
                df_hist = df_hist.iloc[:, :5]
                df_hist.columns = [d.strftime('%Y') for d in df_hist.columns]

                st.write(style_financial_dataframe(df_hist)) 

            else:
                st.info("Données annuelles non disponibles.")

        # --- 2. HISTORIQUE TRIMESTRIEL (TTM) ---
        with st.expander("Derniers trimestres (TTM)", expanded=False):
            if not q_fin.empty and not q_bs.empty:
                # Harmonisation sur les 4 derniers trimestres
                cols_q = q_fin.columns[:4]
                q_fin, q_bs = q_fin[cols_q], q_bs[cols_q]

                # Extraction
                net_income_q = get_safe_row(q_fin, ['Net Income', 'NetIncome'])
                revenue_q = get_safe_row(q_fin, ['Total Revenue', 'Revenue'], fill=1)
                stock_equity_q = get_safe_row(q_bs, ['Stockholders Equity', 'Total Stockholder Equity'], fill=1)

                # Création du tableau
                df_q = pd.DataFrame({
                    "Marge Nette": net_income_q / revenue_q,
                    "ROE": net_income_q / stock_equity_q
                }).T

                # Formatage Dates (Année-Mois)
                df_q.columns = [d.strftime('%b %Y') for d in df_q.columns]

                st.dataframe(style_financial_dataframe(df_q))
            else:
                st.info("Données trimestrielles non disponibles.")

    except Exception as e:
        st.error(f"Erreur lors de l'affichage des tableaux financiers : {e}")


# ==============================================================================
    # 2. CROISSANCE & DIVIDENDES (Les 4 Graphiques)
    # ==============================================================================
    st.subheader("2️⃣ Croissance & Dividendes")
    
    # --- Préparation des données pour les graphiques ---
    
    # 1. REVENUS (Bleu)
    d_rev, v_rev, cagr_rev = prepare_chart_data(stock, 'financials', ['Total Revenue', 'Revenue', 'totalRevenue'])
    
    # 2. FREE CASH FLOW (Vert)
    d_fcf, v_fcf, cagr_fcf = prepare_chart_data(stock, 'cashflow', ['Free Cash Flow', 'FreeCashFlow'])
    
    # 3. EPS / BÉNÉFICE PAR ACTION (Jaune/Orange)
    d_eps, v_eps, cagr_eps = prepare_chart_data(stock, 'financials', ['Diluted EPS', 'Basic EPS'])
    
    # 4. DIVIDENDES (Rose) - Cas particulier car stock.dividends est une série temporelle
    try:
        divs = stock.dividends
        if not divs.empty:
            # On regroupe par année
            divs_annual = divs.resample('YE').sum().sort_index(ascending=False).iloc[:4][::-1]
            # LTM Dividende (Somme des 4 derniers trimestres approx ou 365 jours)
            div_ltm = divs.last('365D').sum() if hasattr(divs, 'last') else divs.iloc[-4:].sum()
            
            d_div = [d.strftime('%Y') for d in divs_annual.index] + ['LTM']
            v_div = list(divs_annual.values) + [div_ltm]
            
            if len(v_div) >= 2:
                cagr_div = calculate_cagr(v_div[0], v_div[-1], len(v_div)-1)
            else:
                cagr_div = 0
        else:
            d_div, v_div, cagr_div = [], [], 0
    except:
        d_div, v_div, cagr_div = [], [], 0


    # --- Affichage en Grille 2x2 ---
    
    c_graph1, c_graph2 = st.columns(2)
    
    # Ligne 1
    with c_graph1:
        if d_rev:
            fig_rev = create_bar_chart("Revenus", d_rev, v_rev, cagr_rev, color="#039BE5") # Bleu
            st.plotly_chart(fig_rev, use_container_width=True, key="chart_rev")
        else:
            st.info("Revenus non disponibles")
            
    with c_graph2:
        if d_fcf:
            fig_fcf = create_bar_chart("Free Cash Flow", d_fcf, v_fcf, cagr_fcf, color="#00C853") # Vert
            st.plotly_chart(fig_fcf, use_container_width=True, key="chart_fcf")
        else:
            st.info("FCF non disponible")

    c_graph3, c_graph4 = st.columns(2)

    # Ligne 2
    with c_graph3:
        if d_div and sum(v_div) > 0:
            fig_div = create_bar_chart("Dividende / Action", d_div, v_div, cagr_div, color="#FF4081") # Rose
            st.plotly_chart(fig_div, use_container_width=True, key="chart_div")
        else:
            st.info("Pas de dividende versé")

    with c_graph4:
        if d_eps:
            fig_eps = create_bar_chart("Bénéfice par action", d_eps, v_eps, cagr_eps, color="#FFAB00") # Jaune/Or
            st.plotly_chart(fig_eps, use_container_width=True, key="chart_eps")
        else:
            st.info("EPS non disponible")

st.divider()

    
               