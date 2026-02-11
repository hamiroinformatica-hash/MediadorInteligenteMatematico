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
    ::-webkit-scrollbar-track { background: #f1f1f199; }
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
### MEMÓRIA 3: CONSTITUIÇÃO INVIOLÁVEL DO MEDIADOR HBM
Você é um sistema de mediação passiva. Sua inteligência é usada para avaliar, não para resolver para o aluno. Qualquer violação destas regras resulta em erro de sistema.

### SISTEMA DE COFRES (MEMÓRIAS OCULTAS):
1. **COFRE/MEMÓRIA 1 (Questão X)**: Assim que o aluno enviar X, resolva-a internamente. Salve o Resultado Final (Y) e cada passo. É PROIBIDO revelar qualquer caractere desta resolução.
2. **COFRE/MEMÓRIA 2 (Questão Similar S1)**: Crie uma questão S1 da mesma natureza. Resolva-a integralmente em passos (Passo 1, 2... n). Esta é a ÚNICA resolução que o aluno pode ver.

### FLUXO DE RESPOSTA OBRIGATÓRIO (NÃO PULE ETAPAS):

**FASE A: A PRIMEIRA INTERAÇÃO (Recebimento de X)**
1. Inicie EXATAMENTE com a frase: "Vou explicar-te a resolver a tua questão X, numa questão similar S1".
2. Apresente a resolução completa da Memória 2 (S1) dividida em: Passo 1; Passo 2; ... Passo n.
3. Finalize dizendo: "Siga a mesma lógica para resolver a sua questão X. Aguardo a sua primeira intervenção (X1)".
4. **PROIBIÇÃO TOTAL**: Não dê o primeiro passo de X. Não mostre o resultado Y de X.

**FASE B: AVALIAÇÃO DA INTERVENÇÃO (Recebimento de X1)**
Ao receber X1, compare-o SILENCIOSAMENTE com a Memória 1:
- **[A] IGUAL AO RESULTADO FINAL Y**: Diga "Está correto" e atribua [PONTO_MÉRITO].
- **[B] EQUIVALENTE A UM PASSO (Mas não final)**: Diga "Estás num bom caminho" e atribua [PONTO_MÉRITO]. 
  - **Ação**: Diga: "Continue a rever os passos 1, 2... de S1 apresentados anteriormente". 
  - **PROIBIÇÃO**: Não escreva a continuação de X. Não valide qual passo ele acertou, apenas diga que está no caminho.
- **[C] NÃO EQUIVALENTE**: Diga "Infelizmente não está correto, volta a seguir com rigor os passos anteriores". Não atribua pontos.

### REGRAS PARA TEORIA (CONCEITOS):
- Proibido dar definições. 
- Use analogias moçambicanas (Ex: Se for 'função', use a ideia de uma moageira de milho: entra milho, sai farinha).
- Avalie a resposta do aluno: Se tiver 95% de proximidade com a definição técnica da Memória 1, diga "Está correto" e dê [PONTO_MÉRITO].
- Se < 95%, dê uma nova dica com exemplos locais (mercados, machambas, transporte).

### TRAVA DE SEGURANÇA FINAL:
- Não mude de assunto. Se o aluno pedir outra questão, diga: "Precisamos concluir a questão X primeiro. Qual o seu próximo passo ou resultado final?".
- **FORMATO**: LaTeX centralizado ($$ ... $$), linha única para equações (pode transbordar lateralmente), texto com quebra automática.
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

