import streamlit as st
from groq import Groq
import time

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="Mediador IntMatemático", layout="wide")

# 2. CSS: BARRA DE ROLAGEM PRETA GROSSA, ASSINATURA E FORMATAÇÃO
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Algerian&display=swap');
    
    /* Barra de Rolagem de Alta Intensidade (45px, Preta) */
    ::-webkit-scrollbar { width: 45px !important; }
    ::-webkit-scrollbar-track { background: #f1f1f1; }
    ::-webkit-scrollbar-thumb { 
        background: #000000; 
        border-radius: 5px; 
        border: 4px solid #333;
    }

    /* Estilo para fórmulas LaTeX e Texto nítido */
    .stMarkdown p, .katex {
        font-size: 1.25rem !important;
        color: #1a1a1a;
    }

    header {visibility: hidden;} footer {visibility: hidden;}
    
    .signature-footer {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background-color: rgba(255, 255, 255, 0.98);
        padding: 8px 0;
        text-align: center;
        z-index: 999;
        font-family: 'Algerian', serif;
        font-size: 17px;
        color: #1e293b;
        border-top: 1px solid #ddd;
    }
    .restore-container { display: flex; justify-content: center; padding-bottom: 110px; }
    </style>
    <div class="signature-footer">HBM</div>
    """, unsafe_allow_html=True)

# 3. GESTÃO DE ESTADO (MEMÓRIA CONTEXTUAL)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pontos" not in st.session_state:
    st.session_state.pontos = 0

# Conexão API
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 4. EXIBIÇÃO DO HISTÓRICO
st.title("🎓 Mediador IntMatemático")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

# 5. LÓGICA DE MEDIAÇÃO COM REGRAS INTENSIFICADAS
entrada_aluno = st.chat_input("Insira sua questão aqui...")

if entrada_aluno:
    st.session_state.chat_history.append({"role": "user", "content": entrada_aluno})
    with st.chat_message("user", avatar="👤"):
        st.markdown(entrada_aluno)

    # PROMPT BLINDADO - REGULAMENTO DE TOLERÂNCIA ZERO
    prompt_sistema = (
        "Você é o 'Mediador IntMatemático' (HBM). Seu comportamento deve seguir estas regras ABSOLUTAS:\n\n"
        "1. TRANCA DE CONTEÚDO: Se o aluno apresentar qualquer questão que não seja de Matemática "
        "(Aritmética, Álgebra, Geometria, Análise e Cálculo, Estatística e Probabilidade ou Matemática Discreta), "
        "TRANQUE O AVANÇO. Responda educadamente que apenas media conteúdos matemáticos e não avance.\n"
        "2. PROIBIÇÃO RADICAL DE RESPOSTA: Nunca resolva exercícios, problemas, equações ou simplificações do aluno. "
        "Mesmo que ele diga 'não consigo', mesmo que peça 'outra forma', mesmo que exija. A responsabilidade é 100% dele.\n"
        "3. AVALIAÇÃO E CRÍTICA: Se o aluno der uma resposta sem passos ou por coincidência, não elogie. Avalie logicamente, "
        "critique a falta de processo e sugira caminhos. Jamais diga 'Você acertou' se houver erro ou falta de justificativa.\n"
        "4. MÉTODO DE EXEMPLO SIMILAR: Para qualquer desafio proposto, você deve criar um EXEMPLO SIMILAR DIFERENTE. "
        "Explique o passo a passo DESTE exemplo similar em LaTeX e oriente o aluno a fazer o mesmo com o dele.\n"
        "5. CONCEITOS E DEFINIÇÕES: Se solicitado um conceito, use apenas palavras-chave e analogias. Nunca dê a definição pronta.\n"
        "6. CONEXÃO E PONTUAÇÃO: Leia o histórico. Só atribua [PONTO_MÉRITO] se o aluno apresentar o resultado correto "
        "da questão que ele mesmo propôs anteriormente, demonstrando evolução e autonomia.\n"
        "7. APRENDIZAGEM ATIVA: Baseie-se na construção ativa do conhecimento. O aluno deve relacionar o novo com o que já sabe.\n"
        "8. FORMATAÇÃO: Use LaTeX profissional ($$ ou $)."
    )

    with st.chat_message("assistant", avatar="🎓"):
        # Processamento de 3 segundos (Regulamento Intensificado)
        with st.spinner("Processando mediação pedagógica (3s)..."):
            time.sleep(3.0) 
            
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": prompt_sistema}] + st.session_state.chat_history,
                    temperature=0.0
                )
                feedback = response.choices[0].message.content
                
                # Validação de Pontos
                if "[PONTO_MÉRITO]" in feedback:
                    st.session_state.pontos += 20
                    feedback = feedback.replace("[PONTO_MÉRITO]", "\n\n✨ **Evolução confirmada! Demonstraste autonomia e o resultado está correto. +20 pontos!**")
                
                st.markdown(feedback)
                st.session_state.chat_history.append({"role": "assistant", "content": feedback})
                st.rerun()
            except Exception:
                st.error("Erro na mediação. Tente novamente.")

# 6. RODAPÉ E RESTAURO
st.write(f"**Pontuação de Autonomia:** {st.session_state.pontos} pontos")
st.markdown("<div class='restore-container'>", unsafe_allow_html=True)
if st.button("🔄 Restaurar Chat (Limpar)"):
    st.session_state.chat_history = []
    st.session_state.pontos = 0
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
