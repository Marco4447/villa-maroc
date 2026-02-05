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

# 2. BARRE LATÉRALE - PARAMÈTRES MODULABLES
with st.sidebar:
    st.header("⚙️ Configuration")
    
    with st.expander("🏦 Financement", expanded=True):
        type_p = st.radio("Type de prêt", ["In Fine", "Amortissable"])
        m_p = st.number_input("Capital (€)", value=470000)
        t_a = st.slider("Taux (%)", 0.0, 10.0, 3.7)
        ans = st.slider("Durée (ans)", 5, 25, 15)

    with st.expander("📅 Revenus Airbnb", expanded=True):
        adr = st.number_input("Prix Nuitée (€)", value=430)
        occ = st.slider("Occupation (%)", 0, 100, 45)

    with st.expander("💸 Charges & Impôts", expanded=True):
        f_fix = st.number_input("Charges Fixes / mois (€)", value=1650)
        c_concierge = st.slider("Conciergerie (%)", 0, 30, 20)
        c_airbnb = st.slider("Frais Airbnb (%)", 0, 20, 3)
        regime = st.selectbox("Régime Fiscal", ["Personne Physique", "Personne Morale"])

# 3. CALCULS FINANCIERS
nb_m = ans * 12
tm = t_a / 100 / 12
tableau = []
capital_restant = m_p

# Calcul Mensualité
if type_p == "Amortissable":
    mens = m_p * (tm / (1 - (1 + tm)**-nb_m)) if tm > 0 else m_p / nb_m
    for i in range(1, nb_m + 1):
        interet = capital_restant * tm
        princ = mens - interet
        capital_restant -= princ
        tableau.append([i, mens, princ, interet, max(0, capital_restant)])
else:
    mens = m_p * tm
    for i in range(1, nb_m + 1):
        tableau.append([i, mens if i < nb_m else mens + m_p, m_p if i == nb_m else 0, mens, m_p if i < nb_m else 0])

# Rentabilité
rev_b = adr * 30.5 * (occ / 100)
f_var = rev_b * ((c_concierge + c_airbnb) / 100)

# Fiscalité (Abattement 40% pour PP ou Réel pour PM)
if regime == "Personne Physique":
    base_t = rev_b * 0.60
    impot = base_t * 0.15
else:
    benef = rev_b - f_var - f_fix - mens
    impot = max(0, benef * 0.20)

p_net = rev_b - f_var - f_fix - mens - impot

# 4. AFFICHAGE ÉCRAN PRINCIPAL
st.title("🏰 Audit de Performance Financière")

# Bandeau de Ratios (KPIs)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Profit Net / Mois", f"{int(p_net)} €")
col2.metric("Mensualité", f"{int(mens)} €")
col3.metric("Impôt", f"{int(impot)} €")
dscr = (rev_b - f_var - f_fix) / mens if mens > 0 else 0
col4.metric("DSCR", f"{dscr:.2f}")

st.markdown("---")

# Détails des flux
c_a, c_b = st.columns(2)
with c_a:
    st.subheader("📝 Flux de Trésorerie Mensuels")
    st.write(f"• Revenu Brut : **{int(rev_b)} €**")
    st.write(f"• Frais Gestion ({c_concierge + c_airbnb}%) : **-{int(f_var)} €**")
    st.write(f"• Charges Fixes : **-{int(f_fix)} €**")
    st.write(f"• Impôt ({regime}) : **-{int(impot)} €**")

with c_b:
    st.subheader
