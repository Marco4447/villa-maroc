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
        text-align: center;
    }
    div[data-testid="stMetricValue"] > div { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. TITRE
st.title("🏰 Simulation de rentabilité de votre villa")
st.markdown("---")

# 4. BARRE LATÉRALE (PARAMÈTRES COMPLETS)
with st.sidebar:
    st.header("⚙️ Paramètres du Projet")
    
    with st.expander("🏦 Financement (Prêt In Fine)", expanded=True):
        montant_credit = st.number_input("Montant de l'emprunt (€)", value=470000, step=5000)
        apport_perso = st.number_input("Apport personnel (€)", value=200000, step=5000)
        taux_annuel = st.number_input("Taux d'intérêt (%)", value=3.70, step=0.05)
        duree_pret = st.slider("Durée du crédit (ans)", 1, 25, 15)

    with st.expander("📅 Performance de la Villa", expanded=True):
        adr = st.slider("Prix de la nuitée (€)", 200, 2000, 500, 25)
        to = st.slider("Taux d'occupation (%)", 0, 100, 45, 1)
        
    with st.expander("💸 Charges & Frais", expanded=False):
        frais_fixes_an = st.number_input("Charges fixes annuelles (€)", value=14000, step=500)
        com_gestion = st.slider("Commissions gestion (%)", 0, 40, 25)
        frais_menage_nuit = st.number_input("Frais ménage / nuitée (€)", value=35, step=5)

# 5. LOGIQUE DE CALCUL
# Partie Crédit
interets_annuels = montant_credit * (taux_annuel / 100)
mensualite_int = interets_annuels / 12

# Partie Exploitation
nb_nuits = 365 * (to / 100)
ca_annuel = nb_nuits * adr
frais_variables = (ca_annuel * (com_gestion / 100)) + (nb_nuits * frais_menage_nuit)
charges_totales_an = frais_variables + frais_fixes_an

# Résultats Nets
profit_annuel_net = ca_annuel - charges_totales_an - interets_annuels
profit_mensuel_net = profit_annuel_net / 12

# 6. AFFICHAGE DES INDICATEURS (KPI)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Chiffre d'Affaires Annuel", f"{int(ca_annuel):,} €".replace(",", " "))
