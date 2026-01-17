# ------------------------------------------------
# --- Création de fonctions autres thématiques ---
# ------------------------------------------------

"""

Sommaire des fonctions ajoutées : 

    - get_currency_symbol : Transforme le code ISO (USD, EUR) en symbole ($, €)
    - translate_sector : Traduit les secteurs Yahoo Finance (EN) vers le Français (FR)

"""

# --------------
# --- DEVISE ---
# --------------
def get_currency_symbol(currency_code):
    if not currency_code:
        return "AUD"
        
    mapping = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥',
        'CNY': '¥',
        'CHF': 'CHF',
        'CAD': 'C$'
    }
    # Retourne le symbole s'il existe, sinon retourne le code AUD
    return mapping.get(currency_code, currency_code)

# -----------------------------------
# --- TRADUCTION SECTEUR ACTIVITÉ ---
# -----------------------------------
def translate_sector(sector_name):
    if not sector_name or sector_name == 'Indéfini':
        return "Non défini"
        
    mapping = {
        "Technology": "Technologie",
        "Financial Services": "Finance",
        "Healthcare": "Santé",
        "Consumer Cyclical": "Consommation Cyclique", # Luxe, Auto...
        "Consumer Defensive": "Consommation de base",    # Alimentaire, Hygiène...
        "Industrials": "Industrie",
        "Communication Services": "Communication",
        "Energy": "Énergie",
        "Real Estate": "Immobilier",
        "Basic Materials": "Matériaux Base",
        "Utilities": "Services Publics" # Eau, Élec...
    }    
    # On renvoie la traduction, ou le nom anglais si on ne trouve pas
    return mapping.get(sector_name, sector_name)