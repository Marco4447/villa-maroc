import streamlit as st

# 1. CONFIGURATION
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

# 4. BARRE LATÉRALE (RÉGLAGES)
with st.sidebar:
    st.header("⚙️ Paramètres")
    
    with st.expander("🏦 Financement (Prêt In Fine)", expanded=True):
        mont_pret = st.number_input("Montant emprunté (€)", value=470000, step=5000)
        apport = st.number_input("Apport injecté (€)", value=200000, step=5000)
        tx = st.number_input("Taux annuel (%)", value=3.70, step=0.05)
        ans = st.slider("Durée du crédit (ans)", 1, 25, 15)

    with st.expander("📅 Performance Villa", expanded=True):
        adr = st.slider("Prix Nuitée (€)", 200, 2000, 500, 25)
        to = st.slider("Occupation (%)", 0, 100, 45, 1)
        
    with st.expander("💸 Charges & Frais", expanded=False):
        fixe = st.number_input("Frais fixes annuels (€)", value=14000, step=500)
        com = st.slider("Gestion (%)", 0, 40, 25)
        menage = st.number_input("Ménage / nuit (€)", value=35, step=5)

# 5. LOGIQUE DE CALCUL
# Crédit
mensu_int = (mont_pret * (tx / 100)) / 12
tot_int = mensu_int * 12 * ans

# Exploitation
nuits = 365 * (to / 100)
ca = nuits * adr
frais_var = (ca * (com / 100)) + (nuits * menage)
total_charges = frais_var + fixe
profit_mensuel = (ca - total_charges - (mensu_int * 12)) / 12

# 6. AFFICHAGE DES RÉSULTATS (KPI)
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Chiffre d'Affaires Annuel", f"{int(ca):,} €".replace(",", " "))
with c2:
    st.metric("Profit Net Mensuel", f"{int(profit_mensuel):,} €".replace(",", " "))
with c3:
    renta = (profit_mensuel * 12 / apport * 100) if apport > 0 else 0
    st.metric("Rendement / Apport", f"{renta:.1f} %")

st.markdown("---")

# 7. DÉTAILS
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("📊 Performance Locative")
    st.write(f"Occupation réelle : **{int(nuits)} nuits/an**")
    st.write(f"Total des charges : **{int(total_charges):,} €/an**".replace(",", " "))
    
with col_b:
    st.subheader("🏦 Détails Bancaires")
    st.write(f"Mensualité (Intérêts) : **{int(mensu_int):,} €/mois**")
    st.write(f"Coût du crédit : **{int(tot_int):,} €** sur {ans} ans")

st.info("💡 La réserve de 80 000 € sécurise le projet en cas de vacance locative prolongée.")
