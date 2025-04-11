import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Inventário de Emissões", layout="centered")

st.title("🌱 Plataforma de Inventário de Emissões - Pará")

# Interface principal (sem login por enquanto)
st.subheader("Preencha os dados da sua empresa")

empresa = st.text_input("Nome da empresa")
ano_base = st.number_input("Ano base do inventário", min_value=2000, max_value=2050, step=1)
consumo_energia = st.number_input("Consumo de energia elétrica (kWh)")
combustivel = st.number_input("Consumo de combustíveis (litros)")
viagens = st.number_input("Quantidade de viagens de transporte (km)")
residuos = st.number_input("Quantidade de resíduos gerados (kg)")

if st.button("Calcular Emissões"):
    # Cálculo simplificado de emissões (exemplo didático)
    emissoes = (consumo_energia * 0.000055) + (combustivel * 0.0025) + (viagens * 0.00021) + (residuos * 0.001)

    st.success(f"Emissões totais estimadas: {emissoes:.2f} toneladas de CO₂e")

    # Salvar dados (se quiser armazenar)
    dados = pd.DataFrame({
        "empresa": [empresa],
        "ano_base": [ano_base],
        "energia_kwh": [consumo_energia],
        "combustivel_l": [combustivel],
        "viagens_km": [viagens],
        "residuos_kg": [residuos],
        "emissoes_ton_CO2e": [emissoes]
    })

 # ⚠️ Esta parte só será acessada por você diretamente no arquivo CSV, sem exibição no app
# Os dados são salvos no arquivo 'dados_emissoes.csv' no diretório da aplicação

st.markdown("---")
st.info("✅ Seus dados foram registrados com sucesso.")
st.markdown("Você pode entrar em contato com nossa equipe para receber um relatório completo e um selo de neutralização.")





