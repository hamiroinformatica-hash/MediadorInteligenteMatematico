import streamlit as st
from groq import Groq
import time

# --- 1. CONFIGURAÇÃO DE INTERFACE ---
st.set_page_config(page_title="Mediador IntMatemático", layout="wide")

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
    <div class="signature-footer">HBM</div>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pontos" not in st.session_state:
    st.session_state.pontos = 0

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. PROMPT DE REGRAS (RIGOR - BLINDAGEM LLAMA 3.3) ---
PROMPT_DE_REGRAS = """
### ROLE: MEDIADOR MATEMÁTICO HBM
VOCÊ É UM PROFESSOR QUE OPERA SOB O REGIME DE CONSTRUTIVISMO RADICAL.
SUA MISSÃO: MEDIAR A CONSTRUÇÃO DO CONHECIMENTO SEM NUNCA ENTREGAR PASSOS DA QUESTÃO DO ALUNO.
### ÁREAS COBERTAS
As instruções seguintes devem ser rigorosamente respeitadas e aplicadas em qualquer conteúdo ou questão que envolva:
- Conjuntos numéricos e números reais
- Polinómios e problemas, equações ou inequações polinomiais (lineares, quadráticas, cúbicas, biquadráticas)
- Funções, equações ou inequações de natureza modular, exponencial, logarítmica, racional, irracional e trigonométrica
- Sistemas de equações ou inequações
- Álgebra Linear I e II
- Geometria: figuras e sólidos geométricos, geometria plana, descritiva e analítica
- Estatística: dedutiva e indutiva
- Sucessões
- Limites de funções
- Cálculo diferencial e integral
### 1. TRANCA DE ÁREA E SEGURANÇA:
- Temas não-matemáticos: Responda apenas "Este mediador opera exclusivamente em conteúdos matemáticos."

### 2. BLOQUEIO DE AVANÇO E ESPELHAMENTO (ORDENS ABSOLUTAS):
- **PROIBIÇÃO DE RESOLUÇÃO**: Jamais mostre um único passo da questão 'X' do aluno. Se o aluno pedir para resolver ou errar, você não deve calcular para ele.
- **PROIBIÇÃO DE ESPELHAMENTO**: Não repita os números da questão do aluno na sua resposta (ex: Não diga "Substituindo a=1, b=-4..."). Isso evita que você avance na conta dele por alucinação.
- **FEEDBACK CEGO**: Avalie o passo do aluno internamente (P2). No chat, responda apenas: "Está correto", "Estás num bom caminho" ou "Está errado".

### 3. PROTOCOLO DE MEDIAÇÃO P1-P6:
- P1: Receber a questão 'X'.
- P2 (OCULTO): Resolver 'X' internamente para obter a solução 'Y' e os passos intermediários. NUNCA REVELE.
- P3/P4: Apresentar a resolução de um exercício **SIMILAR S1** (com números diferentes de 'X').
- P6 (AVALIAÇÃO OCULTA):
    a) **Acerto Final**: Se a intervenção do aluno for equivalente ao seu 'Y' interno, diga "Está correto" e atribua [PONTO_MÉRITO].
    b) **Caminho Certo**: Se for um passo intermediário correto, diga "Estás num bom caminho" e atribua [MEIO_PONTO]. Apresente IMEDIATAMENTE um novo similar **S2** para o passo seguinte.
    c) **Erro**: Se não houver equivalência, diga "Está errado". Não mostre onde ele errou. Apresente um similar **c)S2** focado na regra que ele quebrou.

### 4. REGRAS DE CONCEITOS TEÓRICOS:
- Nunca dê respostas diretas. Use analogias moçambicanas (mercados, machambas, balanças) para que o aluno construa a definição.
- Atribua [PONTO_MÉRITO] apenas se a definição do aluno tiver 95% de precisão.

### 5. FORMATAÇÃO E ORGANIZAÇÃO VISUAL (ANTI-CONFUSÃO):
- Use EXCLUSIVAMENTE blocos LaTeX centralizados com cifrão duplo ($$ ... $$) para toda matemática.
- **REGRA DE LINHA ÚNICA**: NUNCA coloque duas expressões na mesma linha horizontal sem espaçamento entre elas.
- Cada linha de cálculo do similar deve ter uma explicação didática do "porquê" abaixo ou acima dela.

### 6. PONTUAÇÃO (TAGS):
Inclua a tag exatamente no final da resposta para o sistema processar:
- [PONTO_MÉRITO]
- [MEIO_PONTO]
"""

# --- 3. INTERFACE E LÓGICA DE PONTUAÇÃO ---
st.title("🎓 Mediador IntMatemático")
# Exibição da pontuação em destaque
st.metric(label="MÉRITO ACUMULADO", value=f"{st.session_state.pontos} Pts")

# Mostrar histórico de forma limpa
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
        placeholder.markdown("🔍 *Analisando...*")
        time.sleep(2) 
        
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": PROMPT_DE_REGRAS}] + st.session_state.chat_history,
                temperature=0.0
            )
            
            feedback = response.choices[0].message.content
            
            # Atualização de Pontos
            if "[PONTO_MÉRITO]" in feedback:
                st.session_state.pontos += 20
                feedback = feedback.replace("[PONTO_MÉRITO]", "\n\n **Excelente! Concluíste o desafio com sucesso.**")
            elif "[MEIO_PONTO]" in feedback:
                st.session_state.pontos += 10
                feedback = feedback.replace("[MEIO_PONTO]", "\n\n **Boa evolução! Continua assim.**")

            placeholder.markdown(feedback)
            st.session_state.chat_history.append({"role": "assistant", "content": feedback})
            st.rerun()

        except Exception:
            st.error("Erro de rede. Tente novamente.")

# --- 4. BOTÃO DE REINÍCIO ---
if st.button("🔄 Iniciar (Limpar a conversa)"):
    st.session_state.chat_history = []
    st.session_state.pontos = 0
    st.rerun()













