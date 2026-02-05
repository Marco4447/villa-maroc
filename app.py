import streamlit as st

# 1. CONFIGURATION
st.set_page_config(page_title="Simulation de rentabilité", layout="wide")

# 2. STYLE VISUEL (Design Sombre & Or)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    h1, h2, h3 { color: #D4AF37 !important; }
    div[data-testid="stMetric"] { 
        background-color: #161B22; 
        border: 1px solid #D4AF37; 
        padding: 15px; 
        border-radius: 10px; 
    }
    div[data-testid="stMetricValue"] > div { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. TITRE
st.title("🏰 Simulation de rentabilité de votre villa")
st.markdown("---")

# 4. PARAMÈTRES (Sidebar)
with st.sidebar:
    st.header("⚙️ Réglages")
    prix_total = st.slider("Investissement (€)", 500000, 1500000, 670000, 10000)
    apport = st.slider("Apport (€)", 0, 1000000, 200000, 10000)
    taux = st.number_input("Taux Crédit (%)", value=3.70, step=0.05)
    st.markdown("---")
    adr = st.slider("Prix Nuitée (€)", 300, 1500, 500, 25)
    to = st.slider("Occupation (%)", 0, 100, 45, 1)

# 5. CALCULS
pret = prix_total - apport
interets_mensuels = (pret * (taux / 100)) / 12
ca_annuel = 365 * (to / 100) * adr
charges_opco = (ca_annuel * 0.25) + (365 * (to / 100) * 35) + 14000
profit_mensuel = (ca_annuel - charges_opco - (interets_mensuels * 12)) / 12

# 6. AFFICHAGE DES RÉSULTATS
c1, c2, c3 = st.columns(3)
c1.metric("Chiffre d'Affaires", f"{int(ca_annuel)} €")
c2.metric("Profit Net Mensuel", f"{int(profit_mensuel)} €")
c3.metric("Rendement / Apport", f"{(profit_mensuel * 12 / apport * 100 if apport > 0 else 0):.1f} %")

st.markdown("---")

# 7. ANALYSE RAPIDE
col_a, col_b = st.columns(2)
with col_a:
    st.write("### 💎 Crédit & Charges")
    st.write(f"Prêt In Fine : **{pret:,} €**")
    st.write(f"Intérêts : **{int(interets_mensuels)} € / mois**")
with col_b:
    st.write("### 🛡️ Sécurité")
    st.info("Réserve de 80 000 € disponible.")
    st.write("- Paul (Nue-propriété)")
    st.write("- Emmanuelle (Réversion)")
