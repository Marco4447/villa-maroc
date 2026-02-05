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

st.title("🏰 Simulation de rentabilité & Fiscalité Maroc")
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

# 5. CALCUL DE L'IMPÔT SUR LE REVENU FONCIER (MAROC)
# Base imposable = CA Brut - 40% d'abattement forfaitaire
base_imposable = ca_an * 0.60

# Barème simplifié (IR foncier)
if base_imposable <= 3000: # Conversion approximative en Euros
    impot_an = 0
elif base_imposable <= 5000:
    impot_an = (base_imposable * 0.10) - 300
elif base_imposable <= 6000:
    impot_an = (base_imposable * 0.20) - 800
elif base_imposable <= 8000:
    impot_an = (base_imposable * 0.30) - 1400
elif base_imposable <= 18000:
    impot_an = (base_imposable * 0.34) - 1720
else:
    impot_an = (base_imposable * 0.38) - 2440

# Profit final
profit_mensuel_net_impot = (ca_an - charges_an - (mensualite * 12) - impot_an) / 12

# 6. KPI
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("CA Annuel", f"{int(ca_an)} €")
with c2:
    st.metric("Net Mensuel (Après Impôt)", f"{int(profit_mensuel_net_impot)} €")
with c3:
    renta = (profit_mensuel_net_impot * 12 / apport * 100) if apport > 0 else 0
    st.metric("Rendement / Apport", f"{renta:.1f} %")

st.markdown("---")

# 7. RÉCAPITULATIF FISCAL & TECHNIQUE
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("🇲🇦 Fiscalité Marocaine")
    st.write(f"Revenu Brut : **{int(ca_an)} €**")
    st.write(f"Abattement forfaitaire (40%) : **-{int(ca_an * 0.40)} €**")
    st.write(f"Base taxable : **{int(base_imposable)} €**")
    st.warning(f"Impôt annuel à payer : **{int(impot_an)} €**")

with col_b:
    st.subheader(f"🏦 Financement {type_pret}")
    st.write(f"Mensualité : **{int(mensualite)} €/mois**")
    st.write(f"Coût total crédit : **{int((mensualite * 12 * ans) - (0 if type_pret == 'In Fine' else m_pret))} €**")
    cap_terme = m_pret if type_pret == "In Fine" else 0
    st.write(f"Capital dû au terme : **{int(cap_terme)} €**")
