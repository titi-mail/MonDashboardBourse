import requests

# ---------------------------------------------
# --- FONCTION DE RECHERCHE (POUR LA BARRE) ---
# ---------------------------------------------
def search_assets(query):
    """
    Interroge Yahoo Finance pour trouver des actifs.
    """
    if not query:
        return []

    url = "https://query1.finance.yahoo.com/v1/finance/search"
    
    # On se fait passer pour un navigateur standard
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    params = {
        "q": query,
        "quotesCount": 10,
        "newsCount": 0,
        "enableFuzzyQuery": "false",
        "quotesQueryId": "tss_match_phrase_query"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=3)
        data = response.json()
        
        results = []
        if 'quotes' in data:
            for item in data['quotes']:
                if 'symbol' in item:
                    symbol = item['symbol']
                    name = item.get('shortname') or item.get('longname') or symbol
                    exch = item.get('exchDisp', item.get('exchange', 'N/A'))
                    
                    label = f"{name} ({exch})   [{symbol}]"
                    results.append((symbol, label))
        return results
        
    except Exception as e:
        print(f"Erreur API Recherche : {e}")
        return []
    
# -------------------------------------
# --- FONCTION DE LIAISON (LE PONT) ---
# -------------------------------------
def search_wrapper(searchterm):
    """
    Cette fonction fait le pont entre la Searchbox et notre moteur Yahoo.
    Elle inverse les résultats pour correspondre au format attendu par la Searchbox.
    """
    # 1. On récupère les résultats bruts : [('TSLA', 'TSLA - Tesla...'), ...]
    raw_results = search_assets(searchterm)
    
    # 2. On les transforme pour la Searchbox : attendu -> (Label_Visible, Valeur_Renvoyée)
    # On inverse donc l'ordre ici :
    formatted_results = [(item[1], item[0]) for item in raw_results]
    
    return formatted_results