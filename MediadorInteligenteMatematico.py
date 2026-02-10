import streamlit as st
from groq import Groq
import time

# --- 1. CONFIGURAÇÃO DE INTERFACE E ACESSIBILIDADE ---
st.set_page_config(page_title="Mediador IntMatemático HBM", layout="wide")

# CSS para Botões em Losango e Estilo Visual Moçambicano
st.markdown("""
    <style>
    /* Botões em Losango fixos à direita */
    .nav-container {
        position: fixed; right: 20px; top: 50%; transform: translateY(-50%);
        display: flex; flex-direction: column; gap: 20px; z-index: 1000;
    }
    .diamond-btn {
        width: 55px; height: 55px; background: #000; color: white;
        border: 2px solid white; transform: rotate(45deg);
        display: flex; align-items: center; justify-content: center;
        cursor: pointer; box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .diamond-btn span { transform: rotate(-45deg); font-size: 20px; font-weight: bold; }
    
    /* Barra de rolagem grossa para APK/Touch */
    ::-webkit-scrollbar { width: 35px !important; }
    ::-webkit-scrollbar-thumb { background: #000; border-radius: 5px; }

    /* Estilo de fórmulas LaTeX */
    .katex-display { font-size: 1.4rem !important; padding: 10px; background: #f9f9f9; border-left: 5px solid #000; }
    
    .signature-footer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: white; text-align: center; font-family: 'Algerian', serif;
        font-size: 16px; border-top: 2px solid #333; z-index: 999; padding: 10px;
    }
    </style>
    
    <div class="nav-container">
        <div class="diamond-btn" onclick="window.scrollTo(0,0)"><span>▲</span></div>
        <div class="diamond-btn" onclick="window.scrollBy(0, window.innerHeight)"><span>▼</span></div>
    </div>
    <div class="signature-footer">HBM - Mediador Pedagógico Inviolável</div>
""", unsafe_allow_html=True)

# Gestão de Estado (Memória de Chat e Pontos)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pontos" not in st.session_state:
    st.session_state.pontos = 0

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. O PROMPT MESTRE (PROTOCOLO P1-P6 INTEGRAL) ---
PROMPT_SISTEMA_HBM = """
VOCÊ É O PROFESSOR (MEDIADOR HBM). VOCÊ OPERA SOB O PROTOCOLO CONSTRUTIVISTA INVIOLÁVEL.

### REGRAS FUNDAMENTAIS:
1. TRANCAR: Se o tema não for Matemática (Álgebra, Geometria, Cálculo, etc.), responda educadamente que só media Matemática.
2. NUNCA RESOLVA: É terminantemente proibido resolver, simplificar ou dar a resposta da questão 'X' do aluno.
3. CONSTRUTIVISMO: O aluno deve construir o próprio conhecimento através de similares.

### PROTOCOLO DE MEDIAÇÃO (P1-P6):
- P1: Aluno apresenta questão 'X'.
- P2 (OCULTO): Resolva 'X' mentalmente para encontrar a resposta final 'Y'. NUNCA mostre isso.
- P3 (PROCESSAMENTO): Aguarde a busca por um similar 'S1'.
- P4 (SIMILAR): Apresente a resolução DETALHADA, PASSO-A-PASSO e VERTICAL de um exercício similar 'S1'. Use LaTeX ($$). Instrua o aluno a seguir a lógica em 'X', sem você tocar em 'X'.
- P5: Aluno apresenta intervenção 'X1'.
- P6 (AVALIAÇÃO OCULTA): Compare 'X1' com 'Y' de forma oculta:
    a) Se equivalente e final: Diga "Está correto" e use [PONTO_MÉRITO].
    b) Se equivalente mas parcial: Diga "Estás num bom caminho" e use [MEIO_PONTO]. Apresente IMEDIATAMENTE um novo similar 'S2' para o passo seguinte.
    c) Se não equivalente (erro): Diga "Está errado". Não dê pontos. Apresente um novo similar 'c)S2' que trate especificamente da falha do aluno.

### CONCEITOS TEÓRICOS:
NUNCA dê a definição. Use analogias moçambicanas (mercados, machambas, transporte, frutas) para induzir o pensamento socrático. Atribua pontos apenas se a definição do aluno atingir 95% de precisão.

### FORMATO VISUAL:
Use sempre alinhamento vertical em LaTeX:
$$
\\begin{aligned}
& Expressão \\\\
& \\implies Passo 1 \\\\
& \\implies Resultado
\\end{aligned}
$$
"""

# --- 3. INTERFACE E LOGICA ---
st.title("🎓 Mediador IntMatemático")
st.write(f"📊 **Pontuação de Evolução:** {st.session_state.pontos}")

# Exibição do Chat
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

entrada = st.chat_input("Apresente sua questão matemática ou passo de resolução...")

if entrada:
    st.session_state.chat_history.append({"role": "user", "content": entrada})
    with st.chat_message("user", avatar="👤"):
        st.markdown(entrada)

    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("Professor a processar mediação pedagógica..."):
            # Delay pedagógico obrigatório (P3/P6)
            time.sleep(2.5)
            
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": PROMPT_SISTEMA_HBM}] + st.session_state.chat_history,
                    temperature=0.0
                )
                
                feedback = response.choices[0].message.content
                
                # Gamificação P6
                if "[PONTO_MÉRITO]" in feedback:
                    st.session_state.pontos += 20
                    feedback = feedback.replace("[PONTO_MÉRITO]", "\n\n✨ **Parabéns! Internalizaste o conhecimento. +20 pontos!**")
                elif "[MEIO_PONTO]" in feedback:
                    st.session_state.pontos += 10
                    feedback = feedback.replace("[MEIO_PONTO]", "\n\n🚀 **Excelente progresso! Estás no caminho certo. +10 pontos!**")

                st.markdown(feedback)
                st.session_state.chat_history.append({"role": "assistant", "content": feedback})
                st.rerun()
                
            except Exception:
                st.error("Erro na ligação. Tente novamente.")

# --- 4. BOTÃO DE RESTAURO (CENTRALIZADO) ---
st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("🔄 Restaurar Chat (Nova Questão)", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.pontos = 0
        st.rerun()
