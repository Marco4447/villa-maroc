import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Simulation de rentabilité", layout="wide")

# 2. DESIGN PRO (Sombre & Or)
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

# 3. BARRE LATÉRALE (PARAMÈTRES COMPLETS)
with st.sidebar:
    st.header("⚙️ Configuration")
    
    with st.expander("🏦 Financement", expanded=True):
        type_pret = st.radio("Type de crédit", ["In Fine", "Amortissable"])
        m_pret = st.number_input("Montant emprunté (€)", value=470000, step=5000)
        apport = st.number_input("Apport personnel (€)", value=200000, step=5000)
        tx_annuel = st.number_input("Taux annuel (%)", value=3.70, step=0.05)
        ans = st.slider("Durée du crédit (ans)", 1, 25, 15)

    with st.expander("📅 Revenus Locatifs", expanded=True):
        adr = st.number_input("Prix Nuitée (€)", value=500, step=10)
        to = st.slider("Occupation (%)", 0, 100, 45, 1)
        
    with st.expander("💸 Frais Villa (Par mois)", expanded=True):
        st.subheader("Charges Variables")
        com_concierge = st.slider("Conciergerie (%)", 0, 40, 25)
        energie_mois = st.number_input("Eau & Elec / mois (€)", value=450, step=50)
        menage_mois = st.number_input("Ménage & Blanchisserie / mois (€)", value=1000, step=100)
        
        st.subheader("Charges Fixes")
        taxe_an = st.number_input("Taxe Foncière / an (€)", value=3000, step=100)
        jardin_mois = st.number_input("Jardin & Piscine / mois (€)", value=200, step=50)
        fixes_mois = st.number_input("Assurances & Internet / mois (€)", value=100, step=10)

# 4. LOGIQUE DE CALCUL DU CRÉDIT
if type_pret == "In Fine":
    mensualite_totale = m_pret * (tx_annuel / 100 / 12)
    cout_total_credit = mensualite_totale * 12 * ans
else:
    t = tx_annuel / 100 / 12
    n = ans * 12
    mensualite_totale = m_pret * (t / (1 - (1 + t)**-n))
    cout_total_credit = (mensualite_totale * n) - m_pret

# 5. CALCULS EXPLOITATION
nuits_an = 365 * (to / 100)
ca_an = nuits_an * adr

# Ventilation des charges
frais_gestion_an = ca_an * (com_concierge / 100)
frais_
