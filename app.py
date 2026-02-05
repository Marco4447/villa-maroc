import streamlit as st

# 1. CONFIGURATION INITIALE
st.set_page_config(page_title="Audit Villa Maroc", layout="wide")

# 2. DESIGN & WHITE LABEL (Suppression totale Streamlit)
st.markdown("""
    <style>
    header {visibility: hidden !important; height: 0 !important;}
    footer {visibility: hidden !important; height: 0 !important;}
    #MainMenu {visibility: hidden !important;}
    .stAppDeployButton {display: none !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}
    .block-container {padding-top: 0rem !important; padding-bottom: 0rem !important;}
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'serif'; }
    div[data-testid="stMetric"] { 
        background-color: #161B22; border: 1px solid #D4AF37; 
        padding: 15px; border-radius: 10px; text-align: center;
    }
    div[data-testid="stMetricValue"] > div { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏰 Audit de rentabilité de votre Villa")
st.markdown("---")

# 3. BARRE LATÉRALE
with st.sidebar:
    st.header("⚙️ Configuration")
    with st.expander("🏦 Financement", expanded=True):
        type_pret = st.radio("Type de crédit", ["In Fine", "Amortissable"])
        m_pret = st.number_input("Montant emprunté (€)", value=470000)
        tx_annuel = st.number_input("Taux annuel (%)", value=3.70)
        ans = st.slider("Durée (ans)", 1, 25, 15)
        apport = st.number_input("Apport personnel (€)", value=200000)

    with st.expander("📅 Revenus Locatifs", expanded=True):
        adr = st.number_input("Prix Nuitée (€)", value=430)
        to_actuel = st.slider("Occupation Actuelle (%)", 0, 100, 41)
        
    with st.expander("💸 Frais Villa", expanded=True):
        com_concierge = st.slider("Conciergerie (%)", 0, 40, 20)
        energie_mois = st.number_input("Energie / mois (€)", value=350)
        menage_mois = st.number_input("Ménage / mois (€)", value=1000)
        taxe_fonciere_an = st.number_input("Taxe Foncière / an (€)", value=3000)
        jardin_mois = st.number_input("Jardin / mois (€)", value=200)
        fixes_mois = st.number_input("Assurances / mois (€)", value=100)

# 4. MOTEUR DE CALCUL (Simulations)
def engine(occ):
    # Mensualité
    if type_pret == "In Fine":
        mens = (m_pret * (tx_annuel / 100)) / 12
    else:
        tm = tx_annuel / 100 / 12
        nm = ans * 12
        mens = m_pret * (tm / (1 - (1 + tm)**-nm)) if tm >
