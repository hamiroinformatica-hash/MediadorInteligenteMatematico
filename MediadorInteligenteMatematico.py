import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Configuração da Página
st.set_page_config(page_title="TutorIntEqQuadratica", page_icon="🎓")

# Título e Estilo
st.markdown("<h2 style='text-align: center; color: #006644;'>Mediador de Equações Quadráticas</h2>",
            unsafe_allow_html=True)

# Configuração da API do Gemini
API_KEY = "AIzaSyB0PprNuZohuTZeAsGgkslQ8SshmW7osgY"  # Substitua pela sua chave
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Inicializar histórico da conversa
if "messages" not in st.session_state:
    st.session_state.messages = []

# Botão para Limpar Conversa
if st.sidebar.button("Limpar Chat 🗑️"):
    st.session_state.messages = []
    st.rerun()

# Interface de Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de Dados: Texto ou Câmara
st.markdown("---")
col1, col2 = st.columns([3, 1])

with col2:
    # O Streamlit abre a câmara nativa automaticamente no telemóvel
    foto = st.camera_input("📷 Scanner")

with col1:
    entrada_texto = st.chat_input("Escreva o seu passo aqui...")

# Lógica de Processamento
if entrada_texto or foto:
    user_content = entrada_texto if entrada_texto else "Analise a minha resolução nesta foto."

    # Adicionar mensagem do aluno ao chat
    st.session_state.messages.append({"role": "user", "content": user_content})
    with st.chat_message("user"):
        st.markdown(user_content)

    # Prompt Pedagógico (Mediador Socrático)
    prompt = (
        "Age como um mediador pedagógico socrático. O aluno enviou um passo de uma equação quadrática. "
        "Analise criticamente, aponte erros de lógica sem dar a resposta final. "
        "Apresente um exemplo similar bem formatado usando símbolos como x², Δ e ±."
    )

    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("O Tutor está a analisar..."):
            try:
                if foto:
                    img = Image.open(foto)
                    response = model.generate_content([prompt, img])
                else:
                    response = model.generate_content(f"{prompt}\nEntrada do aluno: {entrada_texto}")

                full_response = response.text
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error("Erro de conexão com a IA. Verifique a sua Chave API.")