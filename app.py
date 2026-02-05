import streamlit as st
import pandas as pd

# 1. CONFIGURATION DE BASE
st.set_page_config(page_title="Audit Villa", layout="wide")

# 2. BARRE LATÉRALE
with st.sidebar:
    st.header("⚙️ Réglages")
    type_pret = st.radio("Type", ["Amortissable", "In Fine"])
    m_pret = st.number_input("Montant (€)", value=470000)
    tx_annuel = st.slider("Taux (%)", 0.0, 10.0, 3.7)
    ans = st.slider("Durée (ans)", 5, 25, 15)
    
    st.markdown("---")
    adr = st.number_input("Prix Nuit (€)", value=430)
    occ = st.slider("Occupation (%)", 0, 100, 41)
    
    st.markdown("---")
    f_fixes = st.number_input("Charges Fixes (€)", value=1650)
    com_pct = st.slider("Commission (%)", 0, 40, 20)
    statut = st.selectbox("Statut", ["Physique", "Morale"])

# 3. CALCUL AMORTISSEMENT
nb_m = ans * 12
tm = tx_annuel / 100 / 12
tableau = []
cr = m_pret

if type_pret == "Amortissable":
    mens = m_pret * (tm / (1 - (1 + tm)**-nb_m)) if tm > 0 else m_pret / nb_m
    for i in range(1, nb_m + 1):
        int_m = cr * tm
        princ = mens - int_m
        cr -= princ
        tableau.append([i, mens, princ, int_m, max(0, cr)])
else:
    mens = (m_pret * (tx_annuel / 100)) / 12
    for i in range(1, nb_m + 1):
        p = 0 if i < nb_m else m_pret
        tableau.append([i, mens if i < nb_m else mens + m_pret, p, mens, 0 if i == nb_m else m_pret])

df = pd.DataFrame(tableau, columns=["Mois", "Echeance", "Principal", "Interets", "Restant"])

# 4. CALCUL RENTABILITÉ
rev_brut = adr * 30.5 * (occ / 100)
f_vars = rev_brut * (com_pct / 100)

def calcul_impot(r, s):
    if s == "Physique":
        base = (r * 12) * 0.60
        if base <= 30000: return 0
        elif base <= 180000: return ((base * 0.34) - 17200) / 12
        else: return ((base * 0.38) - 24400) / 12
    else:
        base = (r * 12) - (f_fixes * 12) - (mens * 12)
        return (max(0, base) * 0.20) / 12

impot = calcul_impot(rev_brut, statut)
profit = rev_brut - f_vars - f_fixes - mens - impot

# 5. AFFICHAGE PRINCIPAL
st.title("🏰 Audit de Rentabilité")

c1, c2, c3 = st.columns(3)
c1.metric("Revenu Brut", f"{int(rev_brut)} €")
c2.metric("Profit Net", f"{int(profit)} €")
c3.metric("Mensualité", f"{int(mens)} €")

st.markdown("---")
st.subheader("📊 Tableau d'Amortissement")
st.dataframe(df, use_container_width=True, height=400)
