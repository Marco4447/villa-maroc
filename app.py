import streamlit as st
import pandas as pd

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="Simulation de rentabilité",
    page_icon="🏰",
    layout="wide"
)

# 2. DESIGN PERSONNALISÉ (CSS)
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    h1, h2, h3 {
        color: #D4AF37 !important;
        font-family: 'serif';
    }
    div[data-testid="stMetric"] {
        background-color: #161B22;
        border: 1px solid #D4AF37;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    div[data-testid="stMetricValue"] > div {
        color: #D4AF37 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ENTÊTE
st.title("🏰 Simulation de rentabilité de votre villa")
st.subheader("Ingénierie Patrimoniale & Performance Locative")
st.markdown("---")

# 4. BARRE LATÉRALE (INPUTS)
with st.sidebar:
    st.header("⚙️ Configuration")
    
    with st.expander("💳 Financement In Fine", expanded=True):
        prix_total = st.slider("Investissement Global (€)", 500000, 1500000, 670000, step=10000)
        apport = st.slider("Apport Personnel (€)", 0, 1000000, 200000, step=10000)
        taux_interet = st.number_input("Taux Crédit (%)", value=3.70, step=0.05)
    
    with st.expander("📅 Exploitation OpCo", expanded=True):
        adr = st.slider("Prix Nuitée (ADR €)", 300, 1500, 500, step=25)
        to = st.slider("Occupation Annuelle (%)", 0, 100, 45, step=1)

# 5. LOGIQUE DE CALCUL
nb_nuits = 365 * (to / 100)
revenus_annuels = nb_nuits * adr

# Frais d'exploitation
commissions = revenus_annuels * 0.25 
frais_menage = nb_nuits * 35 
charges_fixes = 14000

# Financement
montant_pret = prix_total - apport
interets_annuels = montant_pret * (taux_interet / 100) 

# Résultat
profit_global_annuel = revenus_annuels - commissions - frais_menage - charges_fixes - interets_annuels
profit_global_mensuel = profit_global_annuel / 12

# 6. AFFICHAGE DU TABLEAU DE BORD
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Chiffre d'Affaires", f"{revenus_annuels:,.0f} €".replace(",", " "))

with col2:
    st.metric("Profit Net / Mois", f"{profit_global_mensuel:,.0f} €".replace(",", " "), delta=f"TO {to}%")

with col3:
    renta_apport = (profit_global_annuel / apport * 100) if apport > 0 else 0
    st.metric("Rendement / Apport", f"{renta_apport:.1f} %")

st.markdown("---")

# 7. ANALYSE ET SÉCURITÉ
c1, c2 = st.columns([2, 1])

with c1:
    st.write("### 💎 Analyse du Montage")
    st.write(f"Le projet repose sur un crédit In Fine de **{montant_pret:,.0f} €**. Le service de la dette s'élève à **{interets_annuels/12:,.0f} € / mois**.")
    
    marge_nuit = adr * 0.75 - 35
    seuil_to = ((charges_fixes + interets_annuels) / marge_nuit / 365 * 100) if marge_nuit > 0 else 0
    
    if to >= seuil_to:
        st.success(f"✅ Seuil d'équilibre atteint à {seuil_to:.1f}% d'occupation.")
    else:
        st.error(f"⚠️ Seuil d'équilibre non atteint (Requis : {seuil_to:.1f}%)")

with c2:
    st.write("###
