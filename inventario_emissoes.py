import streamlit as st

st.set_page_config(page_title="Inventário de Emissões", page_icon="🌿", layout="centered")

# Simulação de base de dados de usuários
usuarios = {
    "Restaurante do Pará": "1234",
    "Açaí Verde LTDA": "senhaacai",
    "Amazon BioCafé": "cafebio2025"
}

def login():
    st.markdown("## 🔐 Acesso à Plataforma")
    st.markdown("Insira os dados da sua empresa para acessar o inventário de emissões.")

    empresa = st.text_input("🏢 Nome da empresa")
    senha = st.text_input("🔑 Senha", type="password")

    if st.button("Entrar"):
        if empresa in usuarios and usuarios[empresa] == senha:
            st.session_state["logado"] = True
            st.session_state["empresa"] = empresa
        else:
            st.error("Nome da empresa ou senha incorretos.")

def inventario():
    st.markdown(f"## 🌿 Bem-vindo(a), **{st.session_state['empresa']}**!")
    st.markdown("### Plataforma de Coleta de Dados para Inventário de Emissões de GEE")
    st.info("Preencha os dados abaixo para estimar as emissões mensais do seu negócio.")

    with st.form("formulario_emissoes"):
        energia = st.number_input("🔌 Consumo de energia elétrica (kWh/mês):", min_value=0.0, step=10.0)
        combustivel = st.number_input("⛽ Consumo de combustível (litros/mês):", min_value=0.0, step=10.0)
        gas = st.number_input("🍳 Gás de cozinha (kg/mês):", min_value=0.0, step=1.0)
        agua = st.number_input("🚿 Consumo de água (m³/mês):", min_value=0.0, step=1.0)
        residuos = st.number_input("🗑️ Geração de resíduos (kg/mês):", min_value=0.0, step=1.0)

        calcular = st.form_submit_button("📊 Calcular Emissões")

    if calcular:
        fe_energia = 0.05
        fe_combustivel = 2.3
        fe_gas = 2.9
        fe_agua = 0.3
        fe_residuos = 1.8

        total_emissoes = (
            energia * fe_energia +
            combustivel * fe_combustivel +
            gas * fe_gas +
            agua * fe_agua +
            residuos * fe_residuos
        )

        st.success(f"🌎 Emissões mensais estimadas: **{total_emissoes:.2f} kg CO₂e**")
        st.markdown("---")
        st.markdown("🎯 *Próximo passo: gere seu selo de neutralização ou exporte este relatório.*")

# Inicialização da sessão
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    login()
else:
    inventario()
