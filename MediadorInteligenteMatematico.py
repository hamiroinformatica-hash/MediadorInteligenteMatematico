# Importação de bibliotecas essenciais
import streamlit as st  # Cria a interface web da aplicação
from groq import Groq      # Conecta com a Inteligência Artificial (Llama 3.3)
import time               # Gerencia os tempos de espera e processamento

# 1. CONFIGURAÇÃO DE INTERFACE
# Define o título da aba do navegador e expande o layout para usar toda a largura da tela
st.set_page_config(page_title="Mediador IntMatemático", layout="wide")

# 2. CSS CUSTOMIZADO: ESTILIZAÇÃO VISUAL AVANÇADA
# O comando st.markdown com unsafe_allow_html permite injetar código CSS para personalizar o visual
st.markdown("""
    <style>
    /* Importa a fonte 'Algerian' do Google Fonts para a assinatura */
    @import url('https://fonts.googleapis.com/css2?family=Algerian&display=swap');
    
    /* Personalização da Barra de Rolagem (Scrollbar) - Alta Intensidade */
    ::-webkit-scrollbar { 
        width: 45px !important; /* Define a largura muito grossa para facilitar o toque */
    }
    ::-webkit-scrollbar-track { 
        background: #f1f1f1; /* Cor de fundo do trilho da barra */
    }
    ::-webkit-scrollbar-thumb { 
        background: #000000; /* Cor preta da barra (o sensor visual) */
        border-radius: 5px;  /* Arredondamento leve */
        border: 4px solid #333; /* Borda cinza para destacar o preto */
    }

    /* Ajuste de tipografia para leitura clara de fórmulas matemáticas (LaTeX) */
    .stMarkdown p, .katex {
        font-size: 1.25rem !important; /* Aumenta o tamanho da letra e dos símbolos */
        color: #1a1a1a;               /* Cor do texto quase preta para contraste */
    }

    /* Oculta elementos padrão do Streamlit (Menu e Rodapé original) */
    header {visibility: hidden;} 
    footer {visibility: hidden;}
    
    /* Estilização da Assinatura HBM Fixa no Rodapé */
    .signature-footer {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background-color: rgba(255, 255, 255, 0.98);
        padding: 8px 0;
        text-align: center;
        z-index: 999;
        font-family: 'Algerian', serif; /* Fonte solicitada */
        font-size: 17px;
        color: #1e293b;
        border-top: 1px solid #ddd;
    }

    /* Container para centralizar o botão de restaurar */
    .restore-container { 
        display: flex; 
        justify-content: center; 
        padding-bottom: 110px; 
    }
    </style>
    
    <div class="signature-footer">HBM</div>
    """, unsafe_allow_html=True)

# 3. GESTÃO DE ESTADO (SESSION STATE)
# O session_state mantém os dados salvos mesmo quando a página atualiza (refresh)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Armazena as mensagens trocadas

if "pontos" not in st.session_state:
    st.session_state.pontos = 0         # Armazena a pontuação de evolução do aluno

# Conexão com a API da Groq usando a chave secreta configurada no servidor
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 4. EXIBIÇÃO DO HISTÓRICO DE CHAT
st.title("🎓 Mediador IntMatemático")

# Percorre a lista de mensagens e as exibe com avatares diferentes para IA e Aluno
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

# 5. LÓGICA DE MEDIAÇÃO E ENTRADA DE DADOS
# Cria o campo de digitação na parte inferior
entrada_aluno = st.chat_input("Insira sua questão matemática aqui...")

if entrada_aluno:
    # Adiciona a pergunta do aluno ao histórico e exibe na tela imediatamente
    st.session_state.chat_history.append({"role": "user", "content": entrada_aluno})
    with st.chat_message("user", avatar="👤"):
        st.markdown(entrada_aluno)

    # DEFINIÇÃO DO PROMPT DE SISTEMA (O Regulamento de Funcionamento da IA)
    prompt_sistema = (
        "Você é o 'Mediador IntMatemático' (HBM). Atue sob este REGULAMENTO ESTRITO:\n\n"
        "1. TRANCA DE SEGURANÇA: Se o tema NÃO for Matemática, TRANQUE o avanço e recuse educadamente.\n"
        "2. PRINCÍPIO GERAL: Função mediadora pura. Responsabilidade total do aluno. NUNCA dê respostas, nem que seja de Aritmética, Álgebra, Geometria, Análise e Cálculo, Estatística e Probabilidade ou Matemática Discreta.\n"
        "3. BLOQUEIO ABSOLUTO: Não resolva mesmo se o aluno insistir ou apresentar resultado sem passos, nem que seja questão de nenhuma questão, seja de Aritmética, Álgebra, Geometria, Análise e Cálculo, Estatística e Probabilidade ou Matemática Discreta.\n"
        "4. PROTOCOLO DE 2 SEGUNDOS: Use exemplos similares passo a passo em LaTeX. Nunca resolva a questão original, nem que seja de Aritmética, Álgebra, Geometria, Análise e Cálculo, Estatística e Probabilidade ou Matemática Discreta.\n"
        "5. CONCEITOS: Medie por palavras-chave e analogias. Nunca dê a definição formal, nem que seja de Aritmética, Álgebra, Geometria, Análise e Cálculo, Estatística e Probabilidade ou Matemática Discreta.\n"
        "6. PONTUAÇÃO: Atribua [PONTO_MÉRITO] apenas se o aluno acertar a própria questão com autonomia.\n"
        "7. FORMATAÇÃO: Use LaTeX ($$ ou $)."
    )

    # Inicia a resposta do assistente
    with st.chat_message("assistant", avatar="🎓"):
        # Exibe uma animação de carregamento (spinner)
        with st.spinner("Processando mediação..."):
            # time.sleep(2.1) cumpre o Artigo 3.1 do Regulamento (Processamento >= 2 segundos)
            time.sleep(2.1) 
            
            try:
                # Envia o histórico + regulamento para o modelo Llama 3.3
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": prompt_sistema}] + st.session_state.chat_history,
                    temperature=0.0  # Zero garante que a IA seja rígida e não 'invente' respostas
                )
                feedback = response.choices[0].message.content
                
                # Verifica se a IA concedeu o ponto de mérito no texto da resposta
                if "[PONTO_MÉRITO]" in feedback:
                    st.session_state.pontos += 20  # Incrementa 20 pontos
                    # Substitui a tag técnica por uma mensagem amigável para o aluno
                    feedback = feedback.replace("[PONTO_MÉRITO]", "\n\n✨ **Evolução confirmada! Autonomia na resolução: +20 pontos!**")
                
                # Exibe a resposta final e salva no histórico
                st.markdown(feedback)
                st.session_state.chat_history.append({"role": "assistant", "content": feedback})
                
                # st.rerun() atualiza a página para garantir que a pontuação e o chat apareçam corretamente
                st.rerun()
            except Exception:
                st.error("Erro na mediação. Tente novamente.")

# 6. RODAPÉ DE PONTUAÇÃO E CONTROLES DE LIMPEZA
# Exibe o placar atual de pontos
st.write(f"**Pontuação de Autonomia:** {st.session_state.pontos} pontos")

# Botão para limpar a conversa e zerar pontos (Restaurar)
st.markdown("<div class='restore-container'>", unsafe_allow_html=True)
if st.button("🔄 Restaurar Chat (Limpar)"):
    st.session_state.chat_history = [] # Esvazia a lista de mensagens
    st.session_state.pontos = 0         # Zera os pontos
    st.rerun()                         # Reinicia a aplicação do zero
st.markdown("</div>", unsafe_allow_html=True)
