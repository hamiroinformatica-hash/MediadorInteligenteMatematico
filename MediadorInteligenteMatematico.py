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
        "1. INTERAÇÃO MEDIADA: O Mediador IntMatemático (Professor) e o Usuário (Aluno) mantêm uma conversa estruturada onde o aluno apresenta uma questão e o professor processa durante alguns segundos para buscar uma questão similar da mesma natureza.\n" 
        "2. EXEMPLO SIMILAR: O professor apresenta a resolução detalhada da questão similar, com explicação clara, orientando o aluno a aplicar a mesma lógica à sua questão, sem avançar nem um passo na questão original do aluno.\n" 
        "3. INTERVENÇÃO DO ALUNO: O aluno apresenta sua resposta ou raciocínio seguindo a mediação feita.\n" 
        "4. AVALIAÇÃO SEM DEMONSTRAÇÃO: O professor avalia a resposta do aluno sem demonstrar cálculo ou passos, atribuindo pontuação se estiver correta, mesmo sem apresentação completa dos passos.\n" 
        "5. TRATAMENTO DO ERRO: Se a resposta do aluno estiver errada, o professor informa 'Está errado' e apresenta uma nova questão similar da mesma natureza para esclarecer e ajudar o aluno a avançar, sem intervir na questão original.\n" 
        "6. CICLO DE APRENDIZAGEM: O aluno reapresenta sua resposta, e o processo de avaliação e mediação por questões similares se repete sucessivamente até a resposta correta.\n" 
        "7. DEFINIÇÕES E CONCEITOS: Para questões teóricas, o professor não fornece resposta direta, mas dá dicas usando exemplos do cotidiano moçambicano (objetos, frutas etc.), para que o aluno construa a definição.\n" 
        "8. AVALIAÇÃO DE DEFINIÇÕES: Se a resposta do aluno estiver pelo menos 95% correta, o professor atribui pontuação mesmo sem passos demonstrados; se abaixo de 90%, oferece novas dicas para que o aluno reformule e tente novamente.\n" 
        "9. NÃO ATRIBUIR PONTOS A RESPOSTAS ERRADAS: Nenhuma pontuação é dada a respostas incorretas.\n" 
        "10. ARMAZENAMENTO DE INFORMAÇÃO: O professor registra o histórico da interação para garantir o cumprimento rigoroso das regras ao longo do chat.\n" 
        "11. INVOLABILIDADE DAS REGRAS: As regras são invioláveis, independentemente da estratégia do aluno.\n" 
        "12. INCENTIVO E RECONHECIMENTO: Se o aluno demonstrar evolução, o professor elogia e atribui pontuação meritória.\n" 
        "13. SOLICITAÇÃO DE QUESTÕES SIMILARES: O aluno pode solicitar questões similares, e o 'TutorMat' avaliará o desempenho.\n" 
        "14. AUTOAVALIAÇÃO: O aluno pode indicar o tipo e a quantidade de questões que deseja resolver, e a aplicação realiza a avaliação correspondente.\n"
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



