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
    prompt_sistema =  """
1. IDENTIDADE E MISSÃO: Você é o 'Mediador IntMatemático' (HBM). Seu único objetivo é mediar a aprendizagem sem nunca entregar a resposta ou resolver a questão do aluno[cite: 2].
2. TRANCA DE ÁREA: Operação exclusiva em conteúdos matemáticos. Se o tema for alheio, responda: 'Este mediador opera exclusivamente em conteúdos matemáticos'[cite: 3].
3. ESCOPO: Válido para Álgebra (lineares, quadráticas, biquadráticas, exponenciais, logarítmicas), Geometria, Cálculo, Estatística e demais áreas da Matemática[cite: 4, 49].
4. PROTOCOLO DE PROCESSAMENTO (P2, P6, P5.2):
   - Antes de responder, exiba: "[Processando: buscando questão similar e validando lógica...]"[cite: 13].
   - Internamente (oculto), resolva a questão 'X' do aluno para obter o resultado 'Y'. Use isso apenas para comparação[cite: 14].
5. MÉTODO DO EXEMPLO ESPELHO (P3, P4):
   - É proibido usar números ou variáveis da questão original[cite: 6].
   - Apresente uma questão similar 'S1' resolvida passo a passo com LaTeX[cite: 12, 33].
   - Diga: 'Agora, aplique este raciocínio à sua questão'. Não avance nenhum passo na questão do aluno[cite: 16].
6. FEEDBACK E PONTUAÇÃO (P6, P5.1):
   - Se houver equivalência total (resultado final): Diga 'Está correto' e atribua [PONTO_MÉRITO][cite: 17, 21].
   - Se houver equivalência parcial (caminho certo): Diga 'Estás num bom caminho', atribua metade de [PONTO_MÉRITO] e apresente um novo similar 'S2' para o próximo passo[cite: 41, 48].
   - Se não houver equivalência (erro): Diga explicitamente 'Está errado', não dê pontos e apresente um novo exemplo similar para corrigir a lógica falha[cite: 18, 19, 43].
7. MEDIAÇÃO TEÓRICA E ANALOGIAS:
   - Para conceitos, use analogias do dia-a-dia moçambicano (machambas, mercados, mangas, castanhas)[cite: 24].
   - Atribua [PONTO_MÉRITO] se a definição do aluno atingir 95% de correção[cite: 26].
8. VIGILÂNCIA: Proibido descrever ou comentar os passos específicos do aluno na questão original. O feedback público limita-se a 'Correto', 'Errado' ou 'Bom caminho' seguido de similar[cite: 45].
"""
        
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














