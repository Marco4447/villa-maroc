import streamlit as st
import pandas as pd

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Audit Villa Marrakech", layout="wide")

# Style CSS pour l'esthétique du dashboard
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

# 2. BARRE LATÉRALE - PARAMÈTRES RÉGLABLES
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
        com_concierge_pct = st.slider("Commission Conciergerie (%)", 0, 30, 20)
        com_airbnb_pct = st.slider("Frais Airbnb/Booking (%)", 0, 20, 3)
        statut = st.selectbox("Régime Fiscal", ["Personne Physique", "Personne Morale"])

# 3. MOTEUR DE CALCULS FINANCIERS
nb_m = ans * 12
tm = tx_annuel / 100 / 12
tableau = []
capital_restant = m_pret

# --- Calcul de la mensualité et amortissement ---
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
        echeance = mens + p_final
        tableau.append([i, round(echeance, 2), p_final, round(mens, 2), m_pret if i < nb_m else 0])

# --- Analyse de la Rentabilité ---
rev_brut_m = adr * 30.5 * (occ / 100)
frais_gestion = rev_brut_m * ((com_concierge_pct + com_airbnb_pct) / 100)

# Fiscalité selon le régime (Abattement de 40% pour PP selon le rapport)
if statut == "Personne Physique":
    # Base imposable = 60% du CA Brut, Taux retenue = 15%
    impot_m = (rev_brut_m * 0.60) * 0.15
else:
    # Personne Morale : IS 20% sur bénéfice net de charges et intérêts
    benef_avant_is = rev_brut_m - frais_gestion - f_fixes - mens
    impot_m = max(0, benef_avant_is * 0.20)

profit_net = rev_brut_m - frais_gestion - f_fixes - mens - impot_m

# Ratios de pilotage
dscr = (rev_brut_m - frais_gestion - f_fixes) / mens if mens > 0 else 0

# 4. AFFICHAGE ÉCRAN PRINCIPAL
st.title("🏰 Audit de Rentabilité Financière")

# Bandeau de KPIs (Inspiré de votre rapport)
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Profit Net / Mois", f"{int(profit_net)} €")
with c2:
    st.metric("Mensualité Crédit", f"{int(mens)} €")
with c3:
    st.metric("Impôt Mensuel", f"{int(impot_m)} €")
with c4:
    st.metric("Ratio DSCR", f"{dscr:.2f}", help="Indice de solvabilité (>1.20)")

st.markdown("---")

# Détails des Flux
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("📝 Détail des Flux Mensuels")
    st.write(f"• Revenu Brut : **{int(rev_brut_m)} €**")
    st.write(f"• Gestion & Plateformes : **-{
