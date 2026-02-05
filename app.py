import streamlit as st

# 1. CONFIGURATION (Doit être la toute première commande)
st.set_page_config(page_title="Audit Rentabilité Villa", layout="wide")

# 2. DESIGN PRO & SUPPRESSION TOTALE STREAMLIT
st.markdown("""
    <style>
    /* Supprimer le header, le footer et le menu hamburger */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    
    /* Supprimer l'espace blanc en haut et en bas */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }

    /* Masquer le bouton 'Deploy' et l'icône de statut de chargement */
    .stAppDeployButton {display: none !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}

    /* Style global sombre et or */
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'serif'; }
    div[data-testid="stMetric"] { 
        background-color: #161B22; border: 1px solid #D4AF37; 
        padding: 15px; border-radius: 10px; text-align: center;
    }
    div[data-testid="stMetricValue"] > div { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏰 Audit de rentabilité de votre Villa")
st.markdown("---")

# 3. BARRE LATÉRALE
with st.sidebar:
    st.header("⚙️ Paramètres")
    with st.expander("🏦 Financement", expanded=True):
        type_pret = st.radio("Type de crédit", ["In Fine", "Amortissable"])
        m_pret = st.number_input("Montant emprunté (€)", value=470000)
        tx_annuel = st.number_input("Taux annuel (%)", value=3.70)
        ans = st.slider("Durée (ans)", 1, 25, 15)
        apport = st.number_input("Apport personnel (€)", value=200000)

    with st.expander("📅 Revenus Locatifs", expanded=True):
        adr = st.number_input("Prix Nuitée (€)", value=430)
        to = st.slider("Occupation (%)", 0, 100, 41)
        
    with st.expander("💸 Frais Villa", expanded=True):
        com_concierge = st.slider("Conciergerie (%)", 0, 40, 20)
        energie_mois = st.number_input("Eau & Elec / mois (€)", value=350)
        menage_mois = st.number_input("Ménage / mois (€)", value=1000)
        taxe_fonciere_an = st.number_input("Taxe Foncière / an (€)", value=3000)
        jardin_mois = st.number_input("Jardin & Piscine / mois (€)", value=200)
        fixes_mois = st.number_input("Assurances & Internet / mois (€)", value=100)

# 4. CALCULS (Logique itérative blindée)
if type_pret == "In Fine":
    mensualite = (m_pret * (tx_annuel / 100)) / 12
else:
    t_m = tx_annuel / 100 / 12
    n_m = ans * 12
    mensualite = m_pret * (t_m / (1 - (1 + t_m)**-n_m)) if t_m > 0 else m_pret / n_m

nuits_an = 365 * (to / 100)
ca_an = nuits_an * adr
charges_fixes_an = taxe_fonciere_an + (energie_mois + menage_mois + jardin_mois + fixes_mois) * 12

def calculer_impot(revenu_brut):
    base = revenu_brut * 0.60
    if base <= 3000: return 0
    elif base <= 18000: return (base * 0.34) - 1720
    else: return (base * 0.38) - 2440

impot_actuel = calculer_impot(ca_an)
total_charges_an = (ca_an * com_concierge / 100) + charges_fixes_an + (mensualite * 12) + impot_actuel
profit_mensuel = (ca_an - total_charges_an) / 12

# Calcul itératif du seuil de rentabilité réel
occ_seuil = 0
for test_occ in range(0, 101):
    test_ca = 365 * (test_occ / 100) * adr
    test_impot = calculer_impot(test_ca)
    test_charges = (test_ca * com_concierge / 100) + charges_fixes_an + (mensualite * 12) + test_impot
    if test_ca >= test_charges:
        occ_seuil = test_occ
        break

# 5. AFFICHAGE DES RÉSULTATS
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("CA Annuel Estimé", str(int(ca_an)) + " €")
with c2:
    st.metric("Profit Net Mensuel", str(int(profit_mensuel)) + " €")
with c3:
    renta_apport = (profit_mensuel * 12 / apport * 100) if apport > 0 else 0
    st.metric("Rentabilité / Apport", str(round(renta_apport, 1)) + " %")

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.subheader("📊 Performance Détaillée")
    st.write("• Impôts Maroc :", int(impot_actuel), "€/an")
    st.write("• Taux d'impôt effectif :", round((impot
