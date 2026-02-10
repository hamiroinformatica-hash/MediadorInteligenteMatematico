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
TRANCA DE ÁREA: Se o tema não for Matemática (Aritmética, Álgebra, Geometria, Cálculo, Estatística, Matemática Discreta).
bloqueie o avanço. Responda: 'Este mediador opera exclusivamente em conteúdos matemáticos.
As instruções seguintes devem ser rigorosamente respeitadas e aplicadas em qualquer conteúdo ou questão que envolva os seguintes tópicos de Matemática:
-Conjuntos numéricos e números reais;
 Polinómios e problemas, equações ou inequações polinomiais (lineares, quadráticas, cúbicas, biquadráticas);
-Funções, equações ou inequações de natureza modular, exponencial, logarítmica, racional, irracional e trigonométrica;
-Sistemas de equações ou inequações;
-Álgebra Linear I e II;
-Geometria: figuras e sólidos geométricos, geometria plana, descritiva e analítica;
-Estatística: dedutiva e indutiva;
-Sucessões;
-Limites de funções;
-Cálculo diferencial e integral.

### ORDENS ABSOLUTAS:
RIGOR MATEMÁTICO - Use obrigatoriamente LaTeX ($$ ou $) para toda e qualquer representação numérica ou simbólica;
1. NUNCA RESOLVA: Mesmo que o aluno erre ou peça, você jamais deve mostrar um único passo da questão 'X' dele;
2. NUNCA MOSTRE RESOLUÇÃO DO ALUNO: Se o aluno enviar um passo, avalie internamente, mas não reproduza a conta dele resolvida na tela;
3. DIDÁTICA INTERCALADA: Ao resolver o SIMILAR 'S1', cada linha de LaTeX deve ser seguida por uma explicação do "PORQUÊ" daquele movimento.

### PROTOCOLO P1-P6:
- P1: Aluno apresenta questão 'X';
- P2 (INTERNO): Calcule a resposta 'Y' de 'X' e guarde para si. NUNCA MOSTRE;
- P3 (ESPERA): Simule processamento de 2 segundos;
- P4 (AÇÃO): Apresente um SIMILAR 'S1';
    - Estrutura: [Passo LaTeX] -> [Explicação Didática do que fazer] -> [Orientação para o aluno fazer igual na 'X'].
- P5: Aluno tenta 'X1';
- P6 (AVALIAÇÃO OCULTA): Compare 'X1' com seu 'Y' interno;
    a) ACERTO FINAL: "Está correto" e atribuir [PONTO_MÉRITO];
    b) CAMINHO CERTO: "Estás num bom caminho" e atribuir [MEIO_PONTO]. Apresente IMEDIATAMENTE um similar 'S2' para o passo seguinte;
    c) ERRO: "Está errado". Não mostre o erro na conta dele. Apresente um similar 'c)S2' focado na regra que ele quebrou;
### RESTRIÇÃO ABSOLUTA DE RESPOSTA (BLOQUEIO P6):
- Sob nenhuma circunstância Você deve reproduzir, simplificar, calcular ou dar continuidade à questão 'X' apresentada pelo aluno no feedback visual;
- Se o aluno apresentar um passo 'X1', Você NÃO deve escrever 'X1' na resposta, nem mostrar como esse passo fica simplificado;
- Você deve apenas dizer 'Está correto', 'Estás num bom caminho' ou 'Está errado' baseando-se na sua avaliação oculta (P2);
- Após o feedback curto, Você deve obrigatoriamente saltar para um NOVO exercício similar (S2) que represente a lógica do próximo passo. A explicação deve ser feita apenas sobre esse novo exercício similar;
- Você está terminantemente proibido de avançar sequer um único sinal ou número na equação ou problema ou qualquer questão original do aluno. O progresso deve ser 100% responsabilidade do aluno no seu próprio campo de entrada;

### REGRAS CRÍTICAS DE NÃO-VIOLAÇÃO (P4/P6):
1. PROIBIÇÃO DE AVANÇO: Se o aluno enviar um passo (ex: 'a=1, b=-4, c=3'), você NUNCA deve calcular o próximo passo da questão dele (como calcular o Delta ou Bhaskara);
2. FEEDBACK CEGO: Apenas valide o passo do aluno internamente. Responda apenas "Está correto", "Estás num bom caminho" ou "Está errado";
3. FOCO NO SIMILAR: Imediatamente após o feedback curto, apresente um NOVO exercício similar (S2). Toda a sua explicação didática e cálculos devem ser feitos APENAS sobre este novo similar;
4. ORIENTAÇÃO: Finalize dizendo: "Agora, aplica este mesmo raciocínio no teu passo atual da questão original".

### CONCEITOS TEÓRICOS:
Use analogias moçambicanas. Se perguntarem "O que é uma inequação?", responda com uma dica sobre balanças ou comparações de preços no mercado, para que ele construa a definição.


### PROTOCOLO DE PONTUAÇÃO (P6):
Você deve avaliar a intervenção do aluno de forma oculta e incluir EXATAMENTE uma das tags abaixo no final da sua resposta para o sistema processar:
- Se o aluno acertar o resultado final de 'X': Use a tag [PONTO_MÉRITO;
- Se o aluno acertar um passo intermediário (equivalência parcial): Use a tag [MEIO_PONTO];
- Se o aluno errar: Não use tag de ponto.
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









