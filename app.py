import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Simulation de rentabilité", layout="wide")

# 2. DESIGN PERSONNALISÉ (Sombre & Or)
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

# 3. BARRE LATÉRALE (PARAMÈTRES)
with st.sidebar:
    st.header("⚙️ Configuration")
    
    with st.expander("🏦 Financement", expanded=True):
        type_pret = st.radio("Type de crédit", ["In Fine", "Amortissable"])
        m_pret = st.number_input("Montant emprunté (€)", value=470000, step=5000)
        apport = st.number_input("Apport personnel (€)", value=200000, step=5000)
        tx_annuel = st.number_input("Taux annuel (%)", value=3.70, step=0.05)
        ans = st.slider("Durée du crédit (ans)", 1, 25, 15)

    with st.expander("📅 Revenus Locatifs", expanded=True):
        # Saisie manuelle pour une précision totale
        adr = st.number_input("Prix Nuitée (€)", value=500, step=10)
        to = st.slider("Occupation (%)", 0, 100, 45, 1)
        
    with st.expander("💸 Frais Villa (Par mois)", expanded=True):
        st.subheader("Charges Variables")
        com_concierge = st.slider("Conciergerie (%)", 0, 40, 25)
        energie_mois = st.number_input("Eau & Elec / mois moyen (€)", value=450, step=50)
        menage_mois = st.number_input("Ménage & Blanchisserie / mois (€)", value=1000, step=100)
        
        st.subheader("Charges Fixes")
        taxe_an = st.number_input("Taxe Foncière / an (€)", value=3000, step=100)
        jardin_mois = st.number_input("Jardin & Piscine / mois (€)", value=200, step=50)
        fixes_mois = st.number_input("Assurances & Internet / mois (€)", value=100, step=10)

# 4. LOGIQUE DE CALCUL DU CRÉDIT
if type_pret == "In Fine":
    # Mensualité intérêts seuls
    mensualite_totale = m_pret * (tx_annuel / 100 / 12)
    cout_total_credit = mensualite_totale * 12 * ans
else:
    # Formule standard pour prêt amortissable
    t = tx_annuel / 100 / 12
    n = ans * 12
    if t > 0:
        mensualite_totale = m_pret * (t / (1 - (1 + t)**-n))
    else:
        mensualite_totale = m_pret / n
    cout_total_credit = (mensualite_totale * n) - m_pret

# 5. CALCULS EXPLOITATION
nuits_an = 365 * (to / 100)
ca_an = nuits_an * adr

# Ventilation des frais (Conversion en annuel)
frais_gestion_an = ca_an * (com_concierge / 100)
frais_var_an = (energie_mois * 12) + (menage_mois * 12)
frais_fixes_an = taxe_an + (jardin_mois * 12) + (fixes_mois * 12)
total_charges_an = frais_gestion_an + frais_var_an + frais_fixes_an

# Cash-flow net mensuel
profit_mensuel = (ca_an - total_charges_an - (mensualite_totale * 12)) / 12

# 6. KPI (SANS VIRGULES DÉCIMALES)
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Chiffre d'Affaires Annuel", f"{int(ca_an)} €")
with c2:
    st.metric("Cash-flow Net Mensuel", f"{int(profit_mensuel)} €")
with c3:
    renta = (profit_mensuel * 12 / apport * 100) if apport > 0 else 0
    st.metric("Rendement / Apport", f"{renta:.1f} %")

st.markdown("---")

# 7. RÉCAPITULATIF TECHNIQUE
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("📊 Tableau des Charges")
    st.write(f"• Conciergerie ({com_concierge}%) : **{int(frais_gestion_an)} €/an**")
    st.write(f"• Énergie (Eau/Elec) : **{int(energie_mois * 12)} €/an**")
    st.write(f"• Ménage & Blanchisserie : **{int(menage_mois * 12)} €/an**")
    st.write(f"• Taxes & Entretien Fixe : **{int(frais_fixes_an)} €/an**")
    st.write(f"**TOTAL DES CHARGES : {int(total_charges_an)} €/an**")

with col_b:
    st.subheader(f"🏦 Financement {type_pret}")
    st.write(f"• Mensualité totale : **{int(mensualite_totale)} €/mois**")
    st.write(f"• Coût total du crédit : **{int(cout_total_credit)} €**")
    cap_terme = m_pret if type_pret == "In Fine" else 0
    st.write(f"• Capital dû au terme : **{int(cap_terme)} €**")
