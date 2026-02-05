import streamlit as st
import pandas as pd

# 1. CONFIGURATION
st.set_page_config(page_title="Simulateur Patrimonial Universel", layout="wide")

# 2. BARRE LATÉRALE - SAISIE TOTALE DES DONNÉES
with st.sidebar:
    st.header("📋 Saisie des Données")
    
    with st.expander("🏦 Financement sur mesure", expanded=True):
        type_pret = st.radio("Type de prêt", ["Amortissable", "In Fine"])
        m_pret = st.number_input("Montant de l'emprunt (€)", value=470000)
        tx_annuel = st.slider("Taux d'intérêt annuel (%)", 0.0, 10.0, 3.7, step=0.1)
        ans = st.slider("Durée du crédit (années)", 5, 25, 15)

    with st.expander("📅 Hypothèses Locatives", expanded=True):
        adr = st.number_input("Prix moyen de la nuitée (€)", value=430)
        occ = st.slider("Taux d'occupation estimé (%)", 0, 100, 45)

    with st.expander("💸 Charges & Fiscalité", expanded=True):
        f_fixes_mensuels = st.number_input("Charges fixes mensuelles (€)", value=1650, help="Assurance, entretien, abonnements")
        com_airbnb_pct = st.slider("Frais Airbnb / Conciergerie (% du CA)", 0, 50, 25)
        impot_taux_est = st.slider("Taux d'imposition effectif (%)", 0, 45, 20, help="Estimation de l'impôt sur le bénéfice")

# 3. MOTEUR DE CALCUL UNIVERSEL
tm = tx_annuel / 100 / 12
nb_m = ans * 12
tableau = []
capital_du = m_pret

if type_pret == "Amortissable":
    mens = m_pret * (tm / (1 - (1 + tm)**-nb_m)) if tm > 0 else m_pret / nb_m
    for i in range(1, nb_m + 1):
        interets = capital_du * tm
        principal = mens - interets
        capital_du -= principal
        tableau.append([i, round(mens, 2), round(principal, 2), round(interets, 2), round(max(0, capital_du), 2)])
else:
    mens = m_pret * tm
    for i in range(1, nb_m + 1):
        p = 0 if i < nb_m else m_pret
        ech = mens if i < nb_m else mens + m_pret
        tableau.append([i, round(ech, 2), round(p, 2), round(mens, 2), m_pret if i < nb_m else 0])

# Calcul Rentabilité
ca_mensuel = adr * 30.5 * (occ / 100)
frais_airbnb = ca_mensuel * (com_airbnb_pct / 100)
base_imposable = max(0, ca_mensuel - frais_airbnb - f_fixes_mensuels - mens)
montant_impot = base_imposable * (impot_taux_est / 100)
profit_net_mensuel = ca_mensuel - frais_airbnb - f_fixes_mensuels - mens - montant_impot

# 4. AFFICHAGE ÉCRAN PRINCIPAL
st.title("🏰 Simulateur de Rentabilité Personnalisable")

# Bandeau de KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Cash-Flow Net Mensuel", f"{int(profit_net_mensuel)} €")
c2.metric("Revenu Brut Annuel", f"{int(ca_mensuel * 12)} €")
c3.metric("Mensualité Crédit", f"{int(mens)} €")
c4.metric("DSCR", f"{round((ca_mensuel - frais_airbnb - f_fixes_mensuels)/mens, 2) if mens > 0 else 0}")

st.markdown("---")

# Détails
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("📝 Détail des flux (Mensuel)")
    st.write(f"• Chiffre d'Affaires : **{int(ca_mensuel)} €**")
    st.write(f"• Frais Airbnb/Gestion ({com_airbnb_pct}%) : **-{int(frais_airbnb)} €**")
    st.write(f"• Charges Fixes : **-{int(f_fixes_mensuels)} €**")
    st.write(f"• Impôt estimé : **-{int(montant_impot)} €**")

with col_b:
    st.subheader("🏁 Point Mort")
    # Calcul simplifié du seuil
    seuil_ca = (f_fixes_mensuels + mens) / (1 - (com_airbnb_pct/100) - (impot_taux_est/100 if ca_mensuel > (frais_airbnb + f_fixes_mensuels + mens) else 0))
    occ_equilibre = (seuil_ca / (adr * 30.5)) * 100
    st.info(f"Équilibre atteint à **{int(occ_equilibre)}%** d'occupation.")

st.markdown("---")
st.subheader(f"📊 Tableau d'Amortissement Dynamique ({type_pret})")
df_a = pd.DataFrame(tableau, columns=["Mois", "Échéance", "Principal", "Intérêts", "Restant"])
st.dataframe(df_a, use_container_width=True, height=400, hide_index=True)
