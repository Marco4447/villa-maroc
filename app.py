import streamlit as st
import numpy as np

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
        com_concierge = st.slider("Conciergerie (%)", 0, 40, 25)
        energie_mois = st.number_input("Eau & Elec / mois (€)", value=450, step=50)
        menage_mois = st.number_input("Ménage & Blanchisserie / mois (€)", value=1000, step=100)
        taxe_an = st.number_input("Taxe Foncière / an (€)", value=3000, step=100)
        jardin_mois = st.number_input("Jardin & Piscine / mois (€)", value=200, step=50)
        fixes_mois = st.number_input("Assurances & Internet / mois (€)", value=100, step=10)

# 4. LOGIQUE DE CALCUL DU CRÉDIT
t = tx_annuel / 100 / 12
n = ans * 12

if type_pret == "In Fine":
    # On ne paie que les intérêts
    mensualite_totale = m_pret * (tx_annuel / 100 / 12)
    part_interets = mensualite_totale
    part_capital = 0
else:
    # Formule annuité amortissable : M = P * [i / (1 - (1+i)^-n)]
    mensualite_totale = m_pret * (t / (1 - (1 + t)**-n))
    # Moyenne simplifiée pour la simulation (la première mensualité)
    part_interets = m_pret * t
    part_capital = mensualite_totale - part_interets

# 5. CALCULS EXPLOITATION
nuits_an = 365 * (to / 100)
ca_an = nuits_an * adr
charges_an = (ca_an * com_concierge / 100) + (energie_mois * 12) + (menage_mois * 12) + taxe_an + (jardin_mois * 12) + (fixes_mois * 12)

# Cash-flow après TOUTES les charges et TOUTE la mensualité
profit_annuel = ca_an - charges_an - (mensualite_totale * 12)
profit_mensuel = profit_annuel / 12

# 6. KPI
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("CA Annuel", f"{int(ca_an)} €")
with c2:
    st.metric("Cash-flow Net Mensuel", f"{int(profit_mensuel)} €")
with c3:
    renta = (profit_annuel / apport * 100) if apport > 0 else 0
    st.metric("Rendement
