import streamlit as st
import pandas as pd

# 1. CONFIGURATION
st.set_page_config(page_title="Audit Villa Marrakech - Précision", layout="wide")

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

# 2. BARRE LATÉRALE - CONFIGURATION DÉTAILLÉE
with st.sidebar:
    st.header("⚙️ Paramètres d'Audit")
    
    with st.expander("🏦 Financement (Prêt)", expanded=False):
        type_pret = st.radio("Type de prêt", ["In Fine", "Amortissable"])
        m_pret = st.number_input("Capital emprunté (€)", value=470000) #
        tx_annuel = st.slider("Taux d'intérêt (%)", 0.0, 10.0, 3.7, step=0.1)
        ans = st.slider("Durée (ans)", 5, 25, 15)

    with st.expander("📅 Revenus Locatifs", expanded=True):
        adr = st.number_input("Prix Nuitée (€)", value=430)
        occ = st.slider("Taux d'occupation (%)", 0, 100, 45)

    with st.expander("💸 Structure des Charges", expanded=True):
        f_fixes = st.number_input("Charges Fixes / mois (€)", value=1650)
        # DISSOCIATION ICI :
        com_concierge_pct = st.slider("Com. Conciergerie (%)", 0, 30, 20)
        com_airbnb_pct = st.slider("Frais Airbnb/Booking (%)", 0, 20, 3)
        
        tx_impot_est = st.slider("Impôt estimé sur bénéfice (%)", 0, 40, 20)
        statut = st.selectbox("Régime Fiscal", ["Personne Physique", "Personne Morale"])

# 3. CALCULS FINANCIERS
nb_m = ans * 12
tm = tx_annuel / 100 / 12
tableau = []
cr = m_pret

# Amortissement
if type_pret == "Amortissable":
    mens = m_pret * (tm / (1 - (1 + tm)**-nb_m)) if tm > 0 else m_pret / nb_m
    for i in range(1, nb_m + 1):
        int_m = cr * tm
        princ = mens - int_m
        cr -= princ
        tableau.append([i, round(mens, 2), round(princ, 2), round(int_m, 2), round(max(0, cr), 2)])
else:
    mens = m_pret * tm
    for i in range(1, nb_m + 1):
        p = 0 if i < nb_m else m_pret
        ech = mens if i < nb_m else mens + m_pret
        tableau.append([i, round(ech, 2), round(p, 2), round(mens, 2), m_pret if i < nb_m else 0])

# Rentabilité avec dissociation
rev_brut_m = adr * 30.5 * (occ / 100)
frais_concierge = rev_brut_m * (com_concierge_pct / 100)
frais_airbnb = rev_brut_m * (com_airbnb_pct / 100)
total_vars = frais_concierge + frais_airbnb

# Fiscalité simplifiée
base_taxable = max(0, rev_brut_m - total_vars - f_fixes - mens)
impot_m = base_taxable * (tx_impot_est / 100)
profit_net = rev_brut_m - total_vars - f_fixes - mens - impot_m

# Ratios Experts
dscr = (rev_brut_m - total_vars - f_fixes) / mens if mens > 0 else 0
roi_annuel = ((profit_net * 12) / m_pret) * 100 if m_pret > 0 else 0

# 4. AFFICHAGE ÉCRAN PRINCIPAL
st.title("🏰 Audit de Performance & Ratios de Pilotage")

# Bandeau KPI
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Profit Net Mensuel", f"{int(profit_net)} €")
with c2: st.metric("DSCR (Solvabilité)", f"{dscr:.2f}", help="Doit être > 1.20 pour rassurer la banque")
with c3: st.metric("Rendement Net (ROI)", f"{roi_annuel:.2f} %")
with c4: st.metric("Mensualité Crédit", f"{int(mens)} €")

st.markdown("---")

# Détails des Flux
col_flux1, col_flux2 = st.columns(2)
with col_flux1:
    st.subheader("📝 Détail des Flux (Mensuel)")
    st.write(f"• Revenu Brut : **{int(rev_brut_m)} €**")
    st.write(f"• Frais Conciergerie ({com_concierge_pct}%) : **-{int(frais_concierge)} €**")
    st.write(f"• Frais Airbnb ({com_airbnb_pct}%) : **-{int(frais_airbnb)} €**")
    st.write(f"• Charges Fixes : **-{int(f_fixes)} €**")
    st.write(f"• Impôt estimé ({tx_impot_est}%) : **-{int(impot_m)} €**")
    st.divider()
    st.markdown(f"### Cash-Flow : **{int(profit_net)} € / mois**")

with col_flux2:
    st.subheader("🏁 Seuil de Rentabilité")
    # Calcul dynamique du point mort
    seuil_ca = (f_fixes + mens) / (1 - (com_concierge_pct + com_airbnb_pct + tx_impot_est)/100)
    occ_seuil = (seuil_ca / (adr * 30.5)) * 100
    st.info(f"Équilibre atteint à **{int(occ_seuil)}%** d'occupation.")
    st.write(f"Soit environ **{int(30.5 * occ_seuil / 100)} nuits** par mois.")

st.markdown("---")

# Tableau d'amortissement
st.subheader(f"📊 Tableau d'Amortissement Dynamique ({type_pret})")
df_a = pd.DataFrame(tableau, columns=["Mois", "Échéance", "Principal", "Intérêts", "Restant"])
st.dataframe(df_a, use_container_width=True, height=400, hide_index=True)
