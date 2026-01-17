# -------------------------------
# --- Création des graphiques ---
# -------------------------------

import plotly.graph_objects as go

"""

Sommaire des graphiques ajoutés : 

    - create_gauge : Crée une jauge semi-circulaire avec un design sombre, un arc coloré et un effet de halo

"""

# ------------------------
# --- Jauge de données ---
# ------------------------
def create_gauge(value, title, min_val, max_val, thresholds, metric_mode="higher_is_better", suffix="" ):
    """
    thresholds (seuils) : important pour inverser ou non les couleurs en fonction de la métrique utilisée
        "higher_is_better" → plus c’est haut, mieux c’est (ROE, croissance, score…)
        "lower_is_better" → plus c’est bas, mieux c’est (PER, drawdown, volatilité…)
        "range_optimal" → une zone optimale (RSI, marge cible…)
    """
    # Initialisation des couleurs 
    COLORS = {
        "good": "#37C36C",   # Vert
        "mid":  "#FACF3D",   # Jaune
        "bad":  "#EA424B"    # Rouge
    }

    # Détermination de la couleur en fonction du paramètre entrée dans la fonction
    if metric_mode == "higher_is_better":
        if value < thresholds[0]:
            color = COLORS["bad"]
        elif value < thresholds[1]:
            color = COLORS["mid"]
        else:
            color = COLORS["good"]

    elif metric_mode == "lower_is_better":
        if value < thresholds[0]:
            color = COLORS["good"]
        elif value < thresholds[1]:
            color = COLORS["mid"]
        else:
            color = COLORS["bad"]

    elif metric_mode == "range_optimal":
        if thresholds[0] <= value <= thresholds[1]:
            color = COLORS["good"]
        elif value < thresholds[0] or value > thresholds[1]:
            color = COLORS["bad"]
        else:
            color = COLORS["mid"]

    else:
        raise ValueError("metric_mode inconnu")

    # Création de la jauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        gauge={
            "shape": "angular",
            "bar": {"color": color, "thickness": 1.0},
            "bgcolor": "#1E222D",
            "axis": {"range": [min_val, max_val], "visible": False} # Création de la plage des axes de la jauge + désactivation de l'affichage
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=25, r=25, t=50, b=25),
        height=160,
        title={
        'text': title,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
        }
    )

    return fig, color
