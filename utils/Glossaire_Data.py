# ------------------------------------------------------------------------------------
# --- Ajout des informations à notre glossaire + création de la fonction glossaire ---
# ------------------------------------------------------------------------------------

GLOSSARY = {
    "PER": {
        "title": "PER (Price Earning Ratio)",
        "definition": "Le multiple de capitalisation des bénéfices. Il indique combien d'années de bénéfices actuels il faut pour rembourser le prix de l'action.",
        "interpretation": "Mesure la cherté d'une action par rapport à ses profits.",
        "thresholds": {
            "🟢 Bon marché": "inférieur à 15",
            "🟡 Juste prix": "entre 15 et 25",
            "🔴 Cher": "supérieur à 25 (sauf hyper-croissance)"
        },
        "tip": "Un PER élevé n'est pas forcément mauvais si l'entreprise double ses profits chaque année (voir PEG)."
    },
}

def get_glossary_info(key):
    """Récupère les infos proprement ou retourne un dictionnaire vide"""
    return GLOSSARY.get(key, {})