import streamlit as st
from groq import Groq
import time

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="TutorIntEqQuadratica", layout="wide")

# 2. INTERFACE E ESTILO (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Algerian&display=swap');
    
    /* Barra de rolagem robusta para toque */
    ::-webkit-scrollbar { width: 35px; }
    ::-webkit-scrollbar-track { background: #f1f1f1; }
    ::-webkit-scrollbar-thumb { background: #2c3e50; border-radius: 10px; border: 3px solid #f1f1f1; }

    /* Estilização de texto e fórmulas */
    .stMarkdown p, .katex { font-size: 1.2rem !important; color: #1e293b; }
    
    /* Assinatura Fixa */
    .signature-footer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background-color: white; padding: 10px 0;
        text-align: center; z-index: 1000;
        font-family: 'Algerian', serif; font-size: 18px;
        border-top: 2px solid #000;
    }
    
    header {visibility: hidden;}
    .main-container { padding-bottom: 100px; }
    </style>
    <div class="signature-footer">HBM - Mediador Didático</div>
    """, unsafe_allow_html=True)

# 3. ESTADO DA SESSÃO
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pontos" not in st.session_state:
    st.session_state.pontos = 0
if "bloqueado" not in st.session_state:
    st.session_state.bloqueado = False # Impede novas questões antes de fechar a atual

# Conexão API
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Erro: Chave API não configurada corretamente nos Secrets.")
    st.stop()

# 4. TÍTULO E PLACAR
st.title("🎓 Tutor Inteligente: Mediador IntMatemático")
st.sidebar.metric("Evolução Acumulada", f"{st.session_state.pontos} pts")
st.sidebar.info("Áreas: Conjuntos, Álgebra, Geometria, Estatística, Cálculo e mais.")

# 5. PROMPT DE SISTEMA (O REGULAMENTO INVIOLÁVEL)
PROMPT_SISTEMA = """
VOCÊ É O PROFESSOR (HBM). VOCÊ OPERA SOB AS LEIS DO CONSTRUTIVISMO E ZDP.
MISSÃO: Nunca resolver a questão 'X' do aluno. Mediar a construção do conhecimento.

REGRAS INVIOLÁVEIS:
1. ESCOPO: Matemática total (Cálculo, Álgebra Linear, Geometria, Estatística, etc.). Recuse qualquer tema fora da matemática.
2. P2 (RESOLUÇÃO OCULTA): Resolva a questão 'X' internamente apenas para obter o resultado 'Y'. JAMAIS mostre isso ao aluno.
3. P3 & P4 (EXEMPLO ESPELHO): 
   - Busque uma questão similar 'S1'. 
   - Apresente a resolução de 'S1' detalhada em LaTeX, passo a passo.
   - Instrua o aluno: "Agora, aplique esta mesma lógica à sua questão original 'X'".
4. P6 (AVALIAÇÃO DE INTERVENÇÕES X1, X2, Xn):
   - Se intervenção == Y (Resultado Final): Diga "Está correto", atribua [PONTO_MÉRITO].
   - Se intervenção == Caminho Correto mas Incompleto: Diga "Estás num bom caminho", atribua metade de [PONTO_MÉRITO] e apresente um novo exemplo similar 'S2' para o próximo passo.
   - Se intervenção != Caminho Correto: Diga "Está Errado", não dê pontos, e apresente um novo exemplo 'cS2' corrigindo a lógica.
5. TEORIA E CONCEITOS: Use analogias moçambicanas (machambas, mangas, mercados, castanhas). Se a definição do aluno tiver 95% de correção face ao conceito acadêmico, atribua [PONTO_MÉRITO].
6. BLOQUEIO: Não aceite novas questões 'Z' enquanto a questão 'X' não for concluída com sucesso ou o chat limpo.
7. FORMATAÇÃO: Use sempre LaTeX para matemática. Seja encorajador mas rigoroso.
"""

# 6. EXIBIÇÃO DO CHAT
for msg in st.session_state.chat_history:
    avatar = "🎓" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# 7. LOGICA DE INTERAÇÃO
entrada = st.chat_input("Envie sua questão ou resposta...")

if entrada:
    # Adiciona fala do aluno
    st.session_state.chat_history.append({"role": "user", "content": entrada})
    with st.chat_message("user", avatar="👤"):
        st.markdown(entrada)

    with st.chat_message("assistant", avatar="🎓"):
        with st.status("Processando mediação didática...", expanded=True) as status:
            # P3: Simulação de busca pedagógica
            st.write("🔍 Analisando lógica da sua questão...")
            time.sleep(1.5)
            st.write("📂 Buscando exercício similar (S1) na base de dados...")
            time.sleep(1.5)
            st.write("✍️ Preparando explicação passo a passo...")
            time.sleep(1.0)
            status.update(label="Processamento Concluído!", state="complete", expanded=False)

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": PROMPT_SISTEMA}] + st.session_state.chat_history,
                temperature=0.0
            )
            feedback = response.choices[0].message.content

            # Gestão de Pontos (Sinalizadores do Sistema)
            if "[PONTO_MÉRITO]" in feedback:
                # Se for metade do ponto (caminho certo)
                if "Estás num bom caminho" in feedback:
                    st.session_state.pontos += 10
                    feedback = feedback.replace("[PONTO_MÉRITO]", "\n\n✨ **+10 pontos (Bom caminho!)**")
                else:
                    st.session_state.pontos += 20
                    feedback = feedback.replace("[PONTO_MÉRITO]", "\n\n🏆 **+20 pontos (Domínio Completo!)**")

            st.markdown(feedback)
            st.session_state.chat_history.append({"role": "assistant", "content": feedback})
            st.rerun()

        except Exception as e:
            st.error(f"Erro na conexão com o cérebro da IA: {e}")

# 8. BOTÃO DE RESET (PARA NOVAS QUESTÕES)
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reiniciar Professor (Limpar Chat)"):
    st.session_state.chat_history = []
    st.session_state.pontos = 0
    st.rerun()
