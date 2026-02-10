import streamlit as st
from groq import Groq
import time

# --- 1. CONFIGURAÇÃO E ESTILO (Otimizado para Moçambique) ---
st.set_page_config(page_title="Mediador IntMatemático HBM", layout="wide")
st.markdown("""
    <style>
    ::-webkit-scrollbar { width: 35px !important; }
    ::-webkit-scrollbar-thumb { background: #000; border-radius: 10px; }
    .signature-footer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: white; text-align: center; font-family: 'Algerian', serif;
        font-size: 16px; border-top: 2px solid #333; z-index: 1000; padding: 5px;
    }
    .stAlert { margin-bottom: 50px; }
    </style>
    <div class="signature-footer">HBM - Mediação Didática Inviolável</div>
""", unsafe_allow_html=True)

# Gestão de Estado (Persistência de Dados)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pontos" not in st.session_state:
    st.session_state.pontos = 0

# Conexão segura com tratamento de erro
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("Chave API não configurada. Verifique os Secrets.")

# --- 2. PROMPT DE SISTEMA BLINDADO (REGRAS P1-P6 EXPLÍCITAS) ---
PROMPT_SISTEMA_V2 = """
VOCÊ É O MEDIADOR HBM. SEU PAPEL É OBSERVAR O ALUNO SEM NUNCA TOCAR NA EQUAÇÃO DELE.

### PROTOCOLO DE RESPOSTA (ESTRITO):
1. **P1/P2 (Oculto):** O aluno apresenta 'X'. Você resolve mentalmente para saber o resultado 'Y'.
2. **P3/P4 (Mediação Inicial):** NUNCA simplifique ou escreva a equação 'X'. Crie uma similar 'S1', RESOLVA-A INTEIRA passo a passo com LaTeX e diga: "Baseado nesta lógica, tente resolver a sua."
3. **P5/P6 (Análise de Intervenção):** Quando o aluno enviar um passo:
   - **NÃO simplifique o passo dele na tela.**
   - **NÃO escreva frases como "Você combinou os termos..." ou "Sua equação agora é...".**
   - **REGRA DE OURO:** Se o aluno escrever '2x-x=9', você NÃO pode escrever 'x=9'. Você deve apenas dizer: "Estás num bom caminho" ou "Está errado".
   - **Ação após o Feedback:** Após dizer "Estás num bom caminho" ou "Está errado", apresente IMEDIATAMENTE a resolução completa de um NOVO exercício similar (S2) que ajude o aluno a continuar ou corrigir o erro.

### PROIBIÇÕES ABSOLUTAS:
- Proibido repetir os números ou variáveis da questão original do aluno.
- Proibido dar a resposta final.
- Proibido mostrar o processo de simplificação da dúvida do aluno.
- Use Analogias de Moçambique (vendedores no mercado de Xipamanine, colheita de castanha em Inhambane) apenas para motivar, nunca para resolver a conta.
- Use LaTeX ($$) para TODA a matemática.
"""

# --- 3. INTERFACE ---
st.title("🎓 Mediador IntMatemático")
st.write(f"📊 **Pontuação Acumulada:** {st.session_state.pontos}")

# Exibição do histórico sem duplicidade
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

# Entrada do Aluno
entrada = st.chat_input("Digite sua dúvida ou o próximo passo...")

if entrada:
    st.session_state.chat_history.append({"role": "user", "content": entrada})
    with st.chat_message("user", avatar="👤"):
        st.markdown(entrada)

    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("Processando mediação pedagógica oculta..."):
            time.sleep(2) # Tempo para simular análise P2
            
            try:
                # Chamada da API Groq
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": PROMPT_SISTEMA_V2}] + st.session_state.chat_history,
                    temperature=0.0
                )
                
                feedback = response.choices[0].message.content
                
                # Sistema de Gamificação (P6)
                if "[PONTO_MÉRITO]" in feedback:
                    st.session_state.pontos += 20
                    feedback = feedback.replace("[PONTO_MÉRITO]", "\n\n✨ **Parabéns! Resposta correta! +20 pontos.**")
                elif "[MEIO_PONTO]" in feedback:
                    st.session_state.pontos += 10
                    feedback = feedback.replace("[MEIO_PONTO]", "\n\n🚀 **Caminho certo! Continue assim. +10 pontos.**")

                st.markdown(feedback)
                st.session_state.chat_history.append({"role": "assistant", "content": feedback})
                
                # Uso de fragmentos ou st.rerun() controlado para evitar erro de conexão
                st.rerun()

            except Exception as e:
                st.error(f"Houve uma instabilidade na rede. Por favor, tente enviar novamente.")

# Botão de Reset
if st.sidebar.button("🔄 Reiniciar (Nova Questão)"):
    st.session_state.chat_history = []
    st.session_state.pontos = 0
    st.rerun()
