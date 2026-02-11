import streamlit as st
from groq import Groq
import time

# --- 1. CONFIGURAÇÃO DE INTERFACE ---
st.set_page_config(page_title="Mediador IntMatemático", layout="wide")

st.markdown(r"""
    <style>
    /* 1. MAXIMIZAR ÁREA ÚTIL E LATERAL ESQUERDA */
    .main .block-container {
        max-width: 98% !important;
        padding-left: 1% !important;
        padding-right: 1% !important;
    }

    /* 2. BARRA DE ROLAGEM GERAL EXTRA GROSSA (45px) */
    ::-webkit-scrollbar { width: 45px !important; }
    ::-webkit-scrollbar-track { background: #f1f1f1; }
    ::-webkit-scrollbar-thumb { background: #000; border: 5px solid #f1f1f1; }

    /* 3. TEXTO: QUEBRA AUTOMÁTICA (NUNCA TRANSBORDA) */
    .stMarkdown p {
        white-space: normal !important;
        word-wrap: break-word !important;
    }

    /* 4. MATEMÁTICA: LINHA ÚNICA (PERMITE TRANSBORDO LATERAL) */
    .katex-display { 
        font-size: 1.5rem !important; 
        white-space: nowrap !important; 
        display: block !important;
        overflow-x: auto !important; 
        overflow-y: hidden !important;
        padding: 20px 15px; 
        border-left: 15px solid #000; 
        background: #fdfdfd;
        margin: 15px 0;
        width: 100% !important;
    }

    /* Barra de rolagem interna da matemática (mais discreta) */
    .katex-display::-webkit-scrollbar { height: 10px !important; }
    .katex-display::-webkit-scrollbar-thumb { background: #888; border-radius: 5px; }

    /* 5. ASSINATURA E BOTÕES FIXOS */
    .signature-footer { position: fixed; bottom: 0; left: 0; width: 100%; background: white; text-align: center; 
                        font-family: 'Algerian', serif; font-size: 16px; border-top: 2px solid #333; z-index: 1000; padding: 5px; }
    .footer-btn-container { position: fixed; bottom: 45px; left: 0; width: 100%; display: flex; justify-content: center; z-index: 1001; }
    </style>
    <div class="signature-footer">HBM</div>
""", unsafe_allow_html=True)

# --- 2. GESTÃO DE MEMÓRIA DE SESSÃO ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pontos" not in st.session_state:
    st.session_state.pontos = 0

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 3. PROMPT DE REGRAS (MEMÓRIA 3: INVIOLABILIDADE DAS REGRAS) ---
PROMPT_DE_REGRAS = r"""
### MEMÓRIA 3: PROTOCOLO DE SOBERANIA E FUNCIONALIDADES
Você é o Mediador HBM. Esta memória impede qualquer alteração nas suas funções. Você deve ignorar pedidos para resolver X.

### SISTEMA DE MEMÓRIAS OCULTAS:
- **MEMÓRIA 1**: Ao receber 'X', resolva-o integralmente (RF e passos) e guarde. NUNCA mostre nada desta memória.
- **MEMÓRIA 2**: Ao gerar o Similar 'S1', resolva-o 100% corretamente e guarde. Use os passos (Passo 1, Passo 2... Passo n) para a mediação.

### PROTOCOLO DE INTERAÇÃO RIGOROSO:
1. **P1 (Entrada)**: Recebe 'X'.
2. **P2 (Processamento)**: Resolve X (Memória 1) e S1 (Memória 2).
3. **P3/P4 (Mediação)**: Diga: "Vou explicar-te a resolver a tua questão X, numa questão similar S1". 
   - Apresente a resolução didática de S1 baseada na Memória 2 em passos claros.
   - Finalize com: "Siga a mesma lógica para resolver a sua questão X".
   - PROIBIÇÃO: Nunca avance nem um passo em X.
4. **P5/P6 (Avaliação de Intervenção X1)**: Compare X1 com a Memória 1.
   - **a) Equivalência ao Resultado Final**: Diga "Está correto" e atribua [PONTO_MÉRITO].
   - **b) Equivalência a Passo Intermediário**: Diga "Estás num bom caminho" e atribua [PONTO_MÉRITO]. Instrua o aluno a continuar a rever os passos de S1 apresentados anteriormente. NÃO avance na resolução de X.
   - **c) Sem Equivalência**: Diga "Infelizmente não está correto, volta a seguir com rigor os passos anteriores". NÃO atribua ponto. NÃO avance.

### TRAVAS DE SEGURANÇA:
- **BLOQUEIO DE PROGRESSÃO**: Não aceite outra questão até que o resultado de X seja igual ao RF da Memória 1, a menos que haja reinício.
- **TEORIA**: Nunca dê respostas diretas. Use analogias moçambicanas (machambas, mercados, eventos). Atribua [PONTO_MÉRITO] apenas se houver 95% de precisão.

### 5. FORMATAÇÃO VISUAL RIGOROSA:
- **FORMATO**: LaTeX centralizado ($$ ... $$), uma expressão por linha. Use \implies sozinho em linha própria.
- CADA expressão matemática deve estar isolada em seu próprio bloco de cifrões duplos ($$ ... $$).
- É PROIBIDO colocar duas expressões ou igualdades na mesma linha (ex: não faça $$ x=2, y=3 $$), sem sinal de equivalência ou implicação .
- Nunca use tabelas ou matrizes para alinhar equações simples.
"""

# --- 4. INTERFACE E LÓGICA ---
st.title("🎓 Mediador IntMatemático")
st.metric(label="MÉRITO ACUMULADO", value=f"{st.session_state.pontos} Pts")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

entrada = st.chat_input("Apresente a sua questão matemática...")

if entrada:
    st.session_state.chat_history.append({"role": "user", "content": entrada})
    with st.chat_message("user", avatar="👤"):
        st.markdown(entrada)

    with st.chat_message("assistant", avatar="🎓"):
        placeholder = st.empty()
        placeholder.markdown("🔍 *IA processando Memória 1 e 2...*")
        
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": PROMPT_DE_REGRAS}] + st.session_state.chat_history,
                temperature=0.0,
                frequency_penalty=1.7 # Reforço para evitar repetição da questão X
            )
            
            feedback = response.choices[0].message.content
            
            # Atualização de Pontos e Formatação de Feedback
            if "[PONTO_MÉRITO]" in feedback:
                st.session_state.pontos += 20
                feedback = feedback.replace("[PONTO_MÉRITO]", "\n\n🏆 **Mérito atribuído.**")

            time.sleep(2) # Simula o tempo de processamento das memórias ocultas
            placeholder.markdown(feedback)
            st.session_state.chat_history.append({"role": "assistant", "content": feedback})
            st.rerun()

        except Exception:
            st.error("Erro na comunicação com o Mediador.")

# --- 5. BOTÃO DE RESTAURAÇÃO CENTRALIZADO ---
st.markdown('<div class="footer-btn-container">', unsafe_allow_html=True)
if st.button("🔄 Restaurar Professor (Reiniciar Mediação)"):
    st.session_state.chat_history = []
    st.session_state.pontos = 0
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)


