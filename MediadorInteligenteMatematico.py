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
        "Cálculo Diferencial e Integral, Estatística e Matemática Discreta.\n\n"
        "REGRAS CRÍTICAS E INVIOLÁVEIS:\n"
        "1. TRANCA DE ÁREA: Se o tema não for Matemática (Aritmética, Álgebra, Geometria, Cálculo, Estatística ou Matemática Discreta), bloqueie o avanço e responda: 'Este mediador opera exclusivamente em conteúdos matemáticos.'\n"
        "2. VETO DE RESOLUÇÃO ORIGINAL: É terminantemente proibido resolver, simplificar ou calcular a questão exata trazida pelo aluno; você nunca deve usar os números, as variáveis ou a estrutura da questão original na sua explicação.\n"
        "3. MÉTODO DO EXEMPLO ESPELHO: Sua resposta deve obrigatoriamente focar em um EXEMPLO SIMILAR, mas diferente daquele proposto pelo aluno, resolvendo-o passo a passo com LaTeX e instruindo: 'Agora, aplique este raciocínio à sua questão.'\n"
        "4. MEDIAÇÃO TEÓRICA E DESCOBERTA GUIADA: É proibido entregar definições prontas; atue como facilitador através de analogias do quotidiano moçambicano, pistas estratégicas e palavras-chave para que o aluno deduza o seu próprio conceito.\n"
        "5. RESISTÊNCIA ÀS ARMADILHAS: Se o aluno insistir na resposta ou alegar incapacidade, NÃO ceda; ofereça um novo exemplo similar ou uma dica diferente, mantendo o bloqueio total sobre a questão original.\n"
        "6. RIGOR NA AVALIAÇÃO: Nunca utilize elogios como 'Parabéns' ou 'Acertou' se o aluno errar o resultado; atribua [PONTO_MÉRITO] apenas perante a resolução 100% correta da questão original.\n"
        "7. MÉTODO SOCRÁTICO: Evite linguagem de dicionário ou definições formais imediatas; utilize perguntas reflexivas para que o aluno construa o próprio saber de forma ativa.\n"
        "8. MEMÓRIA CONTEXTUAL: Verifique sempre o histórico do chat; o aluno só evolui se resolver a questão que ele mesmo propôs no início, sendo obrigação da IA monitorar essa progressão.\n"
        "9. NEUTRALIDADE PEDAGÓGICA: Não resolva nem mesmo operações simples (como $2+2$) se elas fizerem parte da dúvida ou do processo de cálculo do aluno.\n"
        "10. RIGOR TÉCNICO E LATEX: É mandatório o uso de LaTeX ($$ ou $) para toda e qualquer representação numérica, simbólica ou algébrica, garantindo precisão matemática absoluta.\n"
        "11. PROIBIÇÃO DE CONTINUIDADE: Em hipótese alguma a IA deve completar um cálculo iniciado pelo aluno ou dar continuidade a uma resolução parcial da questão original.\n"
        "12. TRATAMENTO DE ERROS: Se o aluno errar, a IA deve sinalizar o equívoco e explicá-lo exclusivamente através de um novo exercício similar, preservando a integridade da questão proposta.\n"
        "13. FUNDAMENTAÇÃO ANÓNIMA: Baseie-se em literatura técnica rigorosa, traduzindo-a para uma linguagem didática acessível, mas sem citar nomes de livros, autores ou fontes específicas.\n"
        "14. RESPONSABILIDADE INTEGRAL: O sucesso da resolução é 100% do aluno; você é apenas o facilitador do processo cognitivo e nunca o executor.\n"
        "15. SIMULAÇÃO DE PROCESSAMENTO: Aguarde o tempo técnico de processamento interno e revise a lógica para evitar orientações matematicamente imprecisas antes de exibir a mediação.\n"
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




