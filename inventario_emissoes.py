import streamlit as st
import pandas as pd
import csv
import os

st.set_page_config(page_title="Inventário de Emissões", page_icon="🌱", layout="centered")

# ---------------- Funções auxiliares ----------------

def salvar_usuario(nome, senha):
    if not os.path.exists("usuarios.csv"):
        with open("usuarios.csv", mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["nome", "senha"])
    with open("usuarios.csv", mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([nome, senha])

def carregar_usuarios():
    if os.path.exists("usuarios.csv"):
        return pd.read_csv("usuarios.csv")
    else:
        return pd.DataFrame(columns=["nome", "senha"])

def autenticar_usuario(nome, senha):
    usuarios = carregar_usuarios()
    user = usuarios[
        (usuarios["nome"].str.strip() == nome) &
        (usuarios["senha"].str.strip() == senha)
    ]
    return not user.empty

# ---------------- Página principal ----------------

st.title("🌿 Plataforma de Inventário de Emissões")
st.markdown("Democratizando a neutralização de emissões para pequenos e médios negócios.")

menu = ["Login", "Cadastrar nova empresa"]
opcao = st.sidebar.selectbox("Menu", menu)

# ---------------- Cadastro ----------------

if opcao == "Cadastrar nova empresa":
    st.subheader("Cadastro")
    nome = st.text_input("Nome da empresa").strip()
    senha = st.text_input("Senha", type="password").strip()
    if st.button("Cadastrar"):
        if not nome or not senha:
            st.error("Preencha todos os campos.")
        else:
            salvar_usuario(nome, senha)
            st.success("Cadastro realizado com sucesso!")

# ---------------- Login ----------------

else:
    st.subheader("Login")
    nome = st.text_input("Nome da empresa").strip()
    senha = st.text_input("Senha", type="password").strip()
    if st.button("Entrar"):
        if autenticar_usuario(nome, senha):
            st.success(f"Bem-vindo(a), {nome}!")
            # Conteúdo principal após login
            app_section(nome)
        else:
            st.error("Nome ou senha incorretos.")

# ---------------- Conteúdo principal ----------------

def app_section(nome):
    st.header("📄 Preencher Inventário de Emissões")
    st.markdown(f"Empresa: **{nome}**")

    tipo_negocio = st.selectbox("Qual é o tipo do seu negócio?", ["Restaurante", "Loja", "Serviço", "Outro"])
    consumo_energia = st.number_input("Consumo mensal de energia elétrica (kWh)", min_value=0.0)
    consumo_combustivel = st.number_input("Consumo mensal de combustíveis (litros)", min_value=0.0)
    deslocamentos = st.number_input("Deslocamentos mensais a trabalho (km)", min_value=0.0)

    if st.button("Calcular emissões"):
        fator_energia = 0.000054  # tCO2/kWh
        fator_combustivel = 0.0023  # tCO2/litro (média)
        fator_deslocamento = 0.00021  # tCO2/km

        total_emissoes = (
            consumo_energia * fator_energia +
            consumo_combustivel * fator_combustivel +
            deslocamentos * fator_deslocamento
        )

        st.success(f"Emissões estimadas: **{total_emissoes:.4f} tCO₂e/mês**")

        if total_emissoes > 0:
            st.markdown("🔄 Para neutralizar essas emissões, recomendamos a compra de créditos de carbono de projetos REDD.")
            st.button("Solicitar contato para neutralização")
