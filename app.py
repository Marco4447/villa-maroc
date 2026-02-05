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

# 2. BARRE LATÉRALE - TOUS LES PARAMÈTRES À GAUCHE
with st.sidebar:
    st.header("⚙️ Configuration")
    
    with st.expander("🏦 1. Financement (Prêt)", expanded=False):
        type_pret = st.radio("Type de prêt", ["In Fine", "Amortissable"])
        m_pret = st.number_input("Capital emprunté (€)", value=470000)
        tx_annuel = st.slider("Taux d'intérêt annuel (%)", 0.0, 10.0, 3.7, step=0.1)
        ans = st.slider("Durée du crédit (ans)", 5, 25, 15)

    with st.expander("📅 2. Revenus & Occupation", expanded=False):
        adr = st.number_input("Prix de la nuitée moyen (€)", value=435)
        occ = st.slider("Taux d'occupation (%)", 0, 100, 45)

    with st.expander("🔒 3. Charges Fixes (Mensuelles)", expanded=True):
        f_fixes_villa = st.number_input("Charges fixes Villa (€)", value=1042, help="Entretien, syndic, jardin")
        f_fixes_detention = st.number_input("Charges Propriétaire (€)", value=125, help="Taxes locales, Assurances")

    with st.expander("💸 4. Charges Variables (%)", expanded=True):
        # SECTION SPÉCIFIQUE DEMANDÉE
        com_concierge_pct = st.slider("Commission Conciergerie (%)", 0, 30, 20)
        com_airbnb_pct = st.slider("Frais Airbnb/Booking (%)", 0, 15, 3)
        autres_vars_pct = st.slider("Autres frais variables (%)", 0, 10, 2)

    with st.expander("⚖️ 5. Régime Fiscal", expanded=True):
        statut = st.selectbox("Structure", ["Personne Physique", "Personne Morale"])

# 3. MOTEUR DE CALCULS FINANCIERS
nb_m = ans * 12
tm = tx_annuel / 100 / 12
tableau = []
capital_restant = m_pret

# --- Calcul du Crédit ---
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

# --- Rentabilité & Fiscalité ---
rev_brut_m = adr * 30.5 * (occ / 100)
total_vars_pct = com_concierge_pct + com_airbnb_pct + autres_vars_pct
montant_vars = rev_brut_m * (total_vars_pct / 100)
total_fixes = f_fixes_villa + f_fixes_detention

if statut == "Personne Physique":
    # Base taxable = 60% du CA Brut (Abattement 40%), Taxe = 15% (Retenue à la source)
    base_t = rev_brut_m * 0.60
    impot_m = base_t * 0.15
else:
    # Personne Morale = IS 20% sur bénéfice net de charges et intérêts
    benef_is = rev_brut_m - montant_vars - total_fixes - mens
    impot_m = max(0, benef_is * 0.20)

profit_net = rev_brut_m - montant_vars - total_fixes - mens - impot_m

# 4. AFFICHAGE ÉCRAN PRINCIPAL
st.title("🏰 Audit de Rentabilité : Villa Marrakech")

# Bandeau de KPIs
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Profit Net / Mois", f"{int(profit_net)} €")
with c2: st.metric("Mensualité Crédit", f"{int(mens)} €")
with c3: st.metric("Impôt Mensuel", f"{int(impot_m)} €")
dscr = (rev_brut_m - montant_vars - total_fixes) / mens if mens > 0 else 0
with c4: st.metric("Ratio de Couverture (DSCR)", f"{dscr:.2f}", help="Indice de solvabilité (>1.20)")

st.markdown("---")

# Détails des Flux
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("📝 Détail des Flux Mensuels")
    st.write(f"• Revenu Brut : **{int(rev_brut_m)} €**")
    st.write(f"• Charges Variables ({total_vars_pct}%) : **-{int(montant_vars)} €**")
    st.write(f"• Charges Fixes Globales : **-{int(total_fixes)} €**")
    st.write(f"• Impôt ({statut}) : **-{int(impot_m)} €**")
    st.divider()
    st.markdown(f"### Cash-Flow Net : **{int(profit_net)} € / mois**")

with col_b:
    st.subheader("🏁 Point d'Équilibre")
    # Calcul du seuil d'occupation
    seuil_fixes = total_fixes + mens
    marge_unitaire = adr * (1 - (total_vars_pct / 100))
    occ_seuil = (seuil_fixes / (marge_unitaire * 30.5)) * 100
    st.info(f"Équilibre à **{int(occ_seuil)}%** d'occupation.")
    st.write(f"Soit environ **{int(30.5 * occ_seuil / 100)} nuits** par mois.")

st.markdown("---")
# Tableau d'amortissement
st.subheader(f"📊 Tableau d'Amortissement Dynamique ({type_pret})")
df_a = pd.DataFrame(tableau, columns=["Mois", "Échéance", "Principal", "Intérêts", "Restant"])
st.dataframe(df_a, use_container_width=True, height=400, hide_index=True)
