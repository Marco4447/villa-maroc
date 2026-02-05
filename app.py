import streamlit as st
import pandas as pd

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Audit Villa Marrakech", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    h1, h2, h3 { color: #D4AF37 !important; }
    div[data-testid="stMetric"] { 
        background-color: #161B22; border: 1px solid #D4AF37; 
        padding: 15px; border-radius: 10px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRE LATÉRALE - RÉGLAGES PAR SECTIONS (FLECHES)
with st.sidebar:
    st.header("⚙️ Paramètres")
    
    with st.expander("🏦 Financement", expanded=False):
        type_pret = st.radio("Type de prêt", ["In Fine", "Amortissable"])
        m_pret = st.number_input("Capital emprunté (€)", value=470000)
        tx_annuel = st.slider("Taux d'intérêt (%)", 0.0, 10.0, 3.7, step=0.1)
        ans = st.slider("Durée (ans)", 5, 25, 15)

    with st.expander("📅 Revenus & Occupation", expanded=True):
        adr = st.number_input("Prix Nuitée (€)", value=430)
        occ = st.slider("Occupation (%)", 0, 100, 45)

    with st.expander("💸 Charges & Fiscalité", expanded=True):
        f_fixes = st.number_input("Charges fixes mensuelles (€)", value=1650)
        com_concierge = st.slider("Conciergerie (%)", 0, 30, 20)
        com_airbnb = st.slider("Frais Airbnb/Booking (%)", 0, 20, 3)
        statut = st.selectbox("Régime Fiscal", ["Personne Physique", "Personne Morale"])

# 3. MOTEUR DE CALCULS FINANCIERS
nb_m = ans * 12
tm = tx_annuel / 100 / 12
tableau = []
capital_restant = m_pret

# --- Calcul du Crédit ---
if type_pret == "Amortissable":
    mens = m_pret * (tm / (1 - (1 + tm)**-nb_m)) if tm > 0 else m_pret / nb_m
    for i in range(1, nb_m + 1):
        interet = capital_restant * tm
        princ = mens - interet
        capital_restant -= princ
        tableau.append([i, round(mens, 2), round(princ, 2), round(interet, 2), round(max(0, capital_restant), 2)])
else:
    mens = m_pret * tm
    for i in range(1, nb_m + 1):
        p_final = m_pret if i == nb_m else 0
        tableau.append([i, round(mens + p_final, 2), p_final, round(mens, 2), m_pret if i < nb_m else 0])

# --- Rentabilité & Fiscalité ---
rev_brut_m = adr * 30.5 * (occ / 100)
frais_gestion = rev_brut_m * ((com_concierge + com_airbnb) / 100)

if statut == "Personne Physique":
    # Base taxable = 60% du CA (abattement 40%), Taxe = 15%
    base_t = rev_brut_m * 0.60
    impot_m = base_t * 0.15
else:
    # Personne Morale = 20% sur bénéfice net réel
    benef_is = rev_brut_m - frais_gestion - f_fixes - mens
    impot_m = max(0, benef_is * 0.20)

profit_net = rev_brut_m - frais_gestion - f_fixes - mens - impot_m

# 4. AFFICHAGE ÉCRAN PRINCIPAL
st.title("🏰 Audit de Rentabilité Financière")

# Bandeau de KPIs
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Profit Net / Mois", f"{int(profit_net)} €")
with c2: st.metric("Mensualité Crédit", f"{int(mens)} €")
with c3: st.metric("Impôt Mensuel", f"{int(impot_m)} €")
dscr = (
