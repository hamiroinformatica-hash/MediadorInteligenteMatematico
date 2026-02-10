import streamlit as st
from groq import Groq
import time

# --- 1. CONFIGURAÇÃO DE INTERFACE E ESTILO ---
st.set_page_config(page_title="Mediador IntMatemático HBM", layout="wide")

st.markdown("""
    <style>
    /* Barra de rolagem otimizada para toque */
    ::-webkit-scrollbar { width: 30px !important; }
    ::-webkit-scrollbar-thumb { background: #000; border-radius: 5px; }

    /* Estilo para fórmulas LaTeX verticais */
    .katex-display { 
        font-size: 1.4rem !important; 
        padding: 15px; 
        background: #f8f9fa; 
        border-left: 6px solid #000; 
        border-radius: 4px;
    }
    
    .signature-footer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: white; text-align: center; font-family: 'Algerian', serif;
        font-size: 16px; border-top: 2px solid #333; z-index: 999; padding: 10px;
    }
    </style>
    <div class="signature-footer">HBM - Mediador Pedagógico Inviolável</div>
""", unsafe_allow_html=True)

# Gestão de Estado
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pontos" not in st.session_state:
    st.session_state.pontos = 0

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. PROMPT MESTRE (RIGOR P1-P6 E MEDIAÇÃO ZDP) ---
PROMPT_SISTEMA_HBM = """
VOCÊ É O PROFESSOR (MEDIADOR HBM). SEU PAPEL É BASEADO NO CONSTRUTIVISMO E ZDP.

### REGRAS CRÍTICAS:
1. TRANCAR: Só aceite questões de Matemática (Álgebra, Geometria, Cálculo, Estatística, etc.). Recuse outros temas.
2. NUNCA RESOLVA: É terminantemente proibido resolver ou simplificar a questão 'X' do aluno.
3. SILÊNCIO ABSOLUTO: Não dê a resposta final, nem que o aluno diga "não consigo".

### PROTOCOLO DE MEDIAÇÃO (P1-P6):
- P1: Aluno apresenta questão 'X'.
- P2 (OCULTO): Resolva 'X' internamente para encontrar 'Y'. NÃO mostre isso.
- P3 (PROCESSAMENTO): Aguarde pelo menos 2 segundos para buscar um similar.
- P4 (SIMILAR): Apresente a resolução DETALHADA e VERTICAL de um similar 'S1'. Use LaTeX ($$). Oriente o aluno a aplicar a lógica na questão 'X'.
- P5: Aluno apresenta intervenção 'X1'.
- P6 (AVALIAÇÃO OCULTA): Compare 'X1' com 'Y':
    a) Equivalente e final: "Está correto" + [PONTO_MÉRITO].
    b) Equivalente parcial: "Estás num bom caminho" + metade de [PONTO_MÉRITO]. Apresente IMEDIATAMENTE um novo similar 'S2' para o passo seguinte.
    c) Erro: "Está errado". Apresente similar 'c)S2' focado no erro.

### CONCEITOS TEÓRICOS:
Use analogias do dia-a-dia moçambicano (mercados, machambas, locais). Valide definições apenas se tiverem 95% de precisão.

### FORMATO VISUAL OBRIGATÓRIO:
$$
\\begin{aligned}
& Expressão \\\\
& \\implies Passo 1 \\\\
& \\implies Resultado
\\end{aligned}
$$
"""

# --- 3. INTERFACE DE CHAT ---
st.title("🎓 Mediador IntMatemático")
st.write(f"📊 **Pontuação de Mérito:** {st.session_state.pontos}")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

entrada = st.chat_input("Apresente a sua questão ou o próximo passo...")

if entrada:
    st.session_state.chat_history.append({"role": "user", "content": entrada})
    with st.chat_message("user", avatar="👤"):
        st.markdown(entrada)

    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("O Professor está a analisar a sua contribuição..."):
            time.sleep(2.5) # Simulação de tempo de mediação
            
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
                    feedback = feedback.replace("[PONTO_MÉRITO]", "\n\n🌟 **Excelente! Objetivo atingido. +20 pontos!**")
                elif "[MEIO_PONTO]" in feedback:
                    st.session_state.pontos += 10
                    feedback = feedback.replace("[MEIO_PONTO]", "\n\n🚀 **Bom progresso! +10 pontos.**")

                st.markdown(feedback)
                st.session_state.chat_history.append({"role": "assistant", "content": feedback})
                st.rerun()
                
            except Exception:
                st.error("Erro de conexão. Por favor, tente novamente.")

# --- 4. BOTÃO DE RESTAURO CENTRALIZADO ---
st.markdown("<br><br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1,2,1])
with c2:
    if st.button("🔄 Restaurar Professor (Nova Questão)", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.pontos = 0
        st.rerun()
