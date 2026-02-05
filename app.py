import streamlit as st

# 1. CONFIGURATION
st.set_page_config(page_title="Simulation de rentabilité", layout="wide")

# 2. DESIGN (Sombre & Or)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    h1, h2, h3 { color: #D4AF37 !important; }
    div[data-testid="stMetric"] { 
        background-color: #161B22; 
        border: 1px solid #D4AF37; 
        padding: 15px; 
        border-radius: 10px; 
    }
    div[data-testid="stMetricValue"] > div { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. TITRE
st.title("🏰 Simulation de rentabilité de votre villa")
st.markdown("---")

# 4. BARRE LATÉRALE (TOUS LES PARAMÈTRES SONT ICI)
with st.sidebar:
    st.header("⚙️ Configuration du Projet")
    prix_villa = st.number_input("Prix de vente de la Villa (€)", value=670000, step=10000)
    
    st.markdown("---")
    st.subheader("🏦 Paramètres du Prêt (In Fine)")
    # Ici, tout est modifiable séparément
    montant_credit = st.number_input("Montant de l'emprunt (€)", value=470000, step=5000)
    apport_perso = st.number_input("Apport personnel injecté (€)", value=200000, step=5000)
    taux_annuel = st.number_input("Taux d'intérêt annuel (%)", value=3.70, step=0.05)
    duree_pret = st.slider("Durée du crédit (années)", 1, 25, 15)
    
    st.markdown("---")
    st.subheader("📅 Hypothèses Locatives")
    adr = st.slider("Prix moyen de la nuitée (€)", 300, 1500, 500, 25)
    to = st.slider("Taux d'occupation annuel (%)", 0, 100, 45, 1)

# 5. LOGIQUE DE CALCUL
# Intérêts In Fine : on ne paye que les intérêts sur le montant emprunté
interets_annuels = montant_credit * (taux_annuel / 100)
mensualite_interets = interets_annuels / 12
cout_total_credit = interets_annuels * duree_pret

# Revenus et Charges (basés sur votre rapport)
ca_annuel = 365 * (to / 100) * adr
# Charges : 25% commissions + 35€ ménage/nuit + 14000€ frais fixes
charges_annuelles = (ca_annuel * 0.25) + (365 * (to / 100) * 35) + 14000
profit_annuel_net = ca_annuel - charges_annuelles - interets_annuels
profit_mensuel_net = profit_annuel_net / 12

# 6. AFFICHAGE DES RÉSULTATS
c1, c2, c3 = st.columns(3)
c1.metric("CA Annuel Estimé", f"{int(ca_annuel):,} €".replace(",", " "))
c2.metric("Profit Net Mensuel", f"{int(profit_mensuel_net):,} €".replace(",", " "))
# Renta calculée sur l'apport réellement décaissé
renta_apport = (profit_annuel_net / apport_perso * 100) if apport_perso > 0 else 0
c3.metric("Rendement / Apport", f"{renta_apport:.1f} %")

st.markdown("---")

# 7. RÉCAPITULATIF BANCAIRE ET PATRIMONIAL
col_a, col_b = st.columns(2)

with col_a:
    st.write("### 🏦 Détails du Financement")
    st.write(f"Montant emprunté : **{montant_credit:,} €**".replace(",", " "))
    st.write(f"Taux retenu : **{taux_annuel} %**")
    st.write(f"Mensualité (Intérêts seuls) : **{int(mensualite_interets):,} € / mois**".replace(",", " "))
    st.write(f"Coût total du crédit sur {duree_pret} ans : **{int(cout_total_credit):,} €**".replace(",", " "))

with col_b:
    st.write("### 🛡️ Sécurité & Transmission")
    #
