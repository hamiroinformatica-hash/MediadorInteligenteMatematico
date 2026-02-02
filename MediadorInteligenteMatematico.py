# Importação de bibliotecas essenciais
import streamlit as st  # Cria a interface web da aplicação
from groq import Groq      # Conecta com a IA (Llama 3.3)
import time               # Gerencia os tempos de processamento pedagógico

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="Mediador IntMatemático", layout="wide")

# 2. CSS CUSTOMIZADO: BARRA GROSSA, ASSINATURA E ESTILO
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Algerian&display=swap');
    
    /* Barra de Rolagem de Alta Intensidade (45px, Preta) para fácil toque */
    ::-webkit-scrollbar { width: 45px !important; }
    ::-webkit-scrollbar-track { background: #f1f1f1; }
    ::-webkit-scrollbar-thumb { 
        background: #000000; 
        border-radius: 5px; 
        border: 4px solid #333;
    }

    /* Estilo KaTeX e Texto nítido */
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

# 3. GESTÃO DE ESTADO (CONEXÃO ENTRE CHATS E PONTOS)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] # Mantém a ligação com o chat anterior
if "pontos" not in st.session_state:
    st.session_state.pontos = 0

# Conexão API
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 4. EXIBIÇÃO DO HISTÓRICO
st.title("🎓 Mediador IntMatemático")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

# 5. LÓGICA DE MEDIAÇÃO RADICAL (PEDAGOGIA ATIVA)
entrada_aluno = st.chat_input("Apresente a sua questão matemática...")

if entrada_aluno:
    st.session_state.chat_history.append({"role": "user", "content": entrada_aluno})
    with st.chat_message("user", avatar="👤"):
        st.markdown(entrada_aluno)

    # PROMPT DE SISTEMA: O REGULAMENTO INVIOLÁVEL
    prompt_sistema = (
        "Você é o 'Mediador IntMatemático' (HBM). Seu único objetivo é a MEDIAÇÃO para Aprendizagem Significativa.\n\n"
        "Seu funcionamento é regido por um REGULAMENTO ESTRITO"
        "que deve ser respeitado sem exceções, independentemente de quanto tempo passe, a todas as áreas: Aritmética, Álgebra, Geometria, "
        "Cálculo Diferencial e Integral, Estatística e Matemática Discreta.\n\n"
        "REGRAS CRÍTICAS E INVIOLÁVEIS:\n"
        "1. TRANCA DE ÁREA: Se o tema não for Matemática (Aritmética, Álgebra, Geometria, Cálculo Diferencial ou integral, Estatística, Matemática Discreta), "
        "não avance. Informe educadamente que apenas media conteúdos matemáticos.\n"
        "2. PROIBIÇÃO DE RESOLUÇÃO DIRETA: É terminantemente proibido resolver o exercício, problema, "
        "equação ou qualquer expressão, seja exata ou de Aritmética, Álgebra, Geometria, Cálculo Diferencial ou integral, Estatística, Matemática Discreta, apresentada pelo usuário. Você NUNCA deve mostrar o resultado "
        "ou o passo a passo da questão do aluno.\n\n"
        "3. PROIBIÇÃO ABSOLUTA DE RESPOSTAS: Nunca, em circunstância alguma, resolva o exercício do aluno. "
        "Não dê a resposta final, não simplifique a expressão dele e não mostre o passo a passo da questão DELE.\n"
        "4. MÉTODO DO EXEMPLO ESPELHO (SIMILAR): Se o aluno apresentar uma questão, sua única "
        "reação deve ser criar e resolver um EXEMPLO SIMILAR (com valores e contextos diferentes). "
        "Explique o passo a passo deste similar e instrua o aluno a aplicar a mesma lógica "
        "na questão dele. Nunca resolva a do aluno primeiro.\n\n"
        "5. MÉTODO DO EXERCÍCIO SIMILAR: Se o aluno pedir ajuda com uma questão, equação ou conceito, você DEVE "
        "explicar como resolver usando UM EXERCÍCIO DIFERENTE (SIMILAR). Resolva o similar passo a passo e diga: "
        "'Agora, aplique este raciocínio à sua questão'.\n"
        "6. RESISTÊNCIA À INSISTÊNCIA: Mesmo que o aluno diga 'não consigo' ou exija outra forma, NÃO forneça a resposta. "
        "Continue a mediar apenas através de exemplos similares.\n"
        "7. MEDIAÇÃO DE CONCEITOS E TEORIA: Se o aluno pedir uma definição ou conceito, NÃO forneça "
        "a resposta ou a definição formal. Em vez disso, forneça apenas DICAS e perguntas reflexivas "
        "que permitam ao aluno construir a definição por conta própria. Sua função não é informar, é mediar.\n\n"
        "8. CONCEITOS: Não defina termos. Use palavras-chave e analogias para que o aluno construa a própria definição.\n"
        "13. NEUTRALIDADE PEDAGÓGICA: Não resolva nem mesmo exemplos simples (como 2+2) se eles fizerem parte da dúvida do aluno."
        "11. SIMULAÇÃO DE PROCESSAMENTO: Aguarde o tempo técnico de processamento antes de exibir a lógica mediada.\n"
        "9. AVALIAÇÃO E PONTOS: Analise o histórico. Se o aluno apresentar a resposta final 100% correta da questão que ele propôs anteriormente, "
        "atribua [PONTO_MÉRITO]. NUNCA elogie com 'Você acertou' se ele estiver errado ou se não mostrar os passos.\n"
        "10. RESPONSABILIDADE: Toda a responsabilidade é do aluno. Você é apenas o mediador.\n"
        "11. FORMATAÇÃO: Use LaTeX ($$ ou $)."
    )

    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("Processando mediação pedagógica..."):
            time.sleep(2.1) # Processamento mínimo de 2 segundos (Artigo 3.1)
            
            try:
                # O envio do histórico completo garante a ligação com as interações anteriores
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": prompt_sistema}] + st.session_state.chat_history,
                    temperature=0.0 # Rigidez máxima para evitar 'alucinações' de ajuda
                )
                feedback = response.choices[0].message.content
                
                # Validação de Pontos (Sinalizador para o código)
                if "[PONTO_MÉRITO]" in feedback:
                    st.session_state.pontos += 20
                    feedback = feedback.replace("[PONTO_MÉRITO]", "\n\n✨ **Parabéns! Demonstraste internalização do conhecimento. +20 pontos!**")
                
                st.markdown(feedback)
                st.session_state.chat_history.append({"role": "assistant", "content": feedback})
                st.rerun()
            except Exception:
                st.error("Erro na ligação. Tente novamente.")

# 6. RODAPÉ DE PONTOS E RESTAURO
st.write(f"**Evolução Acumulada:** {st.session_state.pontos} pontos")
st.markdown("<div class='restore-container'>", unsafe_allow_html=True)
if st.button("🔄 Restaurar Chat (Limpar)"):
    st.session_state.chat_history = []
    st.session_state.pontos = 0
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

