# ------------------------------------------
# --- Création de nos indicateurs et KPI ---
# ------------------------------------------
import datetime


"""

Sommaire des indicateurs : 

    - calculate_rsi : RSI (14 jours)
    - calculate_ytd_performance : calcule la variation en % par rapport à la FERMETURE de l'année N-1

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