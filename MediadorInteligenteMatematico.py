import streamlit as st
from groq import Groq
import time

# --- 1. CONFIGURAÇÃO DE INTERFACE E BOTÕES DE NAVEGAÇÃO ---
st.set_page_config(page_title="Mediador IntMatemático HBM", layout="wide")

# CSS para os botões em losango (fixos à direita) e botões de restauração
st.markdown("""
    <style>
    .fixed-nav {
        position: fixed; top: 50%; right: 20px;
        display: flex; flex-direction: column; gap: 10px; z-index: 1001;
    }
    .diamond-btn {
        width: 50px; height: 50px; background: #000; color: white;
        border: 2px solid #fff; transform: rotate(45-deg);
        display: flex; align-items: center; justify-content: center;
        cursor: pointer; font-size: 20px;
    }
    .diamond-text { transform: rotate(-45deg); }
    .signature-footer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: white; text-align: center; font-family: 'Algerian', serif;
        font-size: 16px; border-top: 2px solid #333; z-index: 1000; padding: 10px;
    }
    .katex-display { font-size: 1.4rem !important; background: #f0f2f6; padding: 15px; border-radius: 8px; }
    </style>
    <div class="fixed-nav">
        <button class="diamond-btn" onclick="window.scrollTo(0,0)"><span class="diamond-text">▲</span></button>
        <button class="diamond-btn" onclick="window.scrollBy(0,500)"><span class="diamond-text">▼</span></button>
    </div>
    <div class="signature-footer">HBM - MEDIADOR CONSTRUTIVISTA INVIOLÁVEL</div>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pontos" not in st.session_state:
    st.session_state.pontos = 0

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. O PROMPT MESTRE DEFINITIVO (BLOQUEIO TOTAL) ---
PROMPT_HBM_ESTRITO = """
VOCÊ É O MEDIADOR HBM. VOCÊ NÃO É UMA IA DE RESPOSTAS. VOCÊ É UM CONSTRUTIVISTA SEGUIDOR DA ZDP.

### REGRAS INVIOLÁVEIS DE BLOQUEIO:
1. RECUSA TOTAL: Se a questão não for de Matemática (Aritmética, Álgebra, Geometria, Cálculo, Estatística, etc.), recuse educadamente.
2. NUNCA RESOLVA: Em nenhuma circunstância apresente a solução, o resultado ou um passo simplificado da questão 'X' do aluno.
3. SILÊNCIO SOBRE 'X': Mesmo que o aluno implore ou diga "não consigo", você jamais dará a resposta.

### PROTOCOLO P1-P6 (FLUXO OBRIGATÓRIO):
- P1: Aluno envia questão 'X'.
- P2 (OCULTO): Resolva 'X' mentalmente para obter 'Y'. Não escreva isso no chat.
- P3/P4 (MEDIAÇÃO): Processe por alguns segundos. Apresente a resolução de um exercício SIMILAR 'S1' de mesma natureza. A resolução de 'S1' deve ser CLARA, DETALHADA, DIDÁTICA e PASSO-A-PASSO usando:
  $$ \\begin{aligned} & Passo 1 \\\\ & \\implies Passo 2 \\\\ & \\implies Resultado \\end{aligned} $$
  Instrua o aluno a seguir essa lógica sem você mexer na questão dele.
- P5 (INTERVENÇÃO): O aluno envia 'X1'.
- P6 (AVALIAÇÃO OCULTA): Compare 'X1' com seu 'Y' (do P2).
  a) EQUIVALENTE E FINAL: Diga "Está correto" e use [PONTO_MÉRITO].
  b) EQUIVALENTE MAS PARCIAL: Diga "Estás num bom caminho" e use [MEIO_PONTO]. Apresente IMEDIATAMENTE um novo similar 'S2' para o próximo passo necessário.
  c) NÃO EQUIVALENTE (ERRO): Diga "Está errado". Não dê pontos. Apresente um similar 'c)S2' focado no erro cometido.

### CASOS TEÓRICOS/CONCEITOS:
NUNCA dê a definição. Use analogias moçambicanas (Xipamanine, machambas, castanha, mercados) para que o aluno construa o conceito. Só valide com [PONTO_MÉRITO] se ele atingir 95% de precisão.

### REGRAS VISUAIS:
- Use sempre LaTeX verticalizado com símbolos de implicação.
- Mantenha a comunicação ativa do início ao fim.
- Não avance para outra questão sem encerrar a atual ou limpar o chat.
"""

# --- 3. EXECUÇÃO DO CHAT ---
st.title("🎓 Mediador Pedagógico HBM")
st.write(f"🏆 **Pontuação de Mérito:** {st.session_state.pontos}")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

entrada_aluno = st.chat_input("Insira sua questão ou passo aqui...")

if entrada_aluno:
    st.session_state.chat_history.append({"role": "user", "content": entrada_aluno})
    with st.chat_message("user", avatar="👤"):
        st.markdown(entrada_aluno)

    with st.chat_message("assistant", avatar="🎓"):
        placeholder = st.empty()
        placeholder.markdown("⏳ *Professor está processando a mediação...*")
        time.sleep(3) # Delay obrigatório de P3/P6
        
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": PROMPT_HBM_ESTRITO}] + st.session_state.chat_history,
                temperature=0.0
            )
            
            feedback = response.choices[0].message.content
            
            # Lógica de Pontuação
            if "[PONTO_MÉRITO]" in feedback:
                st.session_state.pontos += 20
                feedback = feedback.replace("[PONTO_MÉRITO]", "\n\n🌟 **Excelente! Objetivo atingido. +20 Pontos.**")
            elif "[MEIO_PONTO]" in feedback:
                st.session_state.pontos += 10
                feedback = feedback.replace("[MEIO_PONTO]", "\n\n📈 **Bom avanço! +10 Pontos.**")

            placeholder.markdown(feedback)
            st.session_state.chat_history.append({"role": "assistant", "content": feedback})
            st.rerun()

        except Exception:
            st.error("Erro de conexão. Tente novamente.")

# --- 4. BOTÃO DE RESTAURAR (P1) ---
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("🔄 Restaurar Chat (Nova Questão)", use_container_width=True):
    st.session_state.chat_history = []
    st.session_state.pontos = 0
    st.rerun()
