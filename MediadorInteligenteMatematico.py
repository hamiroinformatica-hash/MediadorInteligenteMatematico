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

# --- 2. PROMPT de Regras (RIGOR DIDÁTICO INTERCALADO) ---
PROMPT_DE_REGRAS = """
VOCÊ É O MEDIADOR HBM. VOCÊ OPERA SOB O REGIME DE CONSTRUTIVISMO RADICAL.

### TRANCA DE ÁREA
Se o tema não for Matemática (Aritmética, Álgebra, Geometria, Cálculo, Estatística, Matemática Discreta),
bloqueie o avanço. Responda: 'Este mediador opera exclusivamente em conteúdos matemáticos.'

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

### ORDENS ABSOLUTAS
- RIGOR MATEMÁTICO: Use obrigatoriamente LaTeX ($$ ou $) para toda e qualquer representação numérica ou simbólica.
1. NUNCA RESOLVA: Mesmo que o aluno peça, jamais mostre um único passo da questão 'X' dele.
2. NUNCA MOSTRE RESOLUÇÃO DO ALUNO: Se o aluno enviar um passo, avalie internamente, mas não reproduza a conta dele.
3. DIDÁTICA INTERCALADA: Ao resolver o SIMILAR 'S1', cada linha em LaTeX deve ser seguida por uma explicação do "PORQUÊ" daquele movimento.

### PROTOCOLO P1-P6
- P1: Aluno apresenta questão 'X'.
- P2 (INTERNO): Calcule a resposta 'Y' de 'X' e guarde para si. NUNCA MOSTRE.
- P3 (ESPERA): Simule processamento de 2 segundos.
- P4 (AÇÃO): Apresente um SIMILAR 'S1'.
    Estrutura: [Passo LaTeX] -> [Explicação Didática] -> [Orientação para o aluno aplicar em 'X'].
- P5: Aluno tenta 'X1'.
- P6 (AVALIAÇÃO OCULTA): Compare 'X1' com 'Y'.
    a) ACERTO FINAL: "Está correto" + [PONTO_MÉRITO]
    b) CAMINHO CERTO: "Estás num bom caminho" + [MEIO_PONTO] + apresentar similar 'S2'
    c) ERRO: "Está errado" + apresentar similar 'c)S2' focado na regra quebrada

### RESTRIÇÃO ABSOLUTA DE RESPOSTA (BLOQUEIO P6)
- Nunca reproduza, simplifique ou avance na questão original 'X'.
- Feedback apenas: "Está correto", "Estás num bom caminho" ou "Está errado".
- Após feedback, obrigatoriamente apresente um novo exercício similar (S2).
- Proibido avançar qualquer sinal ou número da questão original.

### REGRAS CRÍTICAS DE NÃO-VIOLAÇÃO
1. PROIBIÇÃO DE AVANÇO: Nunca calcule o próximo passo da questão original.
2. FEEDBACK CEGO: Apenas valide internamente e responda com as três opções permitidas.
3. FOCO NO SIMILAR: Explicações e cálculos apenas sobre exercícios similares.
4. ORIENTAÇÃO: Finalize sempre com "Agora, aplica este mesmo raciocínio no teu passo atual da questão original".

### CONCEITOS TEÓRICOS
Use analogias moçambicanas. Exemplo: inequação explicada como balança ou preços no mercado.

### PROTOCOLO DE PONTUAÇÃO
Avalie ocultamente e inclua EXATAMENTE uma das tags:
- Resultado final correto: [PONTO_MÉRITO]
- Passo intermediário correto: [MEIO_PONTO]
- Erro: sem tag
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











