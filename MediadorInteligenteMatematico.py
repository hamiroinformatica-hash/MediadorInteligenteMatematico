import streamlit as st
from groq import Groq
import time

# --- 1. CONFIGURAÇÃO VISUAL (Foco em Organização Vertical) ---
st.set_page_config(page_title="Mediador IntMatemático HBM", layout="wide")
st.markdown("""
    <style>
    /* Forçar quebra de linha em fórmulas LaTeX longas */
    .katex-display { overflow-x: auto; overflow-y: hidden; padding: 10px 0; }
    ::-webkit-scrollbar { width: 35px !important; }
    ::-webkit-scrollbar-thumb { background: #000; border-radius: 10px; }
    .signature-footer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: white; text-align: center; font-family: 'Algerian', serif;
        font-size: 16px; border-top: 2px solid #333; z-index: 1000; padding: 10px;
    }
    </style>
    <div class="signature-footer">HBM - Mediação Didática e Visual</div>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pontos" not in st.session_state:
    st.session_state.pontos = 0

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. PROMPT DE SISTEMA (Foco em Formatação Vertical e Rigor P1-P6) ---
PROMPT_SISTEMA_V3 = """
VOCÊ É O MEDIADOR HBM. VOCÊ DEVE SER UM MESTRE NA ORGANIZAÇÃO VISUAL.

### REGRAS DE FORMATAÇÃO MATEMÁTICA (CRÍTICO):
1. **Verticalidade Obrigatória:** NUNCA escreva equações na mesma linha. Use duas quebras de linha entre cada passo.
2. **Símbolos de Ligação:** Use obrigatoriamente o símbolo de implicação $\\implies$ entre os passos para mostrar a evolução lógica.
3. **Bloco LaTeX:** Prefira o uso de blocos centralizados com `$$` para que o aluno veja a conta de forma destacada.

### PROTOCOLO PEDAGÓGICO REFORÇADO:
- **Silêncio sobre 'X':** Não repita, não simplifique e não mencione os termos da equação do aluno na sua resposta.
- **Feedback Seco:** Diga apenas "Está correto", "Estás num bom caminho" ou "Está errado". 
- **Exemplo Similar Resolvido:** Após o feedback, você deve apresentar a resolução de um similar 'S2' EXATAMENTE assim:
  $$ Passo 1 $$
  $$\\implies Passo 2 $$
  $$\\implies Resultado Final $$
- **Analogias:** Use o contexto de Moçambique (vendedores, machambas) apenas em texto curto e motivador.

### EXEMPLO DE RESPOSTA ESPERADA:
"Estás num bom caminho. Para continuar, observe como resolvemos este caso similar:
$$ 3x - 5 = 10 $$
$$\\implies 3x = 10 + 5 $$
$$\\implies 3x = 15 $$
$$\\implies x = \\frac{15}{3} = 5 $$
Agora aplique este raciocínio ao seu passo."
"""

# --- 3. INTERFACE E LÓGICA ---
st.title("🎓 Mediador IntMatemático")
st.write(f"📊 **Pontuação:** {st.session_state.pontos}")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

entrada = st.chat_input("Digite sua intervenção...")

if entrada:
    st.session_state.chat_history.append({"role": "user", "content": entrada})
    with st.chat_message("user", avatar="👤"):
        st.markdown(entrada)

    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("Organizando mediação..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": PROMPT_SISTEMA_V3}] + st.session_state.chat_history,
                    temperature=0.0
                )
                
                feedback = response.choices[0].message.content
                
                # Gamificação
                if "[PONTO_MÉRITO]" in feedback:
                    st.session_state.pontos += 20
                    feedback = feedback.replace("[PONTO_MÉRITO]", "\n\n✨ **+20 pontos!**")
                elif "[MEIO_PONTO]" in feedback:
                    st.session_state.pontos += 10
                    feedback = feedback.replace("[MEIO_PONTO]", "\n\n🚀 **+10 pontos!**")

                st.markdown(feedback)
                st.session_state.chat_history.append({"role": "assistant", "content": feedback})
                st.rerun()

            except Exception:
                st.warning("Aguardando estabilidade da conexão...")
                time.sleep(2)
                st.rerun()

if st.sidebar.button("🔄 Reiniciar"):
    st.session_state.chat_history = []
    st.session_state.pontos = 0
    st.rerun()
