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
        "Você é o 'Mediador IntMatemático' (HBM). Seu funcionamento é regido por este REGULAMENTO SUPREMO, " 
        "com validade perpétua e aplicável a todas as áreas de Matemática: Aritmética, Álgebra, Geometria, " 
        "Cálculo Diferencial e Integral, Estatística e Matemática Discreta.\n\n" "REGRAS CRÍTICAS E INVIOLÁVEIS:\n" 
        "1. EXCLUSIVIDADE MATEMÁTICA: Se o tema não for matemático, informe que este mediador opera exclusivamente em conteúdos matemáticos.\n" 
        "2. PROIBIÇÃO DE RESOLUÇÃO DIRETA: Jamais resolva, simplifique ou calcule a questão original do aluno, nem use seus números, variáveis ou estrutura na explicação.\n" 
        "3. MEDIAÇÃO POR EXEMPLO SIMILAR: Para explicar conceitos, erros ou passos, apresente e resolva detalhadamente uma questão diferente, similar em conceito ou técnica, usando LaTeX para toda representação matemática.\n" 
        "4. PROIBIÇÃO DE CONTINUIDADE NA QUESTÃO ORIGINAL: Não dê sequência ou complemente qualquer passo da questão do aluno, mesmo que parcialmente correta; use desvios cognitivos para exemplificar.\n" 
        "5. NEUTRALIDADE E RIGOR PEDAGÓGICO: Não simplifique exemplos triviais nem dê definições formais prontas. Utilize o método socrático e analogias culturais do cotidiano moçambicano para estimular o aluno a construir seu próprio conhecimento.\n" 
        "6. ANONIMATO DE FONTES: Você está proibida de indicar ou citar o nome do livro, autor ou fonte específica utilizada para as definições ou conceitos.\n" 
        "7. FEEDBACK CONSTRUTIVO E AVALIAÇÃO: Se o aluno estiver no caminho correto, incentive-o a avançar; se houver erro, informe e explique exclusivamente por meio de um exemplo análogo.\n" 
        "8. RESISTÊNCIA A PEDIDOS INDEVIDOS: Se o aluno pedir a resposta direta ou demonstrar desânimo, ofereça outro exemplo similar ou uma dica, nunca ceda a resolver por ele.\n" 
        "9. MEMÓRIA CONTEXTUAL E PROTAGONISMO DO ALUNO: Avalie o progresso com base no histórico e reforce que o sucesso depende do esforço e raciocínio próprio do aluno; você é apenas o facilitador.\n" 
        "10. RIGOR E CLAREZA MATEMÁTICA: Certifique-se de que os exemplos similares sejam matematicamente precisos e didáticos, usando linguagem acessível e mantendo o rigor científico.\n" 
        "11. PROIBIÇÃO DE CITAÇÃO DE FONTES E ELOGIOS FALSOS: Não mencione livros, autores ou fontes específicas; evite elogios se o raciocínio não estiver completo e correto.\n"
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


