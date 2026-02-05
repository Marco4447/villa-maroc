import streamlit as st

# 1. CONFIGURATION (Doit être la toute première commande)
st.set_page_config(page_title="Audit Villa Maroc", layout="wide")

# 2. DESIGN & SUPPRESSION TOTALE STREAMLIT (White Label)
st.markdown("""
    <style>
    /* Suppression radicale des menus et footers Streamlit */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    .stAppDeployButton {display: none !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}
    
    /* Optimisation de l'espace pour l'intégration iFrame */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }

    /* Thème Sombre & Or */
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

# 3. BARRE LATÉRALE (CONFIGURATION)
with st.sidebar:
    st.header("⚙️ Paramètres")
    with st.expander("🏦 Financement", expanded=True):
        type_pret = st.radio("Type de crédit", ["In Fine", "Amortissable"])
        m_pret = st.number_input("Montant emprunté (€)", value=470000)
        tx_annuel = st.number_input("Taux annuel (%)", value=3.70)
        ans = st.slider("Durée (ans)", 1, 25, 15)
        apport = st.number_input("Apport personnel (€)", value=200000)

    with st.expander("📅 Revenus Locatifs", expanded=True):
        adr = st.number_input("Prix Nuitée (€)", value=430)
        to = st.slider("Occupation Actuelle (%)", 0, 100, 41)
        
    with st.expander("💸 Frais Villa", expanded=True):
        com_concierge = st.slider("Conciergerie (%)", 0, 40, 20)
        energie_mois = st.number_input("Eau & Elec / mois (€)", value=350)
        menage_mois = st.number_input("Ménage / mois (€)", value=1000)
        taxe_fonciere_an = st.number_input("Taxe Foncière / an (€)", value=3000)
        jardin_mois = st.number_input("Jardin & Piscine / mois (€)", value=200)
        fixes_mois = st.number_input("Assurances & Internet / mois (€)", value=100)

# 4. MOTEUR DE CALCUL (Logique itérative pour le Seuil)
def simuler(occ_test, adr_in, m_pret_in, tx_in, ans_in, type_p):
    # Mensualité
    if type_p == "In Fine":
        mens = (m_pret_in * (tx_in / 100)) / 12
    else:
        tm = tx_in / 100 / 12
        nm = ans_in * 12
        mens = m_pret_in * (tm / (1 - (1 + tm)**-nm)) if tm > 0 else m_pret_in / nm
    
    # Exploitation & Impôts Maroc (Abattement 40%)
    ca = 365 * (occ_test / 100) * adr_in
    base_taxe = ca * 0.60
    if base_taxe <= 3000: imp = 0
    elif base_taxe <= 18000: imp = (base_taxe * 0.34) - 1720
    else: imp = (base_taxe * 0.38) - 2440
