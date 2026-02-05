import streamlit as st

st.set_page_config(page_title="Audit Rentabilité Villa", layout="wide")

# Injection CSS pour masquer le footer et les menus Streamlit
st.markdown("""
    <style>
    /* Masquer le footer "Built with Streamlit" */
    footer {visibility: hidden !important; height: 0 !important;}
    /* Masquer le menu hamburger en haut à droite */
    #MainMenu {visibility: hidden !important;}
    /* Masquer la barre d'outils en haut (Deploy, etc.) */
    header {visibility: hidden !important;}
    /* Supprimer les paddings inutiles pour l'intégration iFrame */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
