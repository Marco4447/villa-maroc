import streamlit as st

# 1. CONFIGURATION (Doit être la première ligne)
st.set_page_config(page_title="Audit Villa Maroc", layout="wide")

# 2. DESIGN & SUPPRESSION DES MENTIONS STREAMLIT (White Label)
st.markdown("""
    <style>
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    .stAppDeployButton {display: none !important;}
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
        energie_mois = st.number_input("Eau & Elec / mois (€)", value=350)
        menage_mois = st.number_input("Ménage / mois (€)", value=1000)
        taxe_fonciere_an = st.number_input("Taxe Foncière / an (€)", value=3000)
        jardin_mois = st.number_input("Jardin & Piscine / mois (€)", value=200)
        fixes_mois = st.number_input("Assurances & Internet / mois (€)", value=100)

# 4. FONCTION FISCALE MAROC
def calculer_tout(taux_occ, adr_val, m_pret_val, tx_pret_val, ans_val, type_p):
    # Crédit
    if type_p == "In Fine":
        mens = (m_pret_val * (tx_pret_val / 100)) / 12
    else:
        tm = tx_pret_val / 100 / 12
        nm = ans_val * 12
        mens = m_pret_val * (tm / (1 - (1 + tm)**-nm)) if tm > 0 else m_pret_val / nm
    
    # Exploitation
    ca = 365 * (taux_occ / 100) * adr_val
    c_fixes = taxe_fonciere_an + (energie_mois + menage_mois + jardin_mois + fixes_mois) * 12
    
    # Impôt Maroc
    base = ca * 0.60
    if base <= 3000: imp = 0
    elif base <= 18000: imp = (base * 0.34) - 1720
    else: imp = (base * 0.38) - 2440
    
    total_frais = (ca * com_concierge / 100) + c_fixes + (mens * 12) + imp
    profit = (ca - total_frais) / 12
    return ca, profit, mens, imp

# 5. CALCULS ACTUELS ET SEUIL RÉEL
ca_actuel, profit_actuel, mens_actuel, imp_actuel = calculer_tout(to, adr, m_pret, tx_annuel, ans, type_pret)

# Recherche du seuil (Point Mort)
occ_seuil = 0
for test_o in range(0, 101):
    _, p_test, _, _ = calculer_tout(test_o, adr, m_pret, tx_annuel, ans, type_pret)
    if p_test >= 0:
        occ_seuil = test_o
        break

# 6. AFFICHAGE
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("CA Annuel Estimé", f"{int(ca_actuel)} €")
with c2:
    st.metric("Profit Net Mensuel", f"{int(profit_actuel)} €")
with c3:
    renta = (profit_actuel * 12 / apport * 100) if apport > 0 else 0
    st.metric("Rentabilité / Apport", f"{round(renta, 1)} %")

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.subheader("📊 Performance Détaillée")
    st.write(f"• Impôts Maroc : **{int(imp_actuel)} €/an**")
    st.write(f"• Taux d'impôt effectif : **{round((imp_actuel/ca_actuel*100) if ca_actuel > 0 else 0, 1)} %**")

with col2:
    st.subheader("🏁 Seuil de Rentabilité Réel")
    ca_seuil = 365 * (occ_seuil / 100) * adr
    st.write(f"• CA d'équilibre : **{int(ca_seuil)} €/an**")
    st.write(f"• Nuits minimum : **{int(365 * occ_seuil / 100)} nuits/an**")
    st.info(f"Occupation minimum requise : {occ_seuil} %")

st.markdown("---")
st.subheader(f"🏦 Détails du Crédit {type_pret}")
st.write(f"Mensualité : **{int(mens_actuel)} €/mois** | Capital dû au terme : **{int(m_pret if type_pret == 'In Fine' else 0)} €**")
