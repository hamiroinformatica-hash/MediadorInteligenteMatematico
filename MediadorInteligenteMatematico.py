import streamlit as st
from groq import Groq
import time

# --- 1. CONFIGURAÇÃO DE INTERFACE E ESTILO ---
st.set_page_config(page_title="Mediador IntMatemático HBM", layout="wide")

st.markdown("""
    <style>
    ::-webkit-scrollbar { width: 30px !important; }
    ::-webkit-scrollbar-thumb { background: #000; border-radius: 5px; }
    .katex-display { 
        font-size: 1.4rem !important; 
        padding: 20px; 
        background: #fdfdfd; 
        border-left: 8px solid #000; 
        margin: 15px 0;
    }
    .signature-footer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: white; text-align: center; font-family: 'Algerian', serif;
        font-size: 16px; border-top: 2px solid #333; z-index: 999; padding: 10px;
    }
    .stAlert { background-color: #f0f2f6; border: none; border-radius: 10px; }
    </style>
    <div class="signature-footer">HBM - MEDIAÇÃO DIDÁTICA RADICAL (ZDP)</div>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pontos" not in st.session_state:
    st.session_state.pontos = 0

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. PROMPT MESTRE BLINDADO (REGRAS HBM ETERNAS) ---
PROMPT_HBM_RADICAL = """
VOCÊ É O MEDIADOR HBM. VOCÊ ESTÁ PROIBIDO DE RESOLVER, SIMPLIFICAR OU DEFINIR A QUESTÃO DO ALUNO.

### REGRAS CRÍTICAS (PARA SEMPRE):
1. TRANCAR: Se a questão não for de Matemática (Álgebra, Geometria, Cálculo, Estatística, etc.), recuse educadamente.
2. ZERO RESPOSTA: Nunca forneça a resposta final ou passos da questão 'X' proposta pelo aluno.
3. CONCEITOS: Nunca dê definições prontas. Use dicas e analogias do dia-a-dia moçambicano (Xipamanine, machambas, frutas, mercados).

### PROTOCOLO DE TRABALHO (P1-P6):
- P1: Aluno apresenta questão 'X'.
- P2 (INTERNO/OCULTO): Resolva 'X' mentalmente para obter 'Y'. NÃO ESCREVA ISSO.
- P3 (PROCESSAMENTO): Aguarde pelo menos 2 segundos simulando busca por similar 'S1'.
- P4 (AÇÃO): Apresente a resolução de um exercício SIMILAR 'S1'. 
    - Formato: Passo matemático em LaTeX ($$) seguido de uma EXPLICAÇÃO DIDÁTICA E DETALHADA.
    - Oriente o aluno a aplicar esta lógica na questão dele.
- P5: Aluno apresenta intervenção 'X1'.
- P6 (AVALIAÇÃO OCULTA): Compare 'X1' com seu 'Y' interno.
    a) EQUIVALENTE FINAL: Diga apenas "Está correto" e atribua [PONTO_MÉRITO].
    b) EQUIVALENTE PARCIAL: Diga "Estás num bom caminho" e atribua [MEIO_PONTO]. Apresente IMEDIATAMENTE um novo similar 'S2' para o próximo passo.
    c) NÃO EQUIVALENTE: Diga "Está errado". Apresente um similar 'c)S2' focado no erro.

### RIGOR VISUAL:
RIGOR MATEMÁTICO LATEX: Use obrigatoriamente LaTeX ($$ ou $) para toda e qualquer representação numérica ou algébrica

# --- 3. INTERFACE E LÓGICA DE EXECUÇÃO ---
st.title("🎓 Mediador IntMatemático HBM")
st.subheader(f"🏆 Pontuação Acumulada: {st.session_state.pontos}")

# Exibição do histórico
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

entrada = st.chat_input("Insira sua questão ou tentativa de resolução...")

if entrada:
    st.session_state.chat_history.append({"role": "user", "content": entrada})
    with st.chat_message("user", avatar="👤"):
        st.markdown(entrada)

    with st.chat_message("assistant", avatar="🎓"):
        placeholder = st.empty()
        placeholder.markdown("⏳ *Professor HBM a analisar a sua proposta...*")
        time.sleep(3) # Delay obrigatório de processamento P3/P6
        
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": PROMPT_HBM_RADICAL}] + st.session_state.chat_history,
                temperature=0.0
            )
            
            feedback = response.choices[0].message.content
            
            # Sistema de Pontuação P6
            if "[PONTO_MÉRITO]" in feedback:
                st.session_state.pontos += 20
                feedback = feedback.replace("[PONTO_MÉRITO]", "\n\n✨ **Objetivo Final Atingido! +20 pontos.**")
            elif "[MEIO_PONTO]" in feedback:
                st.session_state.pontos += 10
                feedback = feedback.replace("[MEIO_PONTO]", "\n\n🚀 **Passo Correto! Continua a aplicar a lógica. +10 pontos.**")

            placeholder.markdown(feedback)
            st.session_state.chat_history.append({"role": "assistant", "content": feedback})
            st.rerun()

        except Exception:
            st.error("Erro de comunicação. Por favor, reinicie ou tente novamente.")

# --- 4. BOTÃO DE RESTAURO (REINÍCIO DO PROTOCOLO) ---
st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("🔄 Reiniciar Professor (Nova Questão)", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.pontos = 0
        st.rerun()
