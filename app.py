import streamlit as st

# 1. CONFIGURATION (Première ligne impérative)
st.set_page_config(page_title="Audit Villa Maroc", layout="wide")

# 2. MASQUAGE TOTAL DES MENTIONS "BUILT WITH STREAMLIT"
st.markdown("""
    <style>
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
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
        to = st.slider("Occupation Actuelle (%)", 0, 100, 41)
        
    with st.expander("💸 Frais Villa", expanded=True):
        com_concierge = st.slider("Conciergerie (%)", 0, 40, 20)
        energie_mois = st.number_input("Energie / mois (€)", value=350)
        menage_mois = st.number_input("Ménage / mois (€)", value=1000)
        taxe_fonciere_an = st.number_input("Taxe Foncière / an (€)", value=3000)
        jardin_mois = st.number_input("Jardin / mois (€)", value=200)
        fixes_mois = st.number_input("Assurances / mois (€)", value=100)

# 4. MOTEUR DE CALCUL
def calculer_sim(occ):
    # Mensualité
    if type_pret == "In Fine":
        mens = (m_pret * (tx_annuel / 100)) / 12
    else:
        tm = tx_annuel / 100 / 12
        nm = ans * 12
        mens = m_pret * (tm / (1 - (1 + tm)**-nm)) if tm > 0 else m_pret / nm
    
    # CA et Impôts Maroc
    ca = 365 * (occ / 100) * adr
    base_taxe = ca * 0.60
    if base_taxe <= 3000: imp = 0
    elif base_taxe <= 18000: imp = (base_taxe * 0.34) - 1720
    else: imp = (base_taxe * 0.38) - 2440
    
    fixes_an = taxe_fonciere_an + (energie_mois + menage_mois + jardin_mois + fixes_mois) * 12
    tot_charges = (ca * com_concierge / 100) + fixes_an + (mens * 12) + imp
    return ca, (ca - tot_charges) / 12, mens, imp, base_taxe

# Résultats actuels
ca_act, pr_act, ms_act, im_act, bs_act = calculer_sim(to)

# Seuil de rentabilité (Point Mort)
occ_seuil = 0
for i in range(0, 101):
    _, p_test, _, _, _ = calculer_sim(i)
    if p_test >= 0:
        occ_seuil = i
        break

# 5. AFFICHAGE
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("CA Annuel Estimé", str(int(ca_act)) + " €")
with c2:
    st.metric("Profit Net Mensuel", str(int(pr_act)) + " €")
with c3:
    renta = (pr_act * 12 / apport * 100) if apport > 0 else 0
    st.metric("Rentabilité / Apport", str(round(renta, 1)) + " %")

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.subheader("📊 Performance Détaillée")
    st.write("• Impôts Maroc :", int(im_act), "€/an")
    st.write("• Taux d'impôt effectif :", round((im_act/ca_act*100) if ca_act > 0 else 0, 1), "%")

with col2:
    st.subheader("🏁 Seuil de Rentabilité Réel")
    st.write("• Nuits minimum :", int(365 * occ_seuil / 100), "nuits/an")
    st.info("Occupation minimum requise : " + str(occ_seuil) + " %")

st.markdown("---")
st.subheader("🏦 Financement " + type_pret)
st.write("Mensualité :", int(ms_act), "€/mois | Capital dû au terme :", int(m_pret if type_pret == "In Fine" else 0), "€")
