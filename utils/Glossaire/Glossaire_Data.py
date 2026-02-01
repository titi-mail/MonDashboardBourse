# ------------------------------------------------------------------------------------
# --- Ajout des informations à notre glossaire + création de la fonction glossaire ---
# ------------------------------------------------------------------------------------

GLOSSARY = {
    "Marge Nette": {
        "title": "Marge Nette",
        "definition": "Marge Nette = Résultat net / Chiffre d'affaires",
        "interpretation": (
            "Indique la part du chiffre d'affaires qui reste en bénéfice net après "
            "toutes les charges (coûts, impôts, intérêts). "
            "Plus la marge nette est élevée et stable, plus le modèle économique "
            "est considéré comme rentable et robuste."
        ),
        "tip": (
            "Cet indicateur est à comparer principalement avec les entreprises du même secteur et "
            "à analyser sur plusieurs années plutôt que sur une seule période."
        ),
        "thresholds": {
            "🔴 Faible": "inférieure à 5 % (forte concurrence ou coûts élevés)",
            "🟡 Correcte": "entre 5 % et 10 %",
            "🟢 Élevée": "supérieure à 10 % (avantage concurrentiel possible)"
        }
    },

    "ROE": {
        "title": "ROE (Return on Equity)",
        "definition": "ROE = Résultat net / Capitaux propres",
        "interpretation": (
            "Mesure la capacité de l'entreprise à générer du bénéfice à partir "
            "des capitaux investis par les actionnaires. "
            "Un ROE élevé traduit une utilisation efficace des fonds propres."
        ),
        "tip": (
            "Un ROE durablement élevé est positif, mais il doit être analysé "
            "avec le niveau d'endettement : une dette excessive peut gonfler "
            "artificiellement le ROE (Capitaux propres = Actifs - Dettes)."
        ),
        "thresholds": {
            "🔴 Faible": "inférieur à 8 % (création de valeur limitée)",
            "🟡 Correct": "entre 8 % et 15 %",
            "🟢 Élevé": "supérieur à 15 % (bonne création de valeur)"
        }
    },

    "ROIC": {
        "title": "ROIC (Return on Invested Capital)",
        "definition": "ROIC = EBIT après impôts / Capital investi total (EBIT : bénéfice avant intérêts et impôts)",
        "interpretation": (
            "Évalue la capacité de l'entreprise à générer un rendement sur l'ensemble "
            "des capitaux investis (fonds propres + dettes financières). "
            "C'est un indicateur plus complet que le ROE car il neutralise l'effet de levier."
        ),
        "tip": (
            "Comparer le ROIC au coût moyen du capital (WACC) : "
            "si ROIC > WACC, l'entreprise crée de la valeur. "
            "Un ROIC stable et supérieur au WACC est un signe de business solide."
        ),
        "thresholds": {
            "🔴 Faible": "inférieur à 5 % (création de valeur insuffisante)",
            "🟡 Correct": "entre 5 % et 10 %",
            "🟢 Élevé": "supérieur à 10 % (bonne rentabilité du capital investi)"
        }
    }
}


def get_glossary_info(key):
    """Récupère les infos proprement ou retourne un dictionnaire vide"""
    return GLOSSARY.get(key, {})