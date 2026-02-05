import streamlit as st

# 1. CONFIGURATION
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

# 4. BARRE LATÉRALE (RÉGLAGES DYNAMIQUES)
with st.sidebar:
    st.header("⚙️ Configuration du Projet")
    prix_villa = st.number_input("Prix de la Villa (€)", value=670000, step=10000)
    
    st.markdown("---")
    st.subheader("🏦 Financement In Fine")
    # Paramètres demandés : crédit, apport, taux, années
    montant_credit = st.number_input("Montant du crédit (€)", value=470000, step=5000)
    apport_perso = st.number_input("Apport Personnel (€)", value=200000, step=5000)
    taux_annuel = st.number_input("Taux d'intérêt annuel (%)", value=3.70, step=0.05)
    duree_pret = st.slider("Nombre d'années du crédit", 1, 25, 15)
    
    st.markdown("---")
    st.subheader("📅 Exploitation")
    adr = st.slider("Prix Nuitée (€)", 300, 1500, 500, 25)
    to = st.slider("Taux d'occupation (%)", 0, 100, 45, 1)

# 5. LOGIQUE DE CALCUL
# Intérêts In Fine (seul le loyer de l'argent est payé mensuellement)
interets_annuels = montant_credit * (taux_annuel / 100)
mensualite_interets = interets_annuels / 12
cout_total_credit = interets_annuels * duree_pret

# Revenus et Charges
ca_annuel = 365 * (to / 100) * adr
charges_totales = (ca_annuel * 0.25) + (365 * (to / 100) * 35) + 14000
profit_mensuel = (ca_annuel - charges_totales - interets_annuels) / 12

# 6. INDICATEURS CLÉS
c1, c2, c3 = st.columns(3)
c1.metric("CA Annuel", f"{int(ca_annuel):,} €".replace(",", " "))
c2.metric("Profit Net Mensuel", f"{int(profit_mensuel):,} €".replace(",", " "))
renta_apport = (profit_mensuel *
