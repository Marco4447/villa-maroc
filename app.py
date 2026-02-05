import streamlit as st
import pandas as pd

# 1. CONFIGURATION
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

# 2. BARRE LATÉRALE (SIDEBAR)
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

# 3. CALCULS FINANCIERS
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

# Revenus et Charges
rev_brut_mois = adr * 30.5 * (occ / 100)
rev_brut_an = rev_brut_mois * 12
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
rendement_brut = (rev_brut_an / (m_pret * 1.2)) * 100 # Estimation avec frais d'acquisition

# 4. AFFICHAGE ÉCRAN PRINCIPAL
st.title("🏰 Tableau de Bord d'Investissement - Marrakech")

# --- LIGNE 1 : METRICS CLÉS ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Profit Net Mensuel", f"{int(cash_flow_net)} €")
with col2:
    st.metric("Revenu Brut Annuel", f"{int(rev_brut_an)} €")
with col3:
    st.metric("Total Intérêts", f"{int(total_int)} €")
with col4:
    st.metric("Rendement Brut", f"{rendement_brut:.1f} %")

st.markdown("---")

# --- LIGNE 2 : DÉTAILS ET SEUIL ---
c1, c2 = st.columns(2)
with c1:
    st.subheader("📝 Analyse des Flux Mensuels")
    st.write(f"• Revenu Locatif Brut : **{int(rev_brut_mois)} €**")
    st.write(f"• Conciergerie ({com_pct}%) : **-{int(f_vars_mois)} €**")
    st.write(f"• Charges Fixes : **-{int(f_fixes)} €**")
    st.write(f"• Échéance Banque : **-{int(mens_banque)} €**")
    st.write(f"• Impôt Estimé ({statut}) : **-{int(impot_mois)} €**")
    st.divider()
    color = "green" if cash_flow_net > 0 else "red"
    st.markdown(f"### Cash-Flow Net : :{color}[{int(cash_flow_net)} € / mois]")

with c2:
    st.subheader("🏁 Seuil de Rentabilité")
    occ_seuil = 0
    for test_occ in range(0, 101):
        t_ca = adr * 30.5 * (test_occ / 100)
        t_imp = calcul_impot(t_ca, statut)
        t_charges = (t_ca * com_pct / 100) + f_fixes + mens_banque + t_imp
        if t_ca >= t_charges:
            occ_seuil = test_occ
            break
    st.info(f"Pour couvrir vos frais, vous devez louer au moins **{occ_seuil}%** du temps.")
    st.write(f"Soit environ **{int(30.5 * occ_seuil / 100)} nuits** par mois à {adr} €.")

st.markdown("---")

# --- LIGNE 3 : TABLEAU D'AMORTISSEMENT ---
st.subheader(f"📊 Tableau d'Amortissement Technique ({type_pret})")
st.dataframe(df_amort, use_container_width=True, height=400, hide_index=True)
