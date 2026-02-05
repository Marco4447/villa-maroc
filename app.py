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

# 2. BARRE LATÉRALE - RÉGLAGES MODULABLES
with st.sidebar:
    st.header("⚙️ Paramètres")
    
    with st.expander("🏦 Financement", expanded=False):
        type_pret = st.radio("Type de prêt", ["In Fine", "Amortissable"])
        m_pret = st.number_input("Capital emprunté (€)", value=470000)
        tx_annuel = st.slider("Taux d'intérêt annuel (%)", 0.0, 10.0, 3.7, step=0.1)
        ans = st.slider("Durée du crédit (ans)", 5, 25, 15)

    with st.expander("📅 Revenus & Occupation", expanded=True):
        adr = st.number_input("Prix de la nuitée moyen (€)", value=430)
        occ = st.slider("Taux d'occupation estimé (%)", 0, 100, 45)

    with st.expander("💸 Charges & Fiscalité", expanded=True):
        f_fixes = st.number_input("Charges fixes mensuelles (€)", value=1650)
        # SECTION CHARGES VARIABLES DÉTAILLÉES
        com_concierge_pct = st.slider("Commission Conciergerie (%)", 0, 30, 20)
        com_airbnb_pct = st.slider("Frais Airbnb/Booking (%)", 0, 20, 3)
        charges_ops_nuit = st.number_input("Consommables/Linge par nuitée (€)", value=35)
        
        statut = st.selectbox("Régime Fiscal", ["Personne Physique", "Personne Morale"])

# 3. MOTEUR DE CALCULS FINANCIERS
nb_m = ans * 12
tm = tx_annuel / 100 / 12
tableau = []
capital_restant = m_pret

# --- Calcul de la mensualité ---
if type_pret == "Amortissable":
    mens = m_pret * (tm / (1 - (1 + tm)**-nb_m)) if tm > 0 else m_pret / nb_m
    for i in range(1, nb_m + 1):
        int_m = capital_restant * tm
        princ_m = mens - int_m
        capital_restant -= princ_m
        tableau.append([i, round(mens, 2), round(princ_m, 2), round(int_m, 2), round(max(0, capital_restant), 2)])
else:
    mens = m_pret * tm
    for i in range(1, nb_m + 1):
        p_final = m_pret if i == nb_m else 0
        tableau.append([i, round(mens + p_final, 2), p_final, round(mens, 2), m_pret if i < nb_m else 0])

# --- Analyse de la Rentabilité ---
nuits_mois = 30.5 * (occ / 100)
rev_brut_m = adr * nuits_mois

# Calcul détaillé des charges variables
frais_com = rev_brut_m * ((com_concierge_pct + com_airbnb_pct) / 100)
frais_ops = charges_ops_nuit * nuits_mois
total_charges_vars = frais_com + frais_ops

# Fiscalité selon le régime (Abattement de 40% pour Personne Physique)
if statut == "Personne Physique":
    impot_m = (rev_brut_m * 0.60) * 0.15
else:
    benef_avant_is = rev_brut_m - total_charges_vars - f_fixes - mens
    impot_m = max(0, benef_avant_is * 0.20)

profit_net = rev_brut_m - total_charges_vars - f_fixes - mens - impot_m

# 4. AFFICHAGE ÉCRAN PRINCIPAL
st.title("🏰 Audit de Rentabilité Financière")

# Bandeau de KPIs
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Profit Net / Mois", f"{int(profit_net)} €")
with c2: st.metric("Mensualité Crédit", f"{int(mens)} €")
with c3: st.metric("Charges Variables", f"{int(total_charges_vars)} €")
dscr = (rev_brut_m - total_charges_vars - f_fixes) / mens if mens > 0 else 0
with c4: st.metric("Ratio DSCR", f"{dscr:.2f}", help="Indice de solvabilité (>1.20)")

st.markdown("---")

# Détails des Flux
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("📝 Détail des Flux Mensuels")
    st.write(f"• Revenu Brut : **{int(rev_brut_m)} €**")
    st.write(f"• Commissions (Concierge+Airbnb) : **-{int(frais_com)} €**")
    st.write(f"• Frais Ops (Linge/Énergie) : **-{int(frais_ops)} €**")
    st.write(f"• Charges Fixes : **-{int(f_fixes)} €**")
    st.write(f"• Impôt ({statut}) : **-{int(impot_m)} €**")

with col_b:
    st.subheader("🏁 Point d'Équilibre")
    seuil_fixes = f_fixes + mens
    marge_unitaire = adr * (1 - (com_concierge_pct + com_airbnb_pct)/100) - charges_ops_nuit
    occ_seuil = (seuil_fixes / (marge_unitaire * 30.5)) * 100
    st.info(f"Équilibre atteint à **{int(occ_seuil)}%** d'occupation.")
    st.write(f"Soit environ **{int(30.5 * occ_seuil / 100)} nuits** par mois.")

st.markdown("---")

# Tableau d'amortissement
st.subheader(f"📊 Tableau d'Amortissement Dynamique ({type_pret})
