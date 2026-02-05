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

# 2. BARRE LATÉRALE AVEC SECTIONS RÉTRACTABLES (FLECHES)
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Section Financement
    with st.expander("🏦 Financement", expanded=False):
        type_pret = st.radio("Type de prêt", ["In Fine", "Amortissable"])
        m_pret = st.number_input("Montant emprunté (€)", value=470000)
        tx_annuel = st.slider("Taux d'intérêt (%)", 0.0, 10.0, 3.7, step=0.1)
        ans = st.slider("Durée (ans)", 5, 25, 15)
    
    # Section Revenus
    with st.expander("📅 Revenus & Occupation", expanded=True):
        adr = st.number_input("Prix Nuitée (€)", value=430)
        occ = st.slider("Taux d'occupation (%)", 0, 100, 41)
    
    # Section Charges
    with st.expander("💸 Charges Mensuelles", expanded=False):
        f_fixes = st.number_input("Frais fixes (€)", value=1650)
        com_pct = st.slider("Com. Conciergerie (%)", 0, 40, 20)
        statut = st.selectbox("Régime Fiscal", ["Personne Physique", "Personne Morale"])

# 3. LOGIQUE DES CALCULS
nb_m = ans * 12
tm = tx_annuel / 100 / 12
tableau = []
cr = m_pret
total_int = 0

if type_pret == "Amortissable":
    mens_banque = m_pret * (tm / (1 - (1 + tm)**-nb_m)) if tm > 0 else m_pret / nb_m
    for i in range(1, nb_m + 1):
        int_m = cr * tm
        princ = mens_banque - int_m
        cr -= princ
        total_int += int_m
        tableau.append([i, round(mens_banque, 2), round(princ, 2), round(int_m, 2), round(max(0, cr), 2)])
else:
    mens_banque = m_pret * tm
    total_int = mens_banque * nb_m
    for i in range(1, nb_m + 1):
        princ = 0 if i < nb_m else m_pret
        echeance = mens_banque if i < nb_m else mens_banque + m_pret
        tableau.append([i, round(echeance, 2), round(princ, 2), round(mens_banque, 2), m_pret if i < nb_m else 0])

df_amort = pd.DataFrame(tableau, columns=["Mois", "Échéance", "Principal", "Intérêts", "Restant"])

# Rentabilité
rev_brut_mois = adr * 30.5 * (occ / 100)
f_vars_mois = rev_brut_mois * (com_pct / 100)

def calcul_impot(r, s):
    if s == "Personne Physique":
        base = (r * 12) * 0.60
        if base <= 30000: return 0
        elif base <= 180000: return ((base * 0.34) - 17200) / 12
        else: return ((base * 0.38) - 24400) / 12
    else:
        base = (r * 12) - (f_fixes * 12) - (mens_banque * 12)
        return (max(0, base) * 0.20) / 12

impot_mois = calcul_impot(rev_brut_mois, statut)
cash_flow_net = rev_brut_mois - f_vars_mois - f_fixes - mens_banque - impot_mois

# 4. AFFICHAGE ÉCRAN PRINCIPAL
st.title("🏰 Audit de Rentabilité Financière")

# Metrics de synthèse
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Profit Net / Mois", f"{int(cash_flow_net)} €")
with col2:
    st.metric("Mensualité Banque", f"{int(mens_banque)} €")
with col3:
    st.metric("Total Intérêts Prêt", f"{int(total_int)} €")

st.markdown("---")

# Détails et Seuil
c1, c2 = st.columns(2)
with c1:
    st.subheader("📝 Flux de Trésorerie")
    st.write(f"• Revenu Brut : **{int(rev_brut_mois)} €**")
    st.write(f"• Conciergerie : **-{int(f_vars_mois)} €**")
    st.write(f"• Charges Fixes : **-{int(f_fixes)} €**")
    st.write(f"• Impôt Estimé : **-{int(impot_mois)} €**")

with c2:
    st.subheader("🏁 Seuil de Rentabilité")
    occ_seuil = 0
    for test_occ in range(0, 101):
        t_ca = adr * 30.5 * (test_occ / 100)
        t_imp = calcul_impot(t_ca, statut)
        if t_ca >= (t_ca * com_pct / 100) + f_fixes + mens_banque + t_imp:
            occ_seuil = test_occ
            break
    st.info(f"Équilibre à **{occ_seuil}%** d'occupation ({int(30.5 * occ_seuil / 100)} nuits).")

st.markdown("---")

# Tableau d'amortissement sans l'index 0-179
st.subheader(f"📊 Tableau d'Amortissement ({type_pret})")
st.dataframe(df_amort, use_container_width=True, height=400, hide_index=True)
