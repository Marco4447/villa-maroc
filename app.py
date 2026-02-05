import streamlit as st
import pandas as pd

# Configuration pro
st.set_page_config(page_title="Simulateur Villa Marrakech", layout="centered")

st.title("🏡 Simulateur de Rentabilité - Villa n°31")
st.markdown("---")

# --- BARRE LATÉRALE : PARAMÈTRES DU RAPPORT ---
st.sidebar.header("🕹️ Ajustez vos Hypothèses")

# Acquisition & Financement
prix_total = st.sidebar.slider("Coût global du projet (€)", 500000, 1000000, 670000, step=10000)
apport = st.sidebar.slider("Votre Apport personnel (€)", 0, 500000, 200000, step=10000)
taux_interet = st.sidebar.number_input("Taux d'intérêt In Fine (%)", value=3.70, step=0.05)

st.sidebar.markdown("---")

# Exploitation Locative
adr = st.sidebar.slider("Prix de la nuitée (ADR en €)", 300, 1000, 435, step=10)
to = st.sidebar.slider("Taux d'occupation annuel (%)", 0, 100, 45, step=1)

# --- CALCULS FINANCIERS (Source : Rapport Design 2) ---

# Financement In Fine
montant_pret = prix_total - apport
interets_mensuels = (montant_pret * (taux_interet / 100)) / 12

# Revenus & Charges OpCo
revenus_annuels = 365 * (to / 100) * adr
commissions_gestion = revenus_annuels * 0.25 # 25% Conciergerie/Plateformes [cite: 313]
frais_menage = (365 * (to / 100)) * 35 # 35€ par nuit louée [cite: 313]
charges_fixes = 14000 # Syndic, Jardin, Eau, Elec, Assurance [cite: 313, 317]

# Cash-Flow Personne Physique
loyer_opco_fixe = 24000 # Loyer versé à vous par la société [cite: 192, 303]
cash_flow_net_mensuel = (loyer_opco_fixe / 12) - interets_mensuels - (charges_fixes / 12)

# --- AFFICHAGE ---

# Métriques principales
col1, col2 = st.columns(2)
with col1:
    st.metric("Revenu Locatif Annuel", f"{revenus_annuels:,.0f} €".replace(",", " "))
with col2:
    st.metric("Cash-Flow Net Mensuel", f"{cash_flow_net_mensuel:,.0f} €".replace(",", " "))

st.markdown("---")

# Analyse de Résilience
st.write("### 🛡️ Sécurité du Financement")
st.write(f"Avec un prêt de **{montant_pret:,.0f} €**, vos intérêts s'élèvent à **{interets_mensuels:,.0f} €/mois**.")

# Point d'équilibre
marge_brute_nuit = adr - (adr * 0.25) - 35
seuil_nuits = (charges_fixes + (interets_mensuels * 12)) / marge_brute_nuit if marge_brute_nuit > 0 else 0
seuil_to = (seuil_nuits / 365) * 100

if to >= seuil_to:
    st.success(f"Le projet est auto-financé. Seuil de rentabilité : {seuil_to:.1f}% d'occupation.")
else:
    st.warning(f"Déficit d'exploitation. Seuil requis : {seuil_to:.1f}%.")

st.info(f"💡 Note : Vos **80 000 €** de liquidités couvrent **4,6 années** de service de dette sans aucun loyer.")
