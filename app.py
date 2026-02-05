import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Simulation de rentabilité", layout="wide")

# 2. DESIGN (Sombre & Or)
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

# 4. BARRE LATÉRALE (RÉGLAGES)
with st.sidebar:
    st.header("⚙️ Paramètres")
    prix_total = st.slider("Prix de la Villa (€)", 500000, 1500000, 670000, 10000)
    apport = st.slider("Votre Apport (€)", 0, 1000000, 200000, 10000)
    
    st.subheader("🏦 Financement In Fine")
    taux = st.number_input("Taux du crédit (%)", value=3.70, step=0.05)
    duree_ans = st.number_input("Durée (années)", value=15, step=1)
    
    st.subheader("📅 Exploitation")
    adr = st.slider("Prix Nuitée (€)", 300, 1500, 500, 25)
    to = st.slider("Occupation (%)", 0, 100, 45, 1)

# 5. CALCULS FINANCIERS
pret = prix_total - apport
interets_annuels = pret * (taux / 100)
mensualite_interets = interets_annuels / 12
cout_total_credit = interets_annuels * duree_ans

ca_annuel = 365 * (to / 100) * adr
# Charges selon le rapport : 25% de com + 35e ménage/nuit + 14000 de fixes
charges_totales = (ca_annuel * 0.25) + (365 * (to / 100) * 35) + 14000
profit_mensuel = (ca_annuel - charges_totales - interets_annuels) / 12

# 6. AFFICHAGE DES INDICATEURS
c1, c2, c3 = st.columns(3)
c1.metric("Chiffre d'Affaires", f"{int(ca_annuel):,} €".replace(",", " "))
c2.metric("Profit Net Mensuel", f"{int(profit_mensuel):,} €".replace(",", " "))
c3.metric("Rendement / Apport", f"{(profit_mensuel * 12 / apport * 100 if apport > 0 else 0):.1f} %")

st.markdown("---")

# 7. DÉTAILS DU CRÉDIT ET SÉCURITÉ
col_a, col_b = st.columns(2)

with col_a:
    st.write("### 🏦 Détails du Financement")
    st.write(f"Montant du prêt In Fine : **{pret:,} €**".replace(",", " "))
    st.write(f"Durée du remboursement : **{duree_ans} ans**")
    st.write(f"Mensualité (Intérêts seuls) : **{int(mensualite_interets):,} € / mois**".replace(",", " "))
    st.write(f"Coût total des intérêts : **{int(cout_total_credit):,} €**".replace(",", " "))
    st.warning("Rappel : Le capital est remboursé en totalité à la fin des 15 ans.")

with col_b:
    st.write("### 🛡️ Protection Familiale")
    st.info("Réserve de 80 000 € (4,6 ans de mensualités)")
    st.write("- **Paul** : Futur propriétaire du capital.")
    st.write("- **Emmanuelle** : Protection via réversion d'usufruit.")
    st.write("- **Stratégie** : Conservation du cash-flow en quasi-usufruit.")
