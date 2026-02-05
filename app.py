import streamlit as st
import pandas as pd

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Audit Rentabilité Villa", layout="wide")

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

# 2. BARRE LATÉRALE - RÉGLAGES PAR SECTIONS
with st.sidebar:
    st.header("⚙️ Paramètres")
    
    with st.expander("🏦 Financement", expanded=False):
        type_pret = st.radio("Type de prêt", ["In Fine", "Amortissable"])
        m_pret = st.number_input("Capital emprunté (€)", value=470000)
        tx_annuel = st.slider("Taux (%)", 0.0, 10.0, 3.7, step=0.1)
        ans = st.slider("Durée (ans)", 5, 25, 15)

    with st.expander("📅 Revenus & Occupation", expanded=True):
        adr = st.number_input("Prix Nuitée (€)", value=430)
        occ = st.slider("Taux d'occupation (%)", 0, 100, 41)

    with st.expander("💸 Structure des Charges", expanded=True):
        f_fixes = st.number_input("Charges Fixes / mois (€)", value=1650)
        # On regroupe tout ici : Conciergerie + Plateforme + Energie variable
        c_vars_pct = st.slider("Total Charges Variables (% du CA)", 10, 50, 30)
        statut = st.selectbox("Régime Fiscal", ["Personne Physique", "Personne Morale"])

# 3. CALCULS FINANCIERS
nb_m = ans * 12
tm = tx_annuel / 100 / 12
tableau = []
cr = m_pret
total_int = 0

# Mensualité et Amortissement
if type_pret == "Amortissable":
    mens = m_pret * (tm / (1 - (1 + tm)**-nb_m)) if tm > 0 else m_pret / nb_m
    for i in range(1, nb_m + 1):
        int_m = cr * tm
        princ = mens - int_m
        cr -= princ
        total_int += int_m
        tableau.append([i, round(mens, 2), round(princ, 2), round(int_m, 2), round(max(0, cr), 2)])
else:
    mens = m_pret * tm
    total_int = mens * nb_m
    for i in range(1, nb_m + 1):
        princ = 0 if i < nb_m else m_pret
        ech = mens if i < nb_m else mens + m_pret
        tableau.append([i, round(ech, 2), round(princ, 2), round(mens, 2), m_pret if i < nb_m else 0])

# Rentabilité
rev_brut_mois = adr * 30.5 * (occ / 100)
montant_c_vars = rev_brut_mois * (c_vars_pct / 100)

def get_impot(r, s):
    if s == "Personne Physique":
        base = (r * 12) * 0.60
        if base <= 30000: return 0
        elif base <= 180000: return ((base * 0.34) - 17200) / 12
        else: return ((base * 0.38) - 24400) / 12
    else:
        base = (r * 12) - (f_fixes * 12) - (mens * 12)
        return (max(0, base) * 0.20) / 12

impot_m = get_impot(rev_brut_mois, statut)
profit_m = rev_brut_mois - montant_c_vars - f_fixes - mens - impot_m

# 4. AFFICHAGE ÉCRAN PRINCIPAL
st.title("🏰 Audit de Rentabilité Financière")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Profit Net / Mois", f"{int(profit_m)} €")
with col2:
    st.metric("Mensualité Crédit", f"{int(mens)} €")
with col3:
    st.metric("Intérêts Totaux", f"{int(total_int)} €")

st.markdown("---")

c1, c2 = st.columns(2)
with c1:
    st.subheader("📊 Flux de Trésorerie")
    st.write(f"• Revenu Brut : **{int(rev_brut_mois)} €**")
    st.write(f"• Charges Variables ({c_vars_pct}%) : **-{int(montant_c_vars)} €**")
    st.write(f"• Charges Fixes : **-{int(f_fixes)} €**")
    st.write(f"• Impôt Estimé : **-{int(impot_m)} €**")

with c2:
    st.subheader("🏁 Point d'Équilibre")
    # Recherche du seuil
    occ_seuil = 0
    for t_occ in range(0, 101):
        t_rev = adr * 30.5 * (t_occ / 100)
        t_imp = get_impot(t_rev, statut)
        if t_rev >= (t_rev * c_vars_pct / 100) + f_fixes + mens + t_imp:
            occ_seuil = t_occ
            break
    st.info(f"Équilibre à **{occ_seuil}%** d'occupation.")
    st.write(f"Soit **{int(30.5 * occ_seuil / 100)} nuits** / mois à {adr} €.")

st.markdown("---")
st.subheader("📅 Tableau d'Amortissement")
df_a = pd.DataFrame(tableau, columns=["Mois", "Échéance", "Principal", "Intérêts", "Restant"])
st.dataframe(df_a, use_container_width=True, height=400, hide_index=True)
