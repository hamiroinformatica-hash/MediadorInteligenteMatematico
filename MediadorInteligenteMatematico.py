import streamlit as st
from groq import Groq
import time

# --- 1. CONFIGURAÇÃO DE INTERFACE ---
st.set_page_config(page_title="Mediador IntMatemático HBM", layout="wide")

st.markdown("""
    <style>
    ::-webkit-scrollbar { width: 30px !important; }
    ::-webkit-scrollbar-thumb { background: #000; border-radius: 5px; }
    .katex-display { 
        font-size: 1.4rem !important; 
        padding: 15px; 
        background: #f9f9f9; 
        border-left: 8px solid #000; 
        margin: 10px 0;
    }
    .didactic-box {
        background-color: #f0f4f8;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #d1d9e6;
        margin-bottom: 20px;
    }
    .signature-footer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: white; text-align: center; font-family: 'Algerian', serif;
        font-size: 16px; border-top: 2px solid #333; z-index: 999; padding: 10px;
    }
    </style>
    <div class="signature-footer">HBM - MEDIAÇÃO PEDAGÓGICA INVIOLÁVEL</div>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pontos" not in st.session_state:
    st.session_state.pontos = 0

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. PROMPT MESTRE (RIGOR DIDÁTICO INTERCALADO) ---
PROMPT_HBM_FINAL = """
VOCÊ É O MEDIADOR HBM. VOCÊ OPERA SOB O REGIME DE CONSTRUTIVISMO RADICAL.

### ORDENS ABSOLUTAS:
1. NUNCA RESOLVA: Mesmo que o aluno erre ou peça, você jamais deve mostrar um único passo da questão 'X' dele.
2. NUNCA MOSTRE RESOLUÇÃO DO ALUNO: Se o aluno enviar um passo, avalie internamente, mas não reproduza a conta dele resolvida na tela.
3. DIDÁTICA INTERCALADA: Ao resolver o SIMILAR 'S1', cada linha de LaTeX deve ser seguida por uma explicação do "PORQUÊ" daquele movimento.

### PROTOCOLO P1-P6:
- P1: Aluno apresenta questão 'X'.
- P2 (INTERNO): Calcule a resposta 'Y' de 'X' e guarde para si. NUNCA MOSTRE.
- P3 (ESPERA): Simule processamento de 2 segundos.
- P4 (AÇÃO): Apresente um SIMILAR 'S1'. 
    - Estrutura: [Passo LaTeX] -> [Explicação Didática do que fazer] -> [Orientação para o aluno fazer igual na 'X'].
- P5: Aluno tenta 'X1'.
- P6 (AVALIAÇÃO OCULTA): Compare 'X1' com seu 'Y' interno.
    a) ACERTO FINAL: "Está correto" + [PONTO_MÉRITO].
    b) CAMINHO CERTO: "Estás num bom caminho" + [MEIO_PONTO]. Apresente IMEDIATAMENTE um similar 'S2' para o passo seguinte.
    c) ERRO: "Está errado". Não mostre o erro na conta dele. Apresente um similar 'c)S2' focado na regra que ele quebrou.

### CONCEITOS TEÓRICOS:
Use analogias moçambicanas. Se perguntarem "O que é uma inequação?", responda com uma dica sobre balanças ou comparações de preços no mercado, para que ele construa a definição.
"""

# --- 3. EXECUÇÃO DO SISTEMA ---
st.title("🎓 Mediador IntMatemático")
st.markdown(f"### 🏆 Pontuação: `{st.session_state.pontos}`")

# Mostrar histórico de forma limpa
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

entrada = st.chat_input("Apresente sua questão ou passo aqui...")

if entrada:
    st.session_state.chat_history.append({"role": "user", "content": entrada})
    with st.chat_message("user", avatar="👤"):
        st.markdown(entrada)

    with st.chat_message("assistant", avatar="🎓"):
        placeholder = st.empty()
        placeholder.markdown("🔍 *Analisando logicamente (Mediação HBM)...*")
        time.sleep(2) 
        
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": PROMPT_HBM_FINAL}] + st.session_state.chat_history,
                temperature=0.0
            )
            
            feedback = response.choices[0].message.content
            
            # Atualização de Pontos
            if "[PONTO_MÉRITO]" in feedback:
                st.session_state.pontos += 20
                feedback = feedback.replace("[PONTO_MÉRITO]", "\n\n✅ **Excelente! Concluíste o desafio com sucesso.**")
            elif "[MEIO_PONTO]" in feedback:
                st.session_state.pontos += 10
                feedback = feedback.replace("[MEIO_PONTO]", "\n\n📈 **Boa evolução! Continua assim.**")

            placeholder.markdown(feedback)
            st.session_state.chat_history.append({"role": "assistant", "content": feedback})
            st.rerun()

        except Exception:
            st.error("Erro de rede. Tente novamente.")

# --- 4. BOTÃO DE REINÍCIO ---
if st.button("🔄 Iniciar Nova Mediação (Limpar)"):
    st.session_state.chat_history = []
    st.session_state.pontos = 0
    st.rerun()
