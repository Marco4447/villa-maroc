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

# 3. TITRE PRINCIPAL
st.title("🏰 Simulation de rentabilité de votre villa")
st.markdown("---")

# 4. BARRE LATÉRALE (PARAMÈTRES)
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
with col2:
    st.metric("Profit Mensuel Net", f"{int(profit_mensuel_net):,} €".replace(",", " "))
with col3:
    renta_apport = (profit_annuel_net / apport_perso * 100) if apport_perso > 0 else 0
    st.metric("Rendement / Apport", f"{renta_apport:.1f} %")

st.markdown("---")

# 7. ANALYSE DÉTAILLÉE AU CENTRE
c1, c2 = st.columns(2)

with c1:
    st.write("### 📊 Performance Locative")
    st.write(f"Nuits louées par an : **{int(nb_nuits)} nuits**")
    st.write(f"Charges d'exploitation : **{int(charges_totales_an):,} € / an**".replace(",", " "))
    
    # Calcul du Point Mort
    marge_par_nuit = adr * (1 - com_gestion/100) - frais_menage_nuit
    if marge_par_nuit > 0:
        seuil_to = (frais_fixes_an + interets_annuels) / marge_par_nuit / 3.65
        st.write(f"Point mort (Équilibre) : **{seuil_to:.1f} % d'occupation**")
    else:
        st.write("⚠️ Prix de nuitée trop bas pour couvrir les frais variables.")

with c2:
    st.write("### 🏦
