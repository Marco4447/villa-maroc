import streamlit as st
import pandas as pd

# Configuration pro
st.set_page_config(page_title="Simulateur Villa Marrakech", layout="centered")

st.title("🏡 Simulateur de Performance Globale - Villa n°31")
st.markdown("---")

# --- BARRE LATÉRALE ---
st.sidebar.header("🕹️ Ajustez vos Hypothèses")

prix_total = st.sidebar.slider("Coût global du projet (€)", 500000, 1500000, 670000, step=10000)
apport = st.sidebar.slider("Votre Apport personnel (€)", 0, 1000000, 200000, step=10000)
taux_interet = st.sidebar.number_input("Taux d'intérêt In Fine (%)", value=3.70, step=0.05)

st.sidebar.markdown("---")

adr = st.sidebar.slider("Prix de la nuitée (ADR en €)", 300, 1000, 435, step=10)
to = st.sidebar.slider("Taux d'occupation annuel (%)", 0, 100, 45, step=1)

# --- LOGIQUE DE CALCUL GLOBALE (Données du Rapport) ---
nb_nuits = 365 * (to / 100)
revenus_annuels = nb_nuits * adr

# Charges basées sur les annexes du rapport
commissions = revenus_annuels * 0.25 
frais_menage = nb_nuits * 35 
charges_fixes_annuelles = 14000 

# Financement In Fine
montant_pret = prix_total - apport
interets_annuels = montant_pret * (taux_interet / 100)

# Profit réel total
profit_total_annuel = revenus_annuels - commissions - frais_menage - charges_fixes_annuelles - interets_annuels
profit_total_mensuel = profit_total_annuel / 12

# --- AFFICHAGE ---
col1, col2 = st.columns(2)
with col1:
    st.metric("Revenu Brut Annuel", f"{revenus_annuels:,.0f} €".replace(",", " "))
with col2:
    st.metric("Profit Global Mensuel Net", f"{profit_total_mensuel:,.0f} €".replace(",", " "), delta=f"{to}% d'occ.")

st.markdown("---")
st.write("### 📈 Analyse de Performance")
st.write(f"Ce montant est le surplus après paiement des intérêts de **{interets_annuels/12:,.0f} €/mois**.")

# Point d'équilibre dynamique
marge_par_nuit = adr * 0.75 - 35
points_morts_charges = charges_fixes_annuelles + interets_annuels
seuil_to = (points_morts_charges / marge_par_nuit / 365 * 100) if marge_par_nuit > 0 else 100

if to >= seuil_to:
    st.success(f"Projet rentable. Seuil d'équilibre : **{seuil_to:.1f}%** d'occupation.")
else:
    st.error(f"Déficit. Seuil requis : {seuil_to:.1f}%.")

st.info(f"💡 Rappel : Vos **80 000 €** couvrent le service de dette pendant **4,6 ans** sans loyer.")
