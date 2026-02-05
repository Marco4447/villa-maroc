import streamlit as st

# 1. CONFIGURATION
st.set_page_config(page_title="Simulation Villa Maroc", layout="wide")

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
        com_concierge = st.slider("Conciergerie (%)", 0, 40, 25)
        energie_mois = st.number_input("Eau & Elec / mois (€)", value=450, step=50)
        menage_mois = st.number_input("Ménage / mois (€)", value=1000, step=100)
        taxe_fonciere_an = st.number_input("Taxe Foncière / an (€)", value=3000, step=100)
        jardin_mois = st.number_input("Jardin & Piscine / mois (€)", value=200, step=50)
        fixes_mois = st.number_input("Assurances & Internet / mois (€)", value=100, step=10)

# 4. CALCULS FINANCIERS
if type_pret == "In Fine":
    mensualite = m_pret * (tx_annuel / 100 / 12)
else:
    t = tx_annuel / 100 / 12
    n = ans * 12
    mensualite = m_pret * (t / (1 - (1 + t)**-n)) if t > 0 else m_pret / (ans * 12)

nuits_an = 365 * (to / 100)
ca_an = nuits_an * adr
frais_gestion_an = ca_an * (com_concierge / 100)
charges_fixes_an = taxe_fonciere_an + (energie_mois + menage_mois + jardin_mois + fixes_mois) * 12
total_charges_an = frais_gestion_an + charges_fixes_an

# 5. FISCALITÉ MAROC
base_imposable = ca_an * 0.60
if base_imposable <= 3000: impot_an = 0
elif base_imposable <= 5000: impot_an = (base_imposable * 0.10) - 300
elif base_imposable <= 6000: impot_an = (base_imposable * 0.20) - 800
elif base_imposable <= 8000: impot_an = (base_imposable * 0.30) - 1400
elif base_imposable <= 18000: impot_an = (base_imposable * 0.34) - 1720
else: impot_an = (base_imposable * 0.38) - 2440

profit_mensuel_net = (ca_an - total_charges_an - (mensualite * 12) - impot_an) / 12

# 6. SEUIL DE RENTABILITÉ (BREAK-EVEN)
# Calcul simplifié du CA nécessaire pour couvrir charges fixes + crédit
marge_brute_taux = 1 - (com_concierge / 100)
seuil_ca_an = (charges_fixes_an + (mensualite * 12)) / marge_brute_taux

# 7. AFFICHAGE ÉCRAN PRINCIPAL
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Chiffre d'Affaires Estimé", f"{int(ca_an)} €")
with c2:
    st.metric("Profit Mensuel (Net de Net)", f"{int(profit_mensuel_net)} €")
with c3:
    renta = (profit_mensuel_net * 12 / apport * 100) if apport > 0 else 0
    st.metric("Rendement / Apport", f"{renta:.1f} %")

st.markdown("---")

col_res1, col_res2 = st.columns(2)
with col_res1:
    st.subheader("📊 Performance Détaillée")
    st.write(f"• Total Charges Annuelles : **{int(total_charges_an)} €**")
    st.write(f"• Impôts Maroc estimés : **{int(impot_an)} €**")
    st.write(f"• Taux d'occupation actuel : **{to} %**")
    
with col_res2:
    st.subheader("🏁 Seuil de Rent
