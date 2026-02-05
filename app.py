import streamlit as st
import pandas as pd

# 1. CONFIGURATION
st.set_page_config(page_title="Audit Villa Marrakech", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    h1, h3 { color: #D4AF37 !important; }
    div[data-testid="stMetric"] { background-color: #161B22; border: 1px solid #D4AF37; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRE LATÉRALE
with st.sidebar:
    st.header("⚙️ Configuration")
    type_pret = st.radio("Type de prêt", ["In Fine", "Amortissable"])
    m_pret = st.number_input("Montant emprunté (€)", value=470000)
    tx_annuel = st.slider("Taux d'intérêt (%)", 0.0, 10.0, 3.7, step=0.1)
    ans = st.slider("Durée (ans)", 5, 25, 15)
    
    st.markdown("---")
    adr = st.number_input("Prix Nuitée (€)", value=430)
    occ = st.slider("Taux d'occupation (%)", 0, 100, 41)
    
    st.markdown("---")
    f_fixes = st.number_input("Charges Fixes Mensuelles (€)", value=1650)
    com_pct = st.slider("Com. Conciergerie (%)", 0, 40, 20)
    statut = st.selectbox("Régime Fiscal", ["Personne Physique", "Personne Morale"])

# 3. LOGIQUE DU TABLEAU D'AMORTISSEMENT
nb_m = ans * 12
tm = tx_annuel / 100 / 12
tableau = []
cr = m_pret
total_int = 0

if type_pret == "Amortissable":
    mens = m_pret * (tm / (1 - (1 + tm)**-nb_m)) if tm > 0 else m_pret / nb_m
    for i in range(1, nb_m + 1):
        int_m = cr * tm
        princ = mens - int_m
        cr -= princ
        total_int += int_m
        tableau.append([i, round(mens, 2), round(princ, 2), round(int_m, 2), round(max(0, cr), 2)])
else:
    mens_int = m_pret * tm
    total_int = mens_int * nb_m
    for i in range(1, nb_m + 1):
        princ = 0 if i < nb_m else m_pret
        echeance = mens_int if i < nb_m else mens_int + m_pret
        tableau.append([i, round(echeance, 2), round(princ, 2), round(mens_int, 2), m_pret if i < nb_m else 0])

df_amort = pd.DataFrame(tableau, columns=["Mois", "Échéance", "Principal", "Intérêts", "Restant"])

# 4. CALCUL RENTABILITÉ
rev_brut = adr * 30.5 * (occ / 100)
f_vars = rev_brut * (com_pct / 100)
mens_banque = m_pret * tm if type_pret == "In Fine" else (m_pret * (tm / (1 - (1 + tm)**-nb_m)) if tm > 0 else m_pret / nb_m)

def calcul_impot(r, s):
    if s == "Personne Physique":
        base = (r * 12) * 0.60
        if base <= 30000: return 0
        elif base <= 180000: return ((base * 0.34) - 17200) / 12
        else: return ((base * 0.38) - 24400) / 12
    else:
        base = (r * 12) - (f_fixes * 12) - (mens_banque * 12)
        return (max(0, base) * 0.20) / 12

impot = calcul_impot(rev_brut, statut)
profit = rev_brut - f_vars - f_fixes - mens_banque - impot

# 5. AFFICHAGE
st.title("🏰 Audit de Rentabilité Financière")

col1, col2, col3 = st.columns(3)
col1.metric("Profit Net Mensuel", f"{int(profit)} €")
col2.metric("Mensualité Banque", f"{int(mens_banque)} €")
col3.metric("Total Intérêts Prêt", f"{int(total_int)} €")

st.markdown("---")
st.subheader(f"📊 Tableau d'Amortissement ({type_pret})")

# COMMANDE FIXÉE : hide_index=True ET PARENTHÈSE FERMÉE
st.dataframe(df_amort, use_container_width=True, height=400, hide_index=True)

if type_pret == "In Fine":
    st.info(f"Note : Le crédit In Fine de {m_pret} € à {tx_annuel} % génère un total d'intérêts de {int(total_int)} € sur {ans} ans.")
