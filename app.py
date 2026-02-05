import streamlit as st

# 1. CONFIGURATION
st.set_page_config(page_title="Simulation de rentabilité", layout="wide")

# 2. DESIGN (Sombre & Or)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'serif'; }
    div[data-testid="stMetric"] { 
        background-color: #161B22; 
        border: 1px solid #D4AF37; 
        padding: 15px; 
        border-radius: 10px; 
        text-align: center;
    }
    div[data-testid="stMetricValue"] > div { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏰 Simulation de rentabilité de votre villa")
st.markdown("---")

# 3. BARRE LATÉRALE
with st.sidebar:
    st.header("⚙️ Configuration")
    
    with st.expander("🏦 Financement (In Fine)", expanded=False):
        m_pret = st.number_input("Montant emprunté (€)", value=470000, step=5000)
        apport = st.number_input("Apport injecté (€)", value=200000, step=5000)
        tx = st.number_input("Taux annuel (%)", value=3.70, step=0.05)
        ans = st.slider("Durée du crédit (ans)", 1, 25, 15)

    with st.expander("📅 Revenus Locatifs", expanded=True):
        adr = st.number_input("Prix Nuitée (€)", value=500, step=10)
        to = st.slider("Occupation (%)", 0, 100, 45, 1)
        
    with st.expander("💸 Frais Villa (Mensuels & Annuels)", expanded=True):
        st.subheader("Charges Variables (Moyennes)")
        com_concierge = st.slider("Conciergerie (%)", 0, 40, 25)
        # Saisie mensuelle demandée
        energie_mois = st.number_input("Eau & Elec / mois moyen (€)", value=450, step=50)
        menage_mois = st.number_input("Ménage & Blanchisserie / mois (€)", value=1000, step=100)
        
        st.subheader("Charges Fixes")
        # Saisie annuelle
        taxe_an = st.number_input("Taxe Habitation & Foncière / an (€)", value=3000, step=100)
        # Saisie mensuelle
        jardin_mois = st.number_input("Entretien Jardin & Piscine / mois (€)", value=200, step=50)
        autres_fixes_mois = st.number_input("Assurances & Internet / mois (€)", value=100, step=10)

# 4. CALCULS (Conversion automatique en annuel)
nuits_an = 365 * (to / 100)
ca_annuel = nuits_an * adr

# Frais convertis en annuel
frais_concierge_an = ca_annuel * (com_concierge / 100)
frais_variables_an = (energie_mois * 12) + (menage_mois * 12)
frais_fixes_an = taxe_an + (jardin_mois * 12) + (autres_fixes_mois * 12)

total_charges_an = frais_concierge_an + frais_variables_an + frais_fixes_an
mensu_int = (m_pret * (tx / 100)) / 12

# Profit net
profit_annuel = ca_annuel - total_charges_an - (mensu_int * 12)
profit_mensuel = profit_annuel / 12

# 5. KPI (Affichage sans virgules)
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("CA Annuel", f"{int(ca_annuel)} €")
with c2:
    st.metric("Profit Net Mensuel", f"{int(profit_mensuel)} €")
with c3:
    renta = (profit_annuel / apport * 100) if apport > 0 else 0
    st.metric("Rendement / Apport", f"{renta:.1f} %")

st.markdown("---")

# 6. RÉCAPITULATIF (Tableau comparatif Mois / An)
st.subheader("📊 Tableau des Charges")
col_table1, col_table2 = st.columns(2)

with col_table1:
    st.write("**Postes de dépenses**")
    st.write("- Conciergerie (variable) :")
    st.write("- Énergie (Eau/Elec) :")
    st.write("- Ménage & Linge :")
    st.write("- Taxes :")
    st.write("- Entretien Jardin/Piscine :")
    st.write("- Assurances & Fixes :")
    st.write("**TOTAL DES CHARGES :**")

with col_table2:
    st.write("**Montant Annuel**")
    st.write(f"{int(frais_concierge_an)} €")
    st.write(f"{int(energie_mois * 12)} €")
    st.write(f"{int(menage_mois * 12)} €")
    st.write(f"{int(taxe_an)} €")
    st.write(f"{int(jardin_mois * 12)} €")
    st.write(f"{int(autres_fixes_mois * 12)} €")
    st.write(f"**{int(total_charges_an)} €**")

st.markdown("---")
st.subheader("🏦 Rappel Crédit In Fine")
st.write(f"Mensualité intérêts : **{int(mensu_int)} €/mois** | Capital dû au terme : **{int(m_pret)} €**")
