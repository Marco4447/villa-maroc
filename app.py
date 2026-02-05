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

# 3. TITRE
st.title("🏰 Simulation de rentabilité de votre villa")
st.markdown("---")

# 4. BARRE LATÉRALE (PARAMÈTRES AFFINÉS)
with st.sidebar:
    st.header("⚙️ Configuration")
    
    with st.expander("🏦 Financement (In Fine)", expanded=False):
        m_pret = st.number_input("Montant emprunté (€)", value=470000, step=5000)
        apport = st.number_input("Apport injecté (€)", value=200000, step=5000)
        tx = st.number_input("Taux annuel (%)", value=3.70, step=0.05)
        ans = st.slider("Durée du crédit (ans)", 1, 25, 15)

    with st.expander("📅 Revenus Locatifs", expanded=True):
        adr = st.slider("Prix Nuitée (€)", 200, 2000, 500, 25)
        to = st.slider("Occupation (%)", 0, 100, 45, 1)
        
    with st.expander("💸 Détail des Frais Villa", expanded=True):
        st.subheader("Charges Variables")
        com_concierge = st.slider("Conciergerie (%)", 0, 40, 25)
        menage_nuit = st.number_input("Ménage / nuitée (€)", value=35, step=5)
        
        st.subheader("Charges Fixes")
        taxe_hab = st.number_input("Taxe Habitation / Foncière (€)", value=3000, step=100)
        frais_fixes_autres = st.number_input("Entretien & Autres fixes (€)", value=11000, step=500)

# 5. LOGIQUE DE CALCUL
# Calcul bancaire
mensu_int = (m_pret * (tx / 100)) / 12

# Calcul exploitation
nuits = 365 * (to / 100)
ca_annuel = nuits * adr

# Ventilation des frais
frais_conciergerie = ca_annuel * (com_concierge / 100)
frais_menage_total = nuits * menage_nuit
total_fixes = taxe_hab + frais_fixes_autres
total_charges = frais_conciergerie + frais_menage_total + total_fixes

# Profit
profit_mensuel = (ca_annuel - total_charges - (mensu_int * 12)) / 12

# 6. AFFICHAGE DES RÉSULTATS (KPI)
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Chiffre d'Affaires Annuel", f"{int(ca_annuel):,} €".replace(",", " "))
with c2:
    st.metric("Profit Net Mensuel", f"{int(profit_mensuel):,} €".replace(",", " "))
with c3:
    renta = (profit_mensuel * 12 / apport * 100) if apport > 0 else 0
    st.metric("Rendement / Apport", f"{renta:.1f} %")

st.markdown("---")

# 7. RÉCAPITULATIF TECHNIQUE
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("📊 Détail des Charges Annuelles")
    st.write(f"Conciergerie ({com_concierge}%) : **{int(frais_conciergerie):,} €**".replace(",", " "))
    st.write(f"Ménages cumulés : **{int(frais_menage_total):,} €**".replace(",", " "))
    st.write(f"Taxes et Frais Fixes : **{int(total_fixes):,} €**".replace(",", " "))
    st.write(f"**Total Charges : {int(total_charges):,} €/an**".replace(",", " "))
    
with col_b:
    st.subheader("🏦 Détails Bancaires")
    st.write(f"Mensualité (Intérêts seuls) : **{int(mensu_int):,} €/mois**")
    st.write(f"Coût total des intérêts : **{int(mensu_int * 12 * ans):,} €**")
    st.write(f"Capital dû au terme : **{int(m_pret):,} €**".replace(",", " "))
