# ----------------------------------------
# --- Création de la page Glossaire.py ---
# ----------------------------------------
"""

Sommaire du fichier : 

    - 00.1 - Importation des librairies
    - 00.2 - Importation de nos fonctions
    - 1 - AFFICHAGE PRINCIPAL

"""
# -----------------------------------------
# --- 00.1 - Importation des librairies ---
# -----------------------------------------
import streamlit as st

# -------------------------------------------
# --- 00.2 - Importation de nos fonctions ---
# -------------------------------------------
from utils.Styles import style_CSS
from utils.Glossaire_Data import GLOSSARY

# ------------------------------------
# --- 00.3 - Réglage de notre page ---
# ------------------------------------
st.set_page_config(page_title="Glossaire & Définitions", page_icon="📚", layout="wide")
style_CSS() # Application de notre style CSS
st.title("📚 Glossaire") 
st.write("---")

# -------------------------------
# --- 1 - AFFICHAGE PRINCIPAL ---
# -------------------------------
# On parcourt le dictionnaire GLOSSARY pour générer les fiches
for key, data in GLOSSARY.items():
    # On crée un conteneur pour chaque indicateur
    with st.container():
        # En-tête avec l'icône et le titre
        st.subheader(f"📌 {data['title']}")
        col_def, col_thresholds = st.columns([1, 1.5])
        # COLONNE GAUCHE : DÉFINITION
        with col_def:
            st.markdown(f"**📖 Définition :**")
            st.write(data['definition'])
            st.markdown(f"*{data['interpretation']}*")
            # Le petit conseil pro dans une boîte verte
            st.success(f"💡 **Conseil Pro :** {data['tip']}")
        # COLONNE DROITE : LES SEUILS (Visuel)
        with col_thresholds:
            st.markdown("**🎯 Les Zones Cibles :**")
            # On récupère les seuils (Vert, Jaune, Rouge)
            seuils_items = list(data['thresholds'].items())
            # On affiche 3 petites colonnes pour les couleurs
            c1, c2, c3 = st.columns(3)
            if len(seuils_items) >= 3:
                # Vert
                with c1:
                    st.info(f"**{seuils_items[0][0]}**\n\n{seuils_items[0][1]}")
                # Jaune
                with c2:
                    st.warning(f"**{seuils_items[1][0]}**\n\n{seuils_items[1][1]}")
                # Rouge
                with c3:
                    st.error(f"**{seuils_items[2][0]}**\n\n{seuils_items[2][1]}")
    st.write("---") # Séparateur entre chaque fiche