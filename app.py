import streamlit as st

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

st.title("🏰 Audit de Rentabilité Premium - Marrakech")
st.markdown("---")

# 2. BARRE LATÉRALE - PARAMÈTRES RÉGLABLES
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # FINANCEMENT
    with st.expander("🏦 Financement & Crédit", expanded=True):
        type_pret = st.radio("Type de crédit", ["Amortissable", "In Fine"])
        m_pret = st.number_input("Montant de l'emprunt (€)", value=470000)
        tx_annuel = st.slider("Taux d'intérêt annuel (%)", 0.0, 10.0, 3.7, step=0.1)
        ans = st.slider("Durée du crédit (années)", 5, 25, 15)

    # REVENUS LOCATIFS
    with st.expander("📅 Revenus & Location", expanded=True):
        adr_base = st.number_input("Prix de la nuitée (€)", value=430)
        to_pourcent = st.slider("Taux d'occupation (%)", 0, 100, 41)
        
    # CHARGES (SYSTÈME DE CURSEURS)
    with st.expander("💸 Charges & Frais", expanded=True):
        frais_fixes_mois = st.number_input("Charges fixes (Entretien/Web/Assur) / mois (€)", value=1650)
        frais_variables_pct = st.slider("Charges variables (Conciergerie/Services) %", 0, 40, 20)

    # FISCALITÉ (BASÉ SUR VOS RAPPORTS)
    with st.expander("⚖️ Régime Fiscal Maroc", expanded=True):
        regime = st.selectbox("Statut Juridique", ["Personne Physique (Revenus Fonciers)", "Personne Morale (IS)"])

# 3. LOGIQUE DES CALCULS FINANCIERS
# Calcul de la mensualité
if type_pret == "In Fine":
    mensualite = (m_pret * (tx_annuel / 100)) / 12
else:
    tm = tx_annuel / 100 / 12
    nm = ans * 12
    if tm > 0:
        mensualite = m_pret * (tm / (1 - (1 + tm)**-nm))
    else:
        mensualite = m_pret / nm

# Revenus mensuels
ca_mensuel = adr_base * 30.5 * (to_pourcent / 100)

# Charges variables
charges_variables_montant = ca_mensuel * (frais_variables_pct / 100)

# Fiscalité Marocaine
def calculer_fiscalite(revenu_brut, statut):
    if statut == "Personne Physique (Revenus Fonciers)":
        # Abattement de 40% sur le revenu brut foncier
        base_imposable = (revenu_brut * 12) * 0.60
        if base_imposable <= 30000:
            impot_an = 0
        elif base_imposable <= 180000:
            impot_an = (base_imposable * 0.34) - 17200
        else:
            impot_an = (base_imposable * 0.38) - 24400
    else:
        # Simplification Personne Morale (Taux IS progressif)
        base_imposable = (revenu_brut * 12) - (frais_fixes_mois * 12) - (mensualite * 12)
        if base_imposable <= 300000:
            impot_an = base_imposable * 0.10
        else:
            impot_an = base_imposable * 0.20
    return max(0, impot_an / 12)

impot_mensuel = calculer_fiscalite(ca_mensuel, regime)
profit_net_mensuel = ca_mensuel - charges_variables_montant - frais_fixes_mois - mensualite - impot_mensuel

# 4. AFFICHAGE DANS L'ÉCRAN PRINCIPAL
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Revenu Mensuel Brut", f"{int(ca_mensuel)} €")
with col2:
    st.metric("Profit Net / Mois", f"{int(profit_net_mensuel)} €")
with col3:
    st.metric("Mensualité Crédit", f"{int(mensualite)} €")

st.markdown("---")

c1, c2 = st.columns(2)
with c1:
    st.subheader("📊 Répartition des Charges")
    st.write(f"• Mensualité ({type_pret}) : **{int(mensualite)} €**")
    st.write(f"• Charges Variables ({frais_variables_pct}%) : **{int(charges_variables_montant)} €**")
    st.write(f"• Charges Fixes : **{int(frais_fixes_mois)} €**")
    st.write(f"• Impôt ({regime}) : **{int(impot_mensuel)} €**")

with c2:
    # Calcul du Point Mort (Seuil de Rentabilité)
    occ_seuil = 0
    for test_occ in range(0, 101):
        test_ca = adr_base * 30.5 * (test_occ / 100)
        test_imp = calculer_fiscalite(test_ca, regime)
        test_total_ch = (test_ca * frais_variables_pct / 100) + frais_fixes_mois + mensualite + test_imp
        if test_ca >= test_total_ch:
            occ_seuil = test_occ
            break
            
    st.subheader("🏁 Seuil de Rentabilité")
    st.write(f"Pour couvrir toutes vos charges à **{adr_base} €/nuit** :")
    st.info(f"**{occ_seuil} % d'occupation minimum**")
    st.write(f"Soit environ **{int(30.5 * occ_seuil / 100)} nuits** louées par mois.")
