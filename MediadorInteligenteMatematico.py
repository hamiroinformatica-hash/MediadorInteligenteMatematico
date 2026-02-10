import streamlit as st
from groq import Groq
import time

# 1. CONFIGURAÇÃO DE INTERFACE (Foco em Acessibilidade e Baixo Consumo)
st.set_page_config(page_title="Mediador IntMatemático HBM", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; }
    ::-webkit-scrollbar { width: 35px !important; }
    ::-webkit-scrollbar-thumb { background: #000000; border-radius: 10px; }
    header {visibility: hidden;} footer {visibility: hidden;}
    .signature-footer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: rgba(255,255,255,0.95); padding: 8px; text-align: center;
        font-family: 'Algerian', serif; font-size: 16px;
        border-top: 2px solid #333; z-index: 1000;
    }
    .main-container { padding-bottom: 100px; }
    </style>
    <div class="signature-footer">HBM - Mediador Pedagógico Construtivista</div>
""", unsafe_allow_html=True)

# 2. INICIALIZAÇÃO DE ESTADO
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pontos" not in st.session_state:
    st.session_state.pontos = 0

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. DEFINIÇÃO DO PROMPT MESTRE (AUTOCONTIDO)
# Este prompt explica à IA o significado de P1 a P6 para que ela saiba exatamente o que fazer em cada etapa.
PROMPT_SISTEMA_INTEGRAL = """
Você é o 'Mediador IntMatemático', um professor moçambicano que aplica a Zona de Desenvolvimento Proximal (Vygotsky).
Sua missão é mediar sem nunca resolver a questão original do aluno.

### DEFINIÇÃO DO FLUXO DE TRABALHO (PROTOCOLO P1-P6):
- **P1 (Entrada):** O aluno apresenta uma questão 'X'.
- **P2 (Cálculo Oculto):** Você deve resolver 'X' internamente para encontrar a solução 'Y'. NUNCA mostre 'Y' ou os passos de 'X' ao aluno.
- **P3 (Busca de Similar):** Processe mentalmente uma questão similar 'S1' de mesma natureza.
- **P4 (Mediação Inicial):** Apresente a resolução detalhada de 'S1' (usando LaTeX $$) e instrua o aluno a aplicar a mesma lógica em 'X'. Não avance nenhum passo em 'X'.
- **P5 (Intervenção do Aluno):** O aluno enviará um passo ou tentativa 'X1'.
- **P6 (Avaliação de Equivalência):** Compare 'X1' com o seu cálculo oculto de P2.
    - **Caso A (Correto Final):** Se 'X1' for equivalente a 'Y', diga "Está correto" e use a tag [PONTO_MÉRITO].
    - **Caso B (Caminho Certo/Incompleto):** Se 'X1' for logicamente correto mas parcial, diga "Estás num bom caminho", use a tag [MEIO_PONTO] e apresente IMEDIATAMENTE um novo exercício similar 'S2' focado no próximo passo necessário.
    - **Caso C (Erro):** Se 'X1' for matematicamente inválido ou divergente de P2, diga "Está errado", NÃO dê pontos, e apresente um novo similar 'S2' que trate especificamente da falha cometida.

### REGRAS INVIOLÁVEIS:
1. ÁREA: Exclusivamente Matemática (Conjuntos, Álgebra, Geometria, Cálculo, Estatística, etc.).
2. MÉTODO: Uso obrigatório de Analogias Moçambicanas (mercados, machambas, transporte, frutas locais).
3. RIGOR: Use LaTeX ($$) para toda e qualquer expressão matemática.
4. RESISTÊNCIA: Se o aluno pedir a resposta ou disser "não consigo", ofereça uma nova analogia ou um similar mais simples (andaime pedagógico).
5. TEORIA: Se o aluno pedir conceitos, use perguntas socráticas. Só valide com [PONTO_MÉRITO] se a definição dele atingir 95% de precisão.
6. PERSISTÊNCIA: Não mude de assunto até que 'X' seja resolvido ou o chat seja reiniciado.
"""

# 4. INTERFACE DE USUÁRIO
st.title("🎓 Mediador IntMatemático")
st.write(f"🏆 **Pontuação de Mérito:** {st.session_state.pontos}")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

# 5. LÓGICA DE INTERAÇÃO
entrada_aluno = st.chat_input("Digite sua questão ou passo de resolução...")

if entrada_aluno:
    st.session_state.chat_history.append({"role": "user", "content": entrada_aluno})
    with st.chat_message("user", avatar="👤"):
        st.markdown(entrada_aluno)

    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("Analisando logicamente..."):
            time.sleep(2.5) # Simulação de tempo para P2/P3
            
            try:
                # O sistema envia o prompt com as definições P1-P6 em cada chamada
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": PROMPT_SISTEMA_INTEGRAL}] + st.session_state.chat_history,
                    temperature=0.0 # Rigor máximo
                )
                
                feedback = response.choices[0].message.content
                
                # Tratamento de Gamificação baseado nas tags do prompt
                if "[PONTO_MÉRITO]" in feedback:
                    st.session_state.pontos += 20
                    feedback = feedback.replace("[PONTO_MÉRITO]", "\n\n🌟 **Excelente! Você atingiu o objetivo. +20 pontos!**")
                elif "[MEIO_PONTO]" in feedback:
                    st.session_state.pontos += 10
                    feedback = feedback.replace("[MEIO_PONTO]", "\n\n📈 **Muito bem! Passo correto. +10 pontos!**")
                
                st.markdown(feedback)
                st.session_state.chat_history.append({"role": "assistant", "content": feedback})
                st.rerun()

            except Exception:
                st.error("Erro de conexão. Verifique os dados ou a chave da API.")

# 6. BOTÃO DE REINÍCIO (Fundamental para o protocolo)
if st.sidebar.button("🔄 Reiniciar Professor (Nova Questão)"):
    st.session_state.chat_history = []
    st.session_state.pontos = 0
    st.rerun()
