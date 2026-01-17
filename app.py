import streamlit as st

# Configuration de la page (Doit être la 1ère commande Streamlit)
st.set_page_config(
    page_title="Mon Dashboard Bourse",
    page_icon="🚀",
    layout="wide"
)

st.title("👋 Bienvenue sur ton Dashboard DCA")

st.markdown("""
### Objectifs de cette application :
1. **Screener :** Identifier les opportunités d'achat.
2. **Portfolio :** Suivre la performance réelle.
3. **Macro :** Comprendre l'environnement économique.

👈 **Utilise le menu à gauche pour naviguer.**
""")