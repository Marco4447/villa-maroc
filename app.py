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

# --- LOGIQUE DE CALCUL GLOBALE (Source : Rapport Patrimonial) ---

# 1. Revenus réels d'exploitation
nb_nuits = 365 * (to / 100)
revenus_annuels = nb_nuits * adr

# 2. Charges d'exploitation totales (OpCo)
# [cite_start]Selon votre rapport : 25% de com [cite: 313] + [cite_start]35€ ménage/nuit [cite: 313]
commissions = revenus_annuels * 0.25 
frais_menage = nb_nuits * 35 
[cite_start]charges_fixes_annuelles = 14000 # Syndic, Jardin, Eau/Elec [cite: 313, 317]

# 3. Financement In Fine (Personnel)
montant_pret = prix_total - apport
interets_annuels = montant_pret * (taux_interet / 100)

# 4. Profit Net Global (Résultat OpCo + Flux Personnel)
# On calcule le surplus total réel après avoir payé le crédit
profit_annuel = revenus_annuels - commissions - frais_menage - charges_fixes_annuelles - interets_annuels
profit_mensuel = profit_annuel / 12

# --- AFFICHAGE ---

col1, col2 = st.columns(2)
with col1:
    st.metric("Revenu Brut Annuel", f"{revenus_annuels:,.0f} €".replace(",", " "))
with col2:
    # Ce chiffre réagira désormais à vos changements de TO et d'ADR
    st.metric("Profit Global Mensuel Net", f"{profit_mensuel:,.0f} €".replace(",", " "), delta=f"{to}% d'occupation")

st.markdown("---")

st.write("### 📈 Analyse de Performance")
st.write(f"Ce profit est calculé après paiement de **{interets_annuels/12:,.0f} €/mois** d'intérêts bancaires.")

# Point d'équilibre dynamique
marge_par_nuit = adr * 0.75 - 35
points_morts_charges = charges_fixes_annuelles + interets_annuels
seuil_to = (points_morts_charges / marge_par_nuit / 365 * 100) if marge_par_nuit > 0 else 100

if to >= seuil_to:
    st.success(f"Projet auto-financé. Seuil de rentabilité : **{seuil_to:.1f}%** d'occupation.")
else:
    st.error(f"Déficit d'exploitation. Seuil requis : **{seuil_to:.1f}%**.")

[cite_start]st.info(f"💡 Note : Vos **80 000 €** de liquidités couvrent **4,6 années** de service de dette sans aucun loyer[cite: 219, 324].")
