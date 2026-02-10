import streamlit as st
from groq import Groq
import time

# --- 1. CONFIGURAÇÃO DE INTERFACE E RENDERIZAÇÃO ---
st.set_page_config(page_title="Mediador IntMatemático HBM", layout="wide")

st.markdown("""
    <style>
    /* Estilização para fórmulas grandes e legíveis */
    .katex-display { 
        font-size: 1.5rem !important; 
        padding: 15px; 
        background: #f8f9fa; 
        border-radius: 10px;
    }
    .signature-footer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: white; text-align: center; font-family: 'Algerian', serif;
        font-size: 16px; border-top: 2px solid #333; z-index: 1000; padding: 10px;
    }
    </style>
    <div class="signature-footer">HBM - Mediação Didática e Estética</div>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pontos" not in st.session_state:
    st.session_state.pontos = 0

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. PROMPT DE SISTEMA: FOCO EM ALINHAMENTO VERTICAL ---
PROMPT_SISTEMA_V4 = """
Você é o MEDIADOR HBM. 

### REGRA DE OURO VISUAL (NÃO NEGOCIÁVEL):
1. **Verticalidade Total:** Você deve usar obrigatoriamente o ambiente `\\begin{aligned} ... \\end{aligned}` dentro de `$$` para todas as resoluções.
2. **Símbolo de Passo:** Use `\\implies` no início de cada linha nova.
3. **Quebra de Linha:** Use `\\\\` ao final de cada linha no LaTeX para garantir que fiquem uma embaixo da outra.

### PROTOCOLO PEDAGÓGICO:
- Se o aluno intervir, responda apenas: "Está correto", "Estás num bom caminho" ou "Está errado".
- NUNCA mencione os números da questão dele.
- Após o feedback, resolva um SIMILAR 'S2' neste formato:
$$
\\begin{aligned}
& Expressão \\\\
& \\implies Passo 1 \\\\
& \\implies Passo 2 \\\\
& \\implies Resultado
\\end{aligned}
$$
"""

# --- 3. EXIBIÇÃO E LÓGICA ---
st.title("🎓 Mediador IntMatemático")
st.write(f"🏆 Pontos: {st.session_state.pontos}")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

entrada = st.chat_input("Digite sua resposta...")

if entrada:
    st.session_state.chat_history.append({"role": "user", "content": entrada})
    st.rerun() # Atualiza a tela imediatamente para mostrar a fala do aluno

# Lógica para processar a resposta da IA (evita o travamento da conexão)
if len(st.session_state.chat_history) > 0 and st.session_state.chat_history[-1]["role"] == "user":
    with st.chat_message("assistant", avatar="🎓"):
        container = st.empty()
        with st.spinner("Analisando e organizando verticalmente..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": PROMPT_SISTEMA_V4}] + st.session_state.chat_history,
                    temperature=0.0
                )
                feedback = response.choices[0].message.content
                
                # Processamento de pontos
                if "[PONTO_MÉRITO]" in feedback:
                    st.session_state.pontos += 20
                    feedback = feedback.replace("[PONTO_MÉRITO]", "\n\n✨ **Parabéns! +20 pontos.**")
                elif "[MEIO_PONTO]" in feedback:
                    st.session_state.pontos += 10
                    feedback = feedback.replace("[MEIO_PONTO]", "\n\n🚀 **Bom caminho! +10 pontos.**")

                st.session_state.chat_history.append({"role": "assistant", "content": feedback})
                st.rerun() # Agora recarrega APÓS salvar a resposta
                
            except Exception:
                st.error("Erro na mediação. Tente reenviar.")

if st.sidebar.button("🔄 Reiniciar"):
    st.session_state.chat_history = []
    st.session_state.pontos = 0
    st.rerun()
