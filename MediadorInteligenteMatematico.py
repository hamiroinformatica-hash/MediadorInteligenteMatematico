import streamlit as st
from groq import Groq
import time

# --- CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Mediador IntMatemático HBM", layout="wide")
st.markdown("""
    <style>
    ::-webkit-scrollbar { width: 35px !important; }
    ::-webkit-scrollbar-thumb { background: #000; border-radius: 10px; }
    .signature-footer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: white; text-align: center; font-family: 'Algerian', serif;
        font-size: 16px; border-top: 2px solid #333; z-index: 1000; padding: 5px;
    }
    </style>
    <div class="signature-footer">HBM - Mediação Didática Estrita</div>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pontos" not in st.session_state:
    st.session_state.pontos = 0

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- PROMPT MESTRE REFORMULADO (BLINDAGEM CONTRA RESOLUÇÃO DIRETA) ---
PROMPT_SISTEMA_ESTRITO = """
VOCÊ É O MEDIADOR HBM. VOCÊ ESTÁ PROIBIDO DE RESOLVER OU SIMPLIFICAR A QUESTÃO DO ALUNO.

### FLUXO OBRIGATÓRIO (NÃO DESVIE):
1. P1: O aluno envia a questão 'X'.
2. P2 (OCULTO): Resolva 'X' internamente. NUNCA escreva nada sobre 'X' na resposta, nem mesmo uma simplificação inicial.
3. P3 (SIMILAR): Crie uma questão similar 'S1'.
4. P4 (RESPOSTA): 
   - Você deve RESOLVER COMPLETAMENTE a questão 'S1' passo a passo no chat usando LaTeX ($$).
   - Diga explicitamente: "Eu resolvi este exemplo similar para você. Agora, sem que eu mexa na sua questão, aplique estes mesmos passos na sua equação 'X'."
5. P5/P6 (AVALIAÇÃO): 
   - Se o aluno enviar um passo 'X1', verifique a equivalência com seu P2 oculto.
   - Se CORRETO parcial: Diga "Estás num bom caminho" [MEIO_PONTO] e resolva um NOVO similar 'S2' para o próximo passo.
   - Se CORRETO final: Diga "Está correto" [PONTO_MÉRITO].
   - Se ERRADO: Diga "Está errado", ignore o erro dele e apresente a resolução de um NOVO similar 'S2' que mostre como evitar aquele erro.

### REGRAS CRÍTICAS DE "BLOQUEIO":
- É TERMINANTEMENTE PROIBIDO escrever qualquer termo da equação original do aluno (ex: se ele deu x-9x, você não pode escrever -8x).
- Se você tocar na equação do aluno, você falhou na sua missão pedagógica.
- Use analogias de Moçambique (machambas, mercados) para explicar conceitos teóricos.
- Use obrigatoriamente LaTeX ($$) para toda a matemática.
"""

# --- INTERFACE ---
st.title("🎓 Mediador IntMatemático")
st.subheader(f"Pontos: {st.session_state.pontos}")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

entrada = st.chat_input("Apresente sua questão ou passo...")

if entrada:
    st.session_state.chat_history.append({"role": "user", "content": entrada})
    with st.chat_message("user", avatar="👤"):
        st.markdown(entrada)

    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("Realizando mediação pedagógica..."):
            time.sleep(2.5)
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": PROMPT_SISTEMA_ESTRITO}] + st.session_state.chat_history,
                    temperature=0.0
                )
                
                feedback = response.choices[0].message.content
                
                # Processamento de Pontos
                if "[PONTO_MÉRITO]" in feedback:
                    st.session_state.pontos += 20
                    feedback = feedback.replace("[PONTO_MÉRITO]", "\n\n✨ **Parabéns! +20 pontos!**")
                elif "[MEIO_PONTO]" in feedback:
                    st.session_state.pontos += 10
                    feedback = feedback.replace("[MEIO_PONTO]", "\n\n🚀 **Caminho correto! +10 pontos!**")
                
                st.markdown(feedback)
                st.session_state.chat_history.append({"role": "assistant", "content": feedback})
                st.rerun()
            except:
                st.error("Erro na conexão.")

if st.sidebar.button("🔄 Limpar para Nova Questão"):
    st.session_state.chat_history = []
    st.session_state.pontos = 0
    st.rerun()
