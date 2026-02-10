import streamlit as st
from groq import Groq
import time

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="Mediador IntMatemático", layout="wide")

# 2. ESTILO E ASSINATURA (HBM)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Algerian&display=swap');
    ::-webkit-scrollbar { width: 45px !important; }
    ::-webkit-scrollbar-track { background: #f1f1f1; }
    ::-webkit-scrollbar-thumb { background: #000; border-radius: 5px; border: 4px solid #333; }
    .stMarkdown p, .katex { font-size: 1.25rem !important; color: #1a1a1a; }
    header {visibility: hidden;} footer {visibility: hidden;}
    .signature-footer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background-color: rgba(255, 255, 255, 0.98);
        padding: 8px 0; text-align: center; z-index: 999;
        font-family: 'Algerian', serif; font-size: 17px;
        color: #1e293b; border-top: 1px solid #ddd;
    }
    .restore-container { display: flex; justify-content: center; padding-bottom: 110px; }
    </style>
    <div class="signature-footer">HBM</div>
    """, unsafe_allow_html=True)

# 3. GESTÃO DE ESTADO E PERSISTÊNCIA
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pontos" not in st.session_state:
    st.session_state.pontos = 0

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 4. TÍTULO E EXIBIÇÃO
st.title("🎓 Mediador IntMatemático (HBM)")
st.subheader("Foco em Construtivismo e ZDP")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

# 5. PROTOCOLO DE MEDIAÇÃO DIDÁTICA (LÓGICA P1-P6)
entrada_aluno = st.chat_input("Apresente a sua questão matemática...")

if entrada_aluno:
    # Registra a entrada do aluno (P1 ou P5)
    st.session_state.chat_history.append({"role": "user", "content": entrada_aluno})
    with st.chat_message("user", avatar="👤"):
        st.markdown(entrada_aluno)

    # PROMPT SISTÊMICO: O CÉREBRO DO PROFESSOR
    prompt_sistema = (
        "Você é o 'Mediador IntMatemático' (HBM). Você opera sob o paradigma Construtivista e a Zona de Desenvolvimento Proximal (ZDP).\n\n"
        "### PROTOCOLO DE OPERAÇÃO OBRIGATÓRIO:\n"
        "1. **P2 (Cálculo Oculto):** Ao receber a questão 'X', resolva-a internamente para encontrar a solução 'Y'. NUNCA mostre 'X' ou 'Y' ao aluno.\n"
        "2. **P3 & P4 (Desvio Cognitivo):** Apresente uma questão similar 'S1'. Explique a resolução de 'S1' passo-a-passo com LaTeX e diga: 'Aplique esta lógica à sua questão X'.\n"
        "3. **P5 & P6 (Avaliação de Intervenção):** Ao receber uma intervenção 'X1':\n"
        "   - Realize avaliação oculta: 'X1' é matematicamente equivalente à questão original ou ao resultado 'Y'?\n"
        "   - **Caso (a) - Sucesso Final:** Se 'X1' == 'Y', diga 'Está correto' e atribua obrigatoriamente [PONTO_MÉRITO].\n"
        "   - **Caso (b) - Caminho Parcial:** Se 'X1' for equivalente mas incompleto, diga 'Estás num bom caminho', atribua [METADE_MÉRITO] e apresente IMEDIATAMENTE um novo similar 'S2' para o próximo passo.\n"
        "   - **Caso (c) - Erro:** Se 'X1' não for equivalente, diga 'Está errado' (sem pontos) e apresente um novo similar 'S2_Erro' focado na falha lógica cometida.\n"
        "4. **MEDIAÇÃO TEÓRICA:** Para conceitos, use analogias moçambicanas (machambas, mercados, frutas como manga/castanha). Atribua [PONTO_MÉRITO] apenas se a definição do aluno estiver 95% correta.\n"
        "5. **RESTRIÇÕES:** Não responda nada fora de Matemática. Não aceite novas questões até concluir a atual (ou o aluno limpar o chat).\n"
        "6. **ESTILO:** Trate o usuário como 'Aluno' e você como 'Professor'. Use LaTeX ($$)."
    )

    with st.chat_message("assistant", avatar="🎓"):
        status_placeholder = st.empty()
        with st.spinner("Professor a processar mediação pedagógica..."):
            # P3: Simulação de processamento técnico para busca de similar
            time.sleep(2.8) 
            
            try:
                # O histórico completo garante que o professor lembre da questão X original (P1)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": prompt_sistema}] + st.session_state.chat_history,
                    temperature=0.1
                )
                feedback = response.choices[0].message.content
                
                # Processamento de Pontuação no Backend do App
                if "[PONTO_MÉRITO]" in feedback:
                    st.session_state.pontos += 20
                    feedback = feedback.replace("[PONTO_MÉRITO]", "\n\n✨ **Parabéns! Alcançaste a meta. +20 pontos de mérito!**")
                elif "[METADE_MÉRITO]" in feedback:
                    st.session_state.pontos += 10
                    feedback = feedback.replace("[METADE_MÉRITO]", "\n\n📈 **Boa evolução! +10 pontos (Metade do mérito).**")
                
                st.markdown(feedback)
                st.session_state.chat_history.append({"role": "assistant", "content": feedback})
                st.rerun()
            except Exception as e:
                st.error("Erro na comunicação com o servidor. Tente novamente.")

# 6. RODAPÉ DE PONTOS E REINICIALIZAÇÃO
st.write(f"**Evolução Acumulada do Aluno:** {st.session_state.pontos} pontos")
st.markdown("<div class='restore-container'>", unsafe_allow_html=True)
if st.button("🔄 Reiniciar Professor (Limpar e Nova Questão)"):
    st.session_state.chat_history = []
    st.session_state.pontos = 0
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
