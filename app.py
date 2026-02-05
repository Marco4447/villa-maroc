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
    </style>
    """, unsafe_allow_html=True)

st.title("🏰 Audit de Rentabilité & Pricing Dynamique")
st.markdown("---")

# 3. BARRE LATÉRALE (CONFIGURATION)
with st.sidebar:
    st.header("⚙️ Paramètres")
    
    # Mensualité fixe selon votre crédit réel
    mensualite_fixe = 1449 
    st.success(f"🏦 Crédit bloqué à : **{mensualite_fixe} €** / mois")

    with st.expander("📅 Saisonnalité & Revenus", expanded=True):
        mois_choisi = st.select_slider(
            "Mois de l'année",
            options=["Janv", "Févr", "Mars", "Avril", "Mai", "Juin", "Juil", "Août", "Sept", "Oct", "Nov", "Déc"],
            value="Avril"
        )
        
        # Logique de Saisonnalité
        if mois_choisi in ["Déc", "Avril", "Mai", "Oct"]:
            coeff = 1.3  
            saison_txt = "🏷️ Haute Saison (+30%)"
        elif mois_choisi in ["Juil", "Août", "Janv"]:
            coeff = 0.8  
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
        # Frais fixes totaux regroupés (Entretien, Taxes, Jardin, etc.)
        frais_fixes_regroupes = st.number_input("Total Frais Fixes / mois (€)", value=1650)

# 4. CALCULS FINANCIERS
nuits_mois = 30.5 * (to / 100)
ca_mois = nuits_mois * adr_actuel

# Fiscalité Marocaine
def calculer_impot_mensuel(revenu_brut):
    base_taxable = (revenu_brut * 12) * 0.60 # Abattement 40%
    if base_taxable <= 30000:
        impot_an = 0
    elif base_taxable <= 180000:
        impot_an = (base_taxable * 0.34) - 17200
    else:
        impot_an = (base_taxable * 0.38) - 24400
    return impot_an / 12

impot_mois = calculer_impot_mensuel(ca_mois)
commission_montant = ca_mois * com_concierge / 100
total_depenses_mois = commission_montant + frais_fixes_regroupes + mensualite_fixe + impot_mois
profit_mensuel = ca_mois - total_depenses_mois

# 5. AFFICHAGE DES RÉSULTATS
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Revenu Mensuel", f"{int(ca_mois)} €")
with col2:
    st.metric("Profit Net / Mois", f"{int(profit_mensuel)} €")
with col3:
    st.metric("Mensualité Crédit", f"{int(mensualite_fixe)} €")

st.markdown("---")

c1, c2 = st.columns(2)
with c1:
    st.subheader("📊 Détail des charges (mensuel)")
    st.write(f"• Conciergerie ({com_concierge}%) : **{int(commission_montant)} €**")
    st.write(f"• Frais fixes regroupés : **{int(frais_fixes_regroupes)} €**")
    st.write(f"• Impôts Maroc (Estimé) : **{int(impot_mois)} €**")
    st.write(f"• Remboursement crédit : **{int(mensualite_fixe)} €**")

with c2:
    # Calcul simplifié du Seuil de Rentabilité
    occ_seuil = 0
    for test_occ in range(0, 101):
        test_ca = 30.5 * (test_occ / 100) * adr_actuel
        test_imp = calculer_impot_mensuel(test_ca)
        test_ch = (test_ca * com_concierge / 100) + frais_fixes_regroupes + mensualite_fixe + test_imp
        if test_ca >= test_ch:
            occ_seuil = test_occ
            break
    
    st.subheader("🏁 Seuil de Rentabilité")
    st.write(f"À {int(adr_actuel)}€/nuit, l'équilibre est à :")
    st.info(f"**{occ_seuil} % d'occupation**")
    st.write(f"Soit environ **{int(30.5 * occ_seuil / 100)} nuits** par mois.")
