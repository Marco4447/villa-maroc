import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Audit Villa Maroc", layout="wide")

# 2. DESIGN PRO (Sombre & Or)
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

st.title("🏰 Audit de rentabilité complet de votre villa")
st.markdown("---")

# 3. BARRE LATÉRALE (PARAMÈTRES)
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
    mensualite = (m_pret * (tx_annuel / 100)) / 12
else:
    t = tx_annuel / 100 / 12
    n = ans * 12
    if t > 0:
        mensualite = m_pret * (t / (1 - (1 + t)**-n))
    else:
        mensualite = m_pret / n

# Exploitation
nuits_an = 365 * (to / 100)
ca_an = nuits_an * adr
frais_gestion_an = ca_an * (com_concierge / 100)
charges_fixes_an = taxe_fonciere_an + (energie_mois + menage_mois + jardin_mois + fixes_mois) * 12
total_charges_an = frais_gestion_an + charges_fixes_an

# 5. FISCALITÉ MAROC (Abattement 40%)
base_taxable = ca_an * 0.60
if base_taxable <= 3000:
    impot_an = 0
elif base_taxable <= 5000:
    impot_an = (base_taxable * 0.10) - 300
elif base_taxable <= 6000:
    impot_an = (base_taxable * 0.20) - 800
elif base_taxable <= 8000:
    impot_an = (base_taxable * 0.30) - 1400
elif base_taxable <= 18000:
    impot_an = (base_taxable * 0.34) - 1720
else:
    impot_an = (base_taxable * 0.38) - 2440

profit_mensuel = (ca_an - total_charges_an - (mensualite * 12) - impot_an) / 12

# 6. SEUIL DE RENTABILITÉ (POINT MORT)
marge_apres_concierge = 1 - (com_concierge / 100)
seuil_ca_annuel = (charges_fixes_an + (mensualite * 12)) / marge_apres_concierge

# 7. AFFICHAGE ÉCRAN PRINCIPAL
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("CA Annuel Estimé", str(int(ca_an)) + " €")
with c2:
    st.metric("Profit Net Mensuel", str(int(profit_mensuel)) + " €")
with c3:
    renta_apport = (profit_mensuel * 12 / apport * 100) if apport
