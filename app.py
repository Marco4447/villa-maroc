import streamlit as st

# 1. CONFIGURATION
st.set_page_config(page_title="Simulation de rentabilité", layout="wide")

# 2. DESIGN PRO
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'serif'; }
    div[data-testid="stMetric"] { 
        background-color: #161B22; 
        border: 1px solid #D4AF37; 
        padding: 15px; 
        border-radius: 10px; 
        text-align: center;
    }
    div[data-testid="stMetricValue"] > div { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏰 Simulation de rentabilité de votre villa")
st.markdown("---")

# 3. BARRE LATÉRALE
with st.sidebar:
    st.header("⚙️ Configuration")
    
    with st.expander("🏦 Financement (In Fine)", expanded=False):
        m_pret = st.number_input("Montant emprunté (€)", value=470000, step=5000)
        apport = st.number_input("Apport injecté (€)", value=200000, step=5000)
        tx = st.number_input("Taux annuel (%)", value=3.70, step=0.05)
        ans = st.slider("Durée du crédit (ans)", 1, 25, 15)

    with st.expander("📅 Revenus Locatifs", expanded=True):
        # Double saisie : Manuelle + Curseur
        adr = st.number_input("Prix Nuitée (€) - Saisie manuelle", value=500, step=10)
        to = st.slider("Occupation (%)", 0, 100, 45, 1)
        
    with st.expander("💸 Détail des Frais Villa", expanded=True):
        st.subheader("Charges Variables")
        com_concierge = st.slider("Conciergerie (%)", 0, 40, 25)
        frais_energie_nuit = st.number_input("Eau & Électricité / nuit (€)", value=15, step=5)
        menage_nuit = st.number_input("Ménage & Blanchisserie / nuit (€)", value=35, step=5)
        
        st.subheader("Charges Fixes")
        taxe_hab = st.number_input("Taxe Habitation & Foncière (€)", value=3000, step=100)
        entretien_jardin = st.number_input("Entretien Jardin & Piscine (€)", value=2400, step=100)
        autres_fixes = st.number_input("Assurances & Internet (€)", value=1200, step=100)

# 4. CALCULS
mensu_int = (m_pret * (tx / 100)) / 12
nuits = 365 * (to / 100)
ca_annuel = nuits * adr

frais_concierge = ca_annuel * (com_concierge / 100)
frais_variables_tot = nuits * (frais_energie_nuit + menage_nuit)
total_fixes = taxe_hab + entretien_jardin + avec_fixes = 1200 # Valeur par défaut
total_fixes = taxe_hab + entretien_jardin + autres_fixes
total_charges = frais_concierge + frais_variables_tot + total_fixes

profit_mensuel = (ca_annuel - total_charges - (mensu_int * 12)) / 12

# 5. KPI (Affichage sans virgules)
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Chiffre d'Affaires
