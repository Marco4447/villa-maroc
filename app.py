import streamlit as st
import pandas as pd

# 1. CONFIGURATION ET DESIGN
st.set_page_config(page_title="Audit Rentabilité Villa Marrakech", layout="wide")

st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'serif'; }
    div[data-testid="stMetric"] { 
        background-color: #161B22; border: 1px solid #D4AF37; 
        padding: 15px; border-radius: 10px; text-align: center;
    }
    div[data-testid="stMetricValue"] > div { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏰 Audit de Rentabilité & Amortissement")
st.markdown("---")

# 2. BARRE LATÉRALE - PARAMÈTRES
with st.sidebar:
    st.header("⚙️ Configuration")
    
    with st.expander("🏦 Financement & Crédit", expanded=True):
        type_pret = st.radio("Type de prêt", ["Amortissable", "In Fine"])
        m_pret = st.number_input("Montant de l'emprunt (€)", value=470000)
        tx_annuel = st.slider("Taux d'intérêt annuel (%)", 0.0, 10.0, 3.7, step=0.1)
        ans = st.slider("Durée du crédit (années)", 5, 25, 15)

    with st.expander("📅 Revenus & Location", expanded=True):
        adr_base = st.number_input("Prix de la nuitée (€)", value=430)
        to_pourcent = st.slider("Taux d'occupation (%)", 0, 100, 41)
        
    with st.expander("💸 Charges & Frais", expanded=True):
        frais_fixes_mois = st.number_input("Charges fixes / mois (€)", value=1650)
        frais_variables_pct = st.slider("Charges variables (Conciergerie) %", 0, 40, 20)

    with st.expander("⚖️ Régime Fiscal Maroc", expanded=True):
        regime = st.selectbox("Statut Juridique", ["Personne Physique (Foncier)", "Personne Morale (IS)"])

# 3. CALCUL DU TABLEAU D'AMORTISSEMENT
tm = tx_annuel / 100 / 12
nb_echeances = ans * 12
data_amortissement = []
cap_restant = m_pret

if type_pret == "Amortissable":
    mensualite = m_pret * (tm / (1 - (1 + tm)**-nb_echeances)) if tm > 0 else m_pret / nb_echeances
    for i in range(1, nb_echeances + 1):
        interets = cap_restant * tm
        principal = mensualite - interets
        cap_restant -= principal
        data_amortissement.append([i, mensualite, principal, interets, max(0, cap_restant)])
else:
    mensualite = (m_pret * (tx_annuel / 100)) / 12
    for i in range(1, nb_echeances + 1):
        interets = mensualite
        principal = 0 if i < nb_echeances else m_pret
        data_amortissement.append([i, mensualite if i < nb_echeances else mensualite + m_pret, principal, interets, 0 if i == nb_echeances else m_pret])

df_amort = pd.DataFrame(data_amortissement, columns=["Mois", "Échéance", "Capital", "Intérêts", "Restant"])

# 4. CALCULS DE RENTABILITÉ
ca_mensuel = adr_base * 30.5 * (to_pourcent / 100)
charges_var = ca_mensuel * (frais_variables_pct / 100)

def calculer_impot(rev_brut, statut):
    if statut == "Personne Physique (Foncier)":
        base = (rev_brut * 12) * 0.60  # Abattement 40%
        if base <= 30000: imp = 0
        elif base <= 180000: imp = (base * 0.34) - 17200
        else: imp = (base
