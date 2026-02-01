# --------------------------------------
# --- Création de l'onglet Glossaire ---
# --------------------------------------

# -----------------------------------------
# --- 00.1 - Importation des librairies ---
# -----------------------------------------
import streamlit as st

# -------------------------------------------
# --- 00.2 - Importation de nos fonctions ---
# -------------------------------------------
from utils.Styles import style_CSS
from utils.Glossaire.Glossaire_Data import GLOSSARY

style_CSS()

# ---------------------------------------------------------------------------------------------------------------------------------
# --- Création de notre fonction qui permet d'afficher notre glossaire en fonction d'un dictionnaire de données donné en entrée ---
# ---------------------------------------------------------------------------------------------------------------------------------

def afficher_definition(data: dict):
    st.write(data["definition"])
    st.caption(data["interpretation"])
    st.caption(data["tip"])

def afficher_seuils(thresholds: dict):

    cols = st.columns(len(thresholds))

    for col, (label, value) in zip(cols, thresholds.items()):
        with col:
            if "🟢" in label:
                st.success(f"**{label}**\n\n{value}")
            elif "🟡" in label:
                st.warning(f"**{label}**\n\n{value}")
            else:
                st.error(f"**{label}**\n\n{value}")


def afficher_fiche_glossaire(data: dict):
    with st.container():
        st.markdown(f"#### 📌 {data['title']}")
        afficher_definition(data)

        if data.get("thresholds"):
            afficher_seuils(data["thresholds"])

    st.divider()


def afficher_onglet_glossaire():
    for data in GLOSSARY.values():
        afficher_fiche_glossaire(data)


 


