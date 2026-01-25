# ------------------------------------------
# --- Création de nos indicateurs et KPI ---
# ------------------------------------------
import datetime
import pandas as pd

"""

Sommaire des indicateurs : 

    - calculate_rsi : RSI (14 jours)
    - calculate_ytd_performance : calcule la variation en % par rapport à la FERMETURE de l'année N-1
    - calculate_nopat : Net Operating Profit After Tax

"""


# -----------
# --- RSI ---
# -----------
def calculate_rsi(data, window=14):
    # 1. Calculer la variation de prix par rapport à la veille
    delta = data.diff()

    # 2. Séparer les gains (hausse) et les pertes (baisse)
    # Si delta > 0, c'est un gain, sinon 0
    gain = (delta.where(delta > 0, 0))
    # Si delta < 0, c'est une perte (on la met en positif), sinon 0
    loss = (-delta.where(delta < 0, 0))

    # 3. Calculer la moyenne des gains et des pertes
    # On utilise une moyenne mobile simple sur la fenêtre (14 jours)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    # 4. Calculer le RS (Relative Strength)
    rs = avg_gain / avg_loss

    # 5. Calculer le RSI final (formule standard 0 à 100)
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


# -----------
# --- YTD ---
# -----------
def calculate_ytd_performance(stock_object, current_price):
    """
    Calcule la variation en % par rapport à la FERMETURE de l'année N-1.
    Standard financier pour le calcul YTD.
    """
    try:
        # 1. Identifier les années
        today = datetime.date.today()
        current_year = today.year
        prev_year = current_year - 1
        
        # 2. On récupère un petit historique commençant fin de l'année d'avant
        # On prend large (20 décembre) pour être sûr d'avoir le dernier jour de bourse
        # même s'il y a des vacances ou des week-ends.
        start_date = f"{prev_year}-12-20"
        
        # On charge l'historique
        hist = stock_object.history(start=start_date, auto_adjust=True)
        
        if hist.empty:
            return 0.0
            
        # 3. On isole uniquement les données de l'année PRÉCÉDENTE
        # hist.index contient les dates. On filtre où l'année == prev_year
        hist_prev_year = hist[hist.index.year == prev_year]
        
        if hist_prev_year.empty:
            # Sécurité : Si l'action est trop récente (IPO cette année), 
            # on prend le tout premier prix disponible de l'année en cours (IPO price)
            reference_price = hist['Close'].iloc[0]
        else:
            # CAS STANDARD : On prend la DERNIÈRE clôture de l'année N-1
            reference_price = hist_prev_year['Close'].iloc[-1]
        
        # 4. Calcul (Prix Actuel - Prix Janvier) / Prix Janvier
        if current_price and reference_price:
            delta_percent = ((current_price - reference_price) / reference_price) * 100
            return delta_percent
            
        return 0.0
        
    except Exception as e:
        print(f"Erreur calcul YTD : {e}")
        return 0.0
    
# -------------
# --- NOPAT ---
# -------------
def calculate_nopat(stock, default_tax_rate=0.25):
    """
    Calcule le NOPAT (Net Operating Profit After Tax) en utilisant la méthode précise :
    Tax Rate = Tax Provision / Pretax Income.
    
    Retourne : 
    - current_nopat (float) : Le NOPAT de la dernière année disponible
    - nopat_history (pd.Series) : L'historique complet (Index=Date, Value=NOPAT)
    """
    try:
        # 1. On transpose immédiatement (.T) pour avoir les Dates en Index et les Métriques en Colonnes
        # C'est ta méthode, beaucoup plus propre pour les calculs vectoriels
        fin_T = stock.financials.T
        
        # Vérification minimale : est-ce qu'on a des données ?
        if fin_T.empty:
            return 0, pd.Series()

        # ---------------------------------------------------------
        # A. CALCUL DU TAUX D'IMPOSITION (Ta méthode précise)
        # ---------------------------------------------------------
        # On vérifie si les colonnes nécessaires existent
        if 'Pretax Income' in fin_T.columns and 'Tax Provision' in fin_T.columns:
            # Calcul du taux réel
            fin_T['Effective Tax Rate'] = fin_T['Tax Provision'] / fin_T['Pretax Income']
            
            # NETTOYAGE DES VALEURS ABERRANTES :
            # Parfois le taux est infini (div par 0) ou négatif (crédit d'impôt exceptionnel)
            # Pour un ROIC cohérent sur le long terme, on "borne" le taux entre 0% et 50%
            # Si c'est hors bornes, on applique le taux par défaut.
            fin_T['Effective Tax Rate'] = fin_T['Effective Tax Rate'].apply(
                lambda x: default_tax_rate if (pd.isna(x) or x < 0 or x > 0.50) else x
            )
        else:
            # Si colonnes manquantes, on utilise le taux par défaut
            fin_T['Effective Tax Rate'] = default_tax_rate

        # ---------------------------------------------------------
        # B. RÉCUPERATION DE L'EBIT
        # ---------------------------------------------------------
        if 'EBIT' in fin_T.columns:
            fin_T['EBIT_Clean'] = fin_T['EBIT']
        elif 'Pretax Income' in fin_T.columns and 'Interest Expense' in fin_T.columns:
            # Reconstruction : EBIT = Pretax + Interest (on prend la valeur absolue des intérêts)
            # fillna(0) est important si Interest Expense est vide par endroits
            fin_T['EBIT_Clean'] = fin_T['Pretax Income'] + fin_T['Interest Expense'].fillna(0).abs()
        else:
            # Impossible de calculer sans EBIT
            return 0, pd.Series()

        # ---------------------------------------------------------
        # C. CALCUL FINAL DU NOPAT
        # Formule : EBIT * (1 - Tax Rate)
        # ---------------------------------------------------------
        fin_T['NOPAT'] = fin_T['EBIT_Clean'] * (1 - fin_T['Effective Tax Rate'])
        
        # Le DataFrame est trié du plus récent au plus ancien par défaut chez Yahoo
        # current_nopat est la première ligne (iloc[0])
        current_nopat = fin_T['NOPAT'].iloc[0]
        
        # nopat_history est la série complète. 
        # Important : Les index sont des Dates, ce qui est compatible avec Onglet_Finance.py
        nopat_history = fin_T['NOPAT']

        return current_nopat, nopat_history

    except Exception as e:
        print(f"Erreur dans le calcul du NOPAT : {e}")
        # En cas de crash, on retourne 0 pour ne pas casser l'app
        return 0, pd.Series()