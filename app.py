import streamlit as st

# 1. CONFIGURATION
st.set_page_config(page_title="Audit Rentabilité Villa", layout="wide")

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

st.title("🏰 Audit de rentabilité complet de votre villa")
st.markdown("---")

# 3. BARRE LATÉRALE
with st.sidebar:
    st.header("⚙️ Configuration")
    with st.expander("🏦 Financement", expanded=True):
        type_pret = st.radio("Type de crédit", ["In Fine", "Amortissable"])
        m_pret = st.number_input("Montant emprunté (€)", value=470000)
        apport = st.number_input("Apport personnel (€)", value=200000)
        tx_annuel = st.number_input("Taux annuel (%)", value=3.70)
        ans = st.slider("Durée du crédit (ans)", 1, 25, 15)

    with st.expander("📅 Revenus Locatifs", expanded=True):
        adr = st.number_input("Prix Nuitée (€)", value=430)
        to = st.slider("Occupation (%)", 0, 100, 27)
        
    with st.expander("💸 Frais Villa (Mensuels)", expanded=True):
        com_concierge = st.slider("Conciergerie (%)", 0, 40, 20)
        energie_mois = st.number_input("Eau & Elec / mois (€)", value=350)
        menage_mois = st.number_input("Ménage / mois (€)", value=1000)
        taxe_fonciere_an = st.number_input("Taxe Foncière / an (€)", value=3000)
        jardin_mois = st.number_input("Jardin & Piscine / mois (€)", value=200)
        fixes_mois = st.number_input("Assurances & Internet / mois (€)", value=100)

# 4. CALCULS FINANCIERS
if type_pret == "In Fine":
    mensualite = (m_pret * (tx_annuel / 100)) / 12
else:
    t_m = tx_annuel / 100 / 12
    n_m = ans * 12
    mensualite = m_pret * (t_m / (1 - (1 + t_m)**-n_m)) if t_m > 0 else m_pret / n_m

nuits_an = 365 * (to / 100)
ca_an = nuits_an * adr
charges_fixes_an = taxe_fonciere_an + (energie_mois + menage_mois + jardin_mois + fixes_mois) * 12
total_charges_an = (ca_an * com_concierge / 100) + charges_fixes_an

# 5. IMPOTS MAROC
base_taxable = ca_an * 0.60
if base_taxable <= 3000: impot_an = 0
elif base_taxable <= 18000: impot_an = (base_taxable * 0.34) - 1720
else: impot_an = (base_taxable * 0.38) - 2440

profit_mensuel = (ca_an - total_charges_an - (mensualite * 12) - impot_an) / 12

# 6. SEUIL DE RENTABILITÉ CORRIGÉ
# Revenu net par nuit après commission
adr_net = adr * (1 - (com_concierge / 100))
# Coûts fixes totaux à couvrir (Charges fixes + Crédit + Impôt moyen)
fixes_totaux = charges_fixes_an + (mensualite * 12) + impot_an
nuits_equilibre = fixes_totaux / adr_net if adr_net > 0 else 0
occ_equilibre = (nuits_equilibre / 365) * 100

# 7. AFFICHAGE
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("CA Annuel Estimé", str(int(ca_an)) + " €")
with c2:
    st.metric("Profit Net Mensuel", str(int(profit_mensuel)) + " €")
with c3:
    renta_val = (profit_mensuel * 12 / apport) * 100 if apport > 0 else 0
    st.metric("Rendement / Apport", str(round(renta_val, 1)) + " %")

st.markdown("---")

col_res1, col_res2 = st.columns(2)
with col_res1:
    st.subheader("📊 Performance Détaillée")
    st.write("• Total Charges Annuelles :", int(total_charges_an), "€")
    st.write("• Impôts Maroc :", int(impot_an), "€/an")
    st.write("• Taux d'impôt effectif :", round((impot_an/ca_an*100) if ca_an > 0 else 0, 1), "%")

with col_res2:
    st.subheader("🏁 Seuil de Rentabilité")
    st.write("• CA minimum (Équilibre) :", int(nuits_equilibre * adr), "€/an")
    st.write("• Nuits minimum :", int(nuits_equilibre), "nuits/an")
    st.info("Occupation minimum requise : " + str(int(occ_equilibre)) + " %")

st.markdown("---")
st.subheader("🏦 Détails du Crédit " + type_pret)
st.write("Mensualité :", int(mensualite), "€/mois | Capital dû au terme :", int(m_pret if type_pret == "In Fine" else 0), "€")
