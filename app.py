import streamlit as st

# 1. CONFIGURATION
st.set_page_config(page_title="Simulation de rentabilité", layout="wide")

# 2. DESIGN PRO
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'serif'; }
    div[data-testid="stMetric"] { 
        background-color: #161B22; border: 1px solid #D4AF37; 
        padding: 15px; border-radius: 10px; text-align: center;
    }
    div[data-testid="stMetricValue"] > div { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏰 Simulation de rentabilité de votre villa")
st.markdown("---")

# 3. BARRE LATÉRALE
with st.sidebar:
    st.header("⚙️ Configuration")
    with st.expander("🏦 Financement", expanded=False):
        type_pret = st.radio("Type de crédit", ["In Fine", "Amortissable"])
        m_pret = st.number_input("Montant emprunté (€)", value=470000, step=5000)
        apport = st.number_input("Apport personnel (€)", value=200000, step=5000)
        tx_annuel = st.number_input("Taux annuel (%)", value=3.70, step=0.05)
        ans = st.slider("Durée du crédit (ans)", 1, 25, 15)

    with st.expander("📅 Revenus Locatifs", expanded=True):
        adr = st.number_input("Prix Nuitée (€)", value=500, step=10)
        to = st.slider("Occupation (%)", 0, 100, 45, 1)
        
    with st.expander("💸 Frais Villa (Mensuels)", expanded=True):
        st.subheader("Charges Variables")
        com_concierge = st.slider("Conciergerie (%)", 0, 40, 25)
        energie_mois = st.number_input("Eau & Elec / mois (€)", value=450, step=50)
        menage_mois = st.number_input("Ménage / mois (€)", value=1000, step=100)
        st.subheader("Charges Fixes")
        taxe_fonciere_an = st.number_input("Taxe Foncière / an (€)", value=3000, step=100)
        jardin_mois = st.number_input("Jardin & Piscine / mois (€)", value=200, step=50)
        fixes_mois = st.number_input("Assurances & Internet / mois (€)", value=100, step=10)

# 4. CALCULS FINANCIERS
# Crédit
if type_pret == "In Fine":
    mensualite = m_pret * (tx_annuel / 100 / 12)
else:
    t = tx_annuel / 100 / 12
    n = ans * 12
    mensualite = m_pret * (t / (1 - (1 + t)**-n)) if t > 0 else m_pret / n

# Exploitation
nuits_an = 365 * (to / 100)
ca_an = nuits_an * adr
charges_an = (ca_an * com_concierge / 100) + (energie_mois * 12) + (menage_mois * 12) + taxe_fonciere_an + (jardin_mois * 12) + (fixes_mois * 12)

# 5. CALCUL "IMPÔTS MAROC"
# Abattement de 40% sur le CA Brut
base_imposable = ca_an * 0.60

# Barème IR
