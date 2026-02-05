import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Simulation de rentabilité", layout="wide")

# 2. STYLE VISUEL (Design Sombre & Or)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    h1, h2, h3 { color: #D4AF37 !important; }
    div[data-testid="stMetric"] { 
        background-color: #161B22; 
        border: 1px solid #D4AF37; 
        padding: 15px; 
        border-radius: 10px; 
    }
    div[data-testid="stMetricValue"] > div { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. TITRE
st.title("🏰 Simulation de rentabilité de votre villa")
st.markdown("---")

# 4. BARRE LATÉRALE (RÉGLAGES)
with st.sidebar:
    st.header("⚙️ Paramètres du Projet")
    
    # Paramètres d'acquisition
    prix_villa = st.number_input("Prix de la Villa (€)", value=670000, step=10000)
    
    st.markdown("---")
    st.subheader("🏦 Financement In Fine")
    # L'utilisateur choisit ici le montant du crédit et l'apport séparément
    montant_credit = st.number_input("Montant du crédit (€)", value=470000, step=5000)
    apport_perso = st.number_input("Apport Personnel (€)", value=200000, step=5000)
    taux_annuel = st.number_input("Taux d'intérêt annuel (%)", value=3.70, step=0.05)
    duree_pret = st.slider("Nombre d'années du crédit", 1
