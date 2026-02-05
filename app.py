import streamlit as st
import pandas as pd

# 1. CONFIGURATION
st.set_page_config(page_title="Audit Expert - Villa Marrakech", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    h1, h2, h3 { color: #D4AF37 !important; }
    div[data-testid="stMetric"] { background-color: #161B22; border: 1px solid #D4AF37; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRE LATÉRALE - SAISIE TOTALE
with st.sidebar:
    st.header("⚙️ Paramètres d'Audit")
    
    with st.expander("🏦 Financement", expanded=False):
        type_pret = st.radio("Type de prêt", ["In Fine", "Amortissable"])
        m_pret = st.number_input("Capital emprunté (€)", value=470000)
        tx_annuel = st.slider("Taux (%)", 0.0, 10.0, 3.7, step=0.1)
        ans = st.slider("Durée (ans)", 5, 25, 15)

    with st.expander("📅 Revenus Locatifs", expanded=True):
        adr = st.number_input("Prix Nuitée (€)", value=430)
        occ = st.slider("Occupation (%)", 0, 100, 45)

    with st.expander("💸 Charges & Fiscalité", expanded=True):
        f_fixes = st.number_input("Charges Fixes / mois (€)", value=1650)
        com_concierge = st.slider("Conciergerie (%)", 0, 30, 20)
        com_airbnb = st.slider("Frais Plateforme (%)", 0, 20, 3)
        statut = st.selectbox("Régime Fiscal Maroc", ["Personne Physique", "Personne Morale"])

# 3. MOTEUR DE CALCULS
nb_m = ans * 12
tm = tx_annuel / 100 / 12
tableau = []
cr = m_pret

# Calcul Mensualité
if type_pret == "Amortissable":
    mens = m_pret * (tm / (1 - (1 + tm)**-nb_m)) if tm > 0 else m_pret / nb_m
    for i in range(1, nb_m + 1):
        int_m = cr * tm
        princ = mens - int_m
        cr -= princ
        tableau.append([i, round(mens, 2), round(princ, 2), round(int_m, 2), round(max(0, cr), 2)])
else:
    mens = m_pret * tm
    for i in range(1, nb_m + 1):
        tableau.append([i, mens if i < nb_m else mens + m_pret, m_pret if i == nb_m else 0, mens, m_pret if i < nb_m else 0])

# Calcul Rentabilité & Impôt Dynamique
rev_brut_m = adr * 30.5 * (occ / 100)
frais_vars = rev_brut_m * ((com_concierge + com_airbnb) / 100)

# LOGIQUE FISCALE EXPERTE
if statut == "Personne Physique":
    # Impôt sur le CA brut (après abattement de 40%) - Taux RAS 15%
    base_fonciere = rev_brut_m * 0.60
    impot_m = base_fonciere * 0.15 #
else:
    # Impôt sur le Bénéfice (après déduction intérêts et charges) - Taux IS 20%
    benefice_avant_is = rev_brut_m - frais_vars - f_fixes - mens
    impot_m = max(0, benefice_avant_is * 0.20) #

profit_net = rev_brut_m - frais_vars - f_fixes - mens - impot_m

# 4. AFFICHAGE
st.title("🏰 Audit de Performance Immobilière")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Net / Mois", f"{int(profit_net)} €")
c2.metric("Impôt Mensuel", f"{int(impot_m)} €", delta=statut, delta_color="off")
c3.metric("Mensualité", f"{int(mens)} €")
c4.metric("DSCR", f"{round((rev_brut_m - frais_vars - f_fixes)/mens, 2) if mens > 0 else 0}")

st.markdown("---")
st.subheader(f"📊 Analyse des flux ({statut})")
col_a, col_b = st.columns(2)
with col_a:
    st.write(f"• Revenu Brut : **{int(rev_brut_m)} €**")
    st.write(f"• Gestion & Plateformes : **-{int(frais_vars)} €**")
    st.write(f"• Charges Fixes : **-{int(f_fixes)} €**")
    st.write(f"• Mensualité Banque : **-{int(mens)} €**")
    st.write(f"• **Impôt estimé : -{int(impot_m)} €**")

with col_b:
    st.info(f"**Note de l'Expert :** En **{statut}**, votre impôt est calculé sur une base de **{int(base_fonciere if statut=='Personne Physique' else max(0, benefice_avant_is))} €**.")
    if statut == "Personne Physique":
        st.warning("Attention : En PP, les intérêts bancaires ne réduisent pas votre impôt au Maroc.")
    else:
        st.success("Avantage IS : Vos intérêts et charges réduisent directement votre base imposable.")

st.markdown("---")
st.subheader("📅 Tableau d'Amortissement")
df_a = pd.DataFrame(tableau, columns=["Mois", "Échéance", "Principal", "Intérêts", "Restant"])
st.dataframe(df_a, use_container_width=True, height=350, hide_index=True)
