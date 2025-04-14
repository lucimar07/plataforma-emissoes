import streamlit as st
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Inventário de Emissões", layout="centered")

st.title("🌱 Plataforma de Inventário de Emissões - Pará")

# Interface principal (sem login por enquanto)
st.subheader("Preencha os dados da sua empresa")
empresa = st.text_input("Nome da empresa")
cnpj = st.text_input("CNPJ")
cidade = st.text_input("Cidade e Estado")
ano_base = st.number_input("Ano base do inventário", min_value=2000, max_value=2050, step=1)
consumo_energia = st.number_input("Consumo de energia elétrica (kWh)")
combustivel = st.number_input("Consumo de combustíveis (litros)")
viagens = st.number_input("Quantidade de viagens de transporte (km)")
residuos = st.number_input("Quantidade de resíduos gerados (kg)")

# Função para enviar dados ao Google Sheets
def send_to_google_sheets(data):
    # Configurações da API
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("path/to/credentials.json", scope)  # Atualize o caminho para o seu arquivo JSON
    client = gspread.authorize(creds)

    # Abra a planilha (substitua pelo nome da sua planilha)
    sheet = client.open("nome_da_sua_planilha").sheet1  # Troque pelo nome da sua planilha

    # Adiciona dados à planilha
    sheet.append_row(data)

if st.button("Calcular Emissões"):
    # Cálculo simplificado de emissões (exemplo didático)
    emissoes = (consumo_energia * 0.000055) + (combustivel * 0.0025) + (viagens * 0.00021) + (residuos * 0.001)
    st.success(f"Emissões totais estimadas: {emissoes:.2f} toneladas de CO₂e")
    
    # Armazenar dados
    dados = pd.DataFrame({
        "empresa": [empresa],
        "ano_base": [ano_base],
        "energia_kwh": [consumo_energia],
        "combustivel_l": [combustivel],
        "viagens_km": [viagens],
        "residuos_kg": [residuos],
        "emissoes_ton_CO2e": [emissoes]
    })

    # ⚠️ Salvar dados em 'dados_emissoes.csv' (opcional)
    dados.to_csv("dados_emissoes.csv", mode='a', header=not os.path.exists("dados_emissoes.csv"), index=False)

    # Enviar dados para Google Sheets
    send_to_google_sheets([empresa, ano_base, consumo_energia, combustivel, viagens, residuos, emissoes])

    st.markdown("---")
    st.markdown("Você pode entrar em contato com nossa equipe para receber um relatório completo e um selo de neutralização.")
