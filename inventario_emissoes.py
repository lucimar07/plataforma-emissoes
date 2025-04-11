import streamlit as st
import pandas as pd
import os

# Caminho do arquivo de usuários
USUARIOS_FILE = "usuarios.csv"

# Função para carregar usuários cadastrados
def carregar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        return pd.read_csv(USUARIOS_FILE)
    return pd.DataFrame(columns=["cnpj", "nome", "senha"])

# Função para salvar novo usuário
def salvar_usuario(cnpj, nome, senha):
    usuarios = carregar_usuarios()
    if cnpj in usuarios["cnpj"].values:
        return False  # já existe
    novo = pd.DataFrame([[cnpj, nome, senha]], columns=["cnpj", "nome", "senha"])
    usuarios = pd.concat([usuarios, novo], ignore_index=True)
    usuarios.to_csv(USUARIOS_FILE, index=False)
    return True

# Verificação de login
def autenticar_usuario(cnpj, senha):
    usuarios = carregar_usuarios()
    user = usuarios[(usuarios["cnpj"] == cnpj) & (usuarios["senha"] == senha)]
    return not user.empty

# --- Interface da aplicação ---

st.set_page_config(page_title="Plataforma de Inventário de Emissões", layout="centered")

st.title("🌱 Plataforma de Inventário de Emissões de GEE")
st.write("Neutralização simplificada para pequenos e médios empreendimentos")

aba = st.sidebar.radio("Menu", ["Login", "Cadastro"])

if aba == "Cadastro":
    st.subheader("Cadastro de empresa")
    cnpj = st.text_input("CNPJ")
    nome = st.text_input("Nome da empresa")
    senha = st.text_input("Senha", type="password")
    if st.button("Cadastrar"):
        if cnpj and nome and senha:
            sucesso = salvar_usuario(cnpj, nome, senha)
            if sucesso:
                st.success("Empresa cadastrada com sucesso!")
            else:
                st.error("CNPJ já cadastrado.")
        else:
            st.warning("Preencha todos os campos.")

elif aba == "Login":
    st.subheader("Login da empresa")
    cnpj = st.text_input("CNPJ")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if autenticar_usuario(cnpj, senha):
            st.success(f"Bem-vindo, empresa {cnpj}!")
            
            # Formulário de inventário
            st.header("📋 Inventário de Emissões")

            nome_empresa = st.text_input("Nome da empresa inventariada", value=cnpj)
            consumo_energia = st.number_input("Consumo de energia elétrica (kWh/mês)", min_value=0.0)
            uso_combustivel = st.number_input("Consumo de combustíveis (litros/mês)", min_value=0.0)
            residuos = st.number_input("Quantidade de resíduos gerados (kg/mês)", min_value=0.0)

            if st.button("Calcular emissões"):
                emissao_total = (consumo_energia * 0.000084) + (uso_combustivel * 2.5) + (residuos * 1.9)
                st.success(f"Emissão total estimada: {emissao_total:.2f} kg CO₂e/mês")

                # Sugestão de créditos
                preco_credito = 65.0  # R$/tCO2
                toneladas = emissao_total / 1000
                custo_neutralizar = toneladas * preco_credito
                st.info(f"Para neutralizar: {toneladas:.2f} tCO₂e → R$ {custo_neutralizar:.2f}")

        else:
            st.error("CNPJ ou senha incorretos.")
