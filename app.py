import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Audit Rentabilité Villa Marrakech", layout="wide")

# 2. DESIGN PERSONNALISÉ (OR ET NOIR)
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
    .stSelectSlider [data-baseweb="slider"] { color: #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏰 Audit de Rentabilité & Pricing Dynamique")
st.markdown("---")

# 3. BARRE LATÉRALE (CONFIGURATION)
with st.sidebar:
    st.header("⚙️ Paramètres")
    
    with st.expander("🏦 Financement", expanded=False):
        type_pret = st.radio("Type de crédit", ["In Fine", "Amortissable"])
        m_pret = st.number_input("Montant emprunté (€)", value=470000)
        tx_annuel = st.number_input("Taux annuel (%)", value=3.70)
        ans = st.slider("Durée du crédit (ans)", 1, 25, 15)

    with st.expander("📅 Saisonnalité & Revenus", expanded=True):
        mois_choisi = st.select_slider(
            "Mois de l'année",
            options=["Janv", "Févr", "Mars", "Avril", "Mai", "Juin", "Juil", "Août", "Sept", "Oct", "Nov", "Déc"],
            value="Avril"
        )
        
        # Logique de Pricing Dynamique
        if mois_choisi in ["Déc", "Avril", "Mai", "Oct"]:
            coeff = 1.3  # Haute saison
            saison_txt = "🏷️ Haute Saison (+30%)"
        elif mois_choisi in ["Juil", "Août", "Janv"]:
            coeff = 0.8  # Basse saison
            saison_txt = "🏷️ Basse Saison (-20%)"
        else:
            coeff = 1.0
            saison_txt = "🏷️ Saison Standard"
            
        adr_base = st.number_input("Prix Nuitée de base (€)", value=430)
        adr_actuel = adr_base * coeff
        st.info(f"{saison_txt} : **{int(adr_actuel)} €** / nuit")
        
        to = st.slider("Taux d'occupation (%)", 0, 100, 41)
        
    with st.expander("💸 Frais Villa (Mensuels)", expanded=True):
        com_concierge = st.slider("Conciergerie (%)", 0, 40, 20)
        energie_mois = st.number_input("Eau & Elec / mois (€)", value=350)
        menage_mois = st.number_input("Ménage / mois (€)", value=1000)
        taxe_fonciere_an = st.number_input("Taxe Foncière / an (€)", value=3000)
        jardin_mois = st.number_input("Jardin & Piscine / mois (€)", value=200)
        fixes_mois = st.number_input("Assurances & Internet / mois (€)", value=100)

# 4. CALCULS FINANCIERS
# Mensualité crédit
if type_pret == "In Fine":
    mensualite = (m_pret * (tx_annuel / 100)) / 12
else:
    tm = tx_annuel / 100 / 12
    nm = ans * 12
    if tm > 0:
        mensualite = m_pret * (tm / (1 - (1 + tm)**-nm))
    else:
        mensualite = m_pret / nm

# Revenus et Charges
nuits_mois = 30.5 * (to / 100)
ca_mois = nuits_mois * adr_actuel
charges_fixes_mois = (taxe_fonciere_an / 12) + energie_mois + menage_mois + jardin_mois + fixes_mois

# Fiscalité Marocaine (Abattement 40% -> Base taxable 60%)
def calculer_impot_mensuel(revenu_brut):
    base_taxable = (revenu_brut * 12) * 0.60
    if base_taxable <= 30000:
        impot_an = 0
    elif base_taxable <= 180000:
        impot_an = (base_taxable * 0.34) - 17200
    else:
        impot_an = (base_taxable * 0.38) - 24400
    return impot_an / 12

impot_mois = calculer_impot_mensuel(ca_mois)
total_depenses_mois = (ca_mois * com_concierge / 100) + charges_fixes_mois + mensualite + impot_mois
profit_mensuel = ca_mois - total_depenses_mois

# 5. CALCUL DU POINT MORT (SEUIL DE RENTABILITÉ)
occ_seuil = 0
for test_occ in range(0, 101):
    test_ca = 30.5 * (test_occ / 100) * adr_actuel
    test_imp = calculer_impot_mensuel(test_ca)
    test_ch = (test_ca * com_concierge / 100) + charges_fixes_mois + mensualite + test_imp
    if test_ca >= test_ch:
        occ_seuil = test_occ
        break

# 6. AFFICHAGE DES RÉSULTATS
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Revenu Mensuel", f"{int(ca_mois)} €")
with col2:
    st.metric("Profit Net / Mois", f"{int(profit_mensuel)} €")
with col3:
    st.metric("Mensualité Crédit", f"{int(mensualite)} €")

st.markdown("---")

c1, c2 = st.columns(2)
with c1:
    st.subheader("📊 Détail des charges (mensuel)")
    st.write(f"• Conciergerie : **{int(ca_mois * com_concierge / 100)} €**")
    st.write(f"• Frais fixes (Entretien/Taxes) : **{int(charges_fixes_mois)} €**")
    st.write(f"• Impôts Maroc (Estimé) : **{int(impot_mois)} €**")
    st.write(f"• Remboursement crédit : **{int(mensualite)} €**")

with c2:
    st.subheader("🏁 Seuil de Rentabilité")
    st.write(f"Pour ce prix ({int(adr_actuel)}€), l'équilibre est à :")
    st.info(f"**{occ_seuil} % d'occupation**")
    st.write(f"Soit environ **{int(30.5 * occ_seuil / 100)} nuits** louées par mois.")
