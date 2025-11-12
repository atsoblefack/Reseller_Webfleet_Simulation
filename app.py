
import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF

st.set_page_config(page_title='Projection Webfleet Cameroun', layout='wide')
st.title('Dashboard avancé Webfleet Cameroun')

# Chargement des données
xls = pd.ExcelFile('App_Webfleet_Projection_FCFA.xlsx')
df_proj = pd.read_excel(xls, 'Projection trimestrielle')

# Paramètres interactifs
st.sidebar.header('Paramètres de simulation')
prix_boîtier = st.sidebar.number_input('Prix de vente boîtier (FCFA)', value=3430*33)
prix_abonnement = st.sidebar.number_input('Prix abonnement client (FCFA/mois)', value=343*33)
taux_change = st.sidebar.number_input('Taux de change ZAR→FCFA', value=33.0)
croissance = st.sidebar.slider('Croissance trimestrielle (%)', 10, 30, 20)

# Recalcul dynamique
df_proj['CA Total recalculé (FCFA)'] = df_proj['CA Total (ZAR)'] * taux_change

# KPIs
st.subheader('Synthèse & KPIs')
ca_total = df_proj['CA Total recalculé (FCFA)'].sum()
resultat_net = (df_proj['Résultat net (ZAR)'] * taux_change).sum()
roi = resultat_net / (143000 * taux_change)
st.metric('CA total (FCFA)', f"{ca_total:,.0f}")
st.metric('Résultat net (FCFA)', f"{resultat_net:,.0f}")
st.metric('ROI cumulé', f"{roi:.2f}")

# Graphiques interactifs
st.subheader('Graphiques')
fig1 = px.line(df_proj, x='Trimestre', y='Cumul véhicules', title='Croissance du parc')
fig2 = px.bar(df_proj, x='Trimestre', y='CA Total recalculé (FCFA)', title='CA trimestriel (FCFA)')
fig3 = px.line(df_proj, x='Trimestre', y='Résultat net (FCFA)', title='Résultat net (FCFA)')
fig4 = px.line(df_proj, x='Trimestre', y='Cumul Cash (FCFA)', title='Cashflow cumulé (FCFA)')

st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
st.plotly_chart(fig3, use_container_width=True)
st.plotly_chart(fig4, use_container_width=True)

# Export PDF
if st.button('Exporter en PDF'):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Rapport de Simulation Webfleet Cameroun')
    pdf.ln(20)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'CA total (FCFA): {ca_total:,.0f}', ln=True)
    pdf.cell(0, 10, f'Resultat net (FCFA): {resultat_net:,.0f}', ln=True)
    pdf.cell(0, 10, f'ROI cumulé: {roi:.2f}', ln=True)
    pdf.output('rapport_webfleet.pdf')
    with open('rapport_webfleet.pdf', 'rb') as file:
        st.download_button('Télécharger le PDF', file, file_name='rapport_webfleet.pdf')


# --- Simulation multi-investisseurs ---
st.subheader('Simulation multi-investisseurs')
n_investisseurs = st.number_input('Nombre d'investisseurs', min_value=1, max_value=10, value=1)
investissements = []
for i in range(n_investisseurs):
    montant = st.number_input(f'Montant investi par investisseur {i+1} (FCFA)', min_value=0, value=1000000)
    investissements.append(montant)

if st.button('Calculer parts'):
    valorisation_post_money = ca_total  # Utilisation du CA total comme base de valorisation
    st.write(f'Valorisation post-money estimée : {valorisation_post_money:,.0f} FCFA')
    data_parts = []
    for i, montant in enumerate(investissements):
        part = (montant / valorisation_post_money) * 100
        data_parts.append({'Investisseur': f'Investisseur {i+1}', 'Montant (FCFA)': montant, 'Part (%)': round(part, 2)})
    st.table(data_parts)
