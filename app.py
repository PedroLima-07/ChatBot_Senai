# ============================================================
# POWERTECH AI ASSISTANT - INDUSTRIAL TECH PREMIUM UI
# Projeto Final - SENAI
# Desenvolvedor: Pedro
# Visual: WhatsApp Style + Local High-Res Avatars & Logo
# ============================================================

import os
import time  # Controla o tempo do efeito de digitação
import streamlit as st
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (.env)
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings, ChatNVIDIA

# ============================================================
# CONFIGURAÇÃO DOS ÍCONES E LOGO LOCAL (PASTA ASSETS)
# ============================================================
ICON_USER = "assets/user.png"
ICON_IA = "assets/ai.png"

# Sistema de segurança para Avatars
if not os.path.exists(ICON_USER):
    ICON_USER = "😎"
if not os.path.exists(ICON_IA):
    ICON_IA = "🤖"

# Busca automática pelo formato da logo (png, jpg ou jpeg)
PATH_LOGO = None
for ext in [".png", ".jpg", ".jpeg"]:
    caminho_teste = f"assets/logo{ext}"
    if os.path.exists(caminho_teste):
        PATH_LOGO = caminho_teste
        break

# ============================================================
# CONFIGURAÇÃO DA PÁGINA E DESIGN PREMIUM (CSS INJECTION)
# ============================================================
st.set_page_config(
    page_title="PowerTech AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção CSS com a paleta Industrial Tech Premium organizada por blocos
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* ==========================================
       BLOCO 1: IDENTIDADE VISUAL GLOBAL (UI)
       ========================================== */
    .stApp {
        background-color: #0B1220 !important; /* Fundo Principal */
        color: #E6EDF3 !important;            /* Texto Principal */
        font-family: 'Inter', sans-serif;
    }
    
    /* Força a cor do texto principal em parágrafos e marcações comuns */
    p, span, label, div[data-testid="stMarkdownContainer"] p {
        color: #E6EDF3 !important;
    }

    .main-title {
        color: #00A67E; /* Destaque da Marca */
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0px;
        text-align: center;
        text-shadow: 0px 0px 15px rgba(0, 166, 126, 0.2);
    }
    
    /* ==========================================
       BLOCO 2: PAINEL LATERAL (SIDEBAR E TELEMETRIA)
       ========================================== */
    [data-testid="stSidebar"] {
        background-color: #111A2E !important; /* Fundo Sidebar */
        border-right: 1px solid #162235;
    }
    
    /* CORREÇÃO DO BOTÃO: Garante que o botão de abrir/fechar a sidebar apareça estilizado */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        background: transparent !important;
    }
    div[data-testid="stHeaderDecoration"] {
        visibility: hidden;
    }
    button[data-testid="stSidebarCollapseButton"] {
        background-color: #162235 !important;
        color: #E6EDF3 !important;
        border: 1px solid #1E2A3A !important;
        border-radius: 6px !important;
    }
    button[data-testid="stSidebarCollapseButton"]:hover {
        background-color: #1E2A3A !important;
        color: #00A67E !important;
        border-color: #00A67E !important;
    }
    
    /* Cards de Informação na Sidebar */
    .sidebar-card {
        background-color: #162235; /* Fundo dos Cards */
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #1E2A3A;
        margin-bottom: 10px;
    }
    .sidebar-label {
        font-size: 0.75rem;
        color: #9AA4B2; /* Texto Secundário */
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }
    .sidebar-value {
        font-size: 0.95rem;
        font-weight: 600;
        color: #E6EDF3; /* Texto Principal */
    }
    
    /* Badges de Status da Telemetria */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 6px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        width: 100%;
        margin-bottom: 8px;
        background-color: #162235; /* Container do Status */
        border: 1px solid #1E2A3A;
    }
    .badge-success { color: #00A67E; } /* Sucesso/Ativo */
    .badge-warning { color: #9AA4B2; } /* Pendente/Aviso */
    .badge-error { color: #FF4D4D; }   /* Erros/Alertas */
    .badge-dot { height: 8px; width: 8px; border-radius: 50%; display: inline-block; margin-right: 8px; }
    
    /* Botão Limpar Conversa */
    .stButton>button {
        width: 100%;
        background-color: #162235;
        color: #9AA4B2; 
        border: 1px solid #1E2A3A;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1E2A3A !important;
        color: #FF4D4D !important; /* Destaque de Erro ao passar o mouse */
        border-color: #FF4D4D !important;
        box-shadow: 0px 0px 10px rgba(255, 77, 77, 0.2);
    }
    
    /* ==========================================
       BLOCO 3: JANELA DE CHAT (MENSAGENS E ALINHAMENTO)
       ========================================== */
    div[data-testid="stChatMessage"] {
        padding: 12px 16px !important;
        margin-bottom: 12px !important;
        max-width: 75% !important; 
        border-radius: 14px !important;
    }

    /* Balão do Usuário -> Alinhado à Direita e Cor de Destaque #00A67E */
    div[data-testid="stChatMessage"]:has(.user-marker) {
        background-color: #00A67E !important; 
        margin-left: auto !important;         
        margin-right: 0px !important;
        border: none !important;
        border-top-right-radius: 2px !important;
    }
    div[data-testid="stChatMessage"]:has(.user-marker) p {
        color: #FFFFFF !important; /* Força contraste do texto no balão verde */
    }

    /* Balão da IA -> Alinhado à Esquerda e Tom Neutro Escuro #1E2A3A */
    div[data-testid="stChatMessage"]:has(.assistant-marker) {
        background-color: #1E2A3A !important; 
        margin-right: auto !important;        
        margin-left: 0px !important;
        border: none !important;
        border-top-left-radius: 2px !important;
    }

    /* Ajuste para imagens de avatar ficarem perfeitamente redondas */
    div[data-testid="stChatMessage"] img {
        border-radius: 50% !important;
        object-fit: cover !important;
    }

    /* ==========================================
       BLOCO 4: SISTEMAS DE ENTRADA (INPUTS E BOTÕES)
       ========================================== */
    /* CORREÇÃO DO RODAPÉ: Elimina completamente a faixa preta abaixo do input */
    div[data-testid="stBottom"], div[data-testid="stBottomBlockContainer"] {
        background-color: #0B1220 !important;
    }

    div[data-testid="stChatInput"] {
        border-radius: 10px !important;
        background-color: #162235 !important; /* Fundo do Input */
        border: 1px solid #1E2A3A !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #E6EDF3 !important; 
        background-color: transparent !important;
    }
    
    /* Ocultação limpa do menu de deploy (Mantendo o cabeçalho funcional) */
    div[data-testid="stToolbar"] {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Obtém a chave da API com tratamento de segurança
nvidia_api_key = os.getenv("NVIDIA_API_KEY")
try:
    if "NVIDIA_API_KEY" in st.secrets:
        nvidia_api_key = st.secrets["NVIDIA_API_KEY"]
except Exception:
    pass

# ==========================
# INICIALIZAÇÃO DO RAG
# ==========================
@st.cache_resource(show_spinner="📄 Processando e indexando o manual técnico...")
def inicializar_rag():
    nome_arquivo = "manual.pdf"
    if not os.path.exists(nome_arquivo):
        return None
    try:
        loader = PyPDFLoader(nome_arquivo)
        paginas = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=80
        )
        docs = text_splitter.split_documents(paginas)

        embeddings = NVIDIAEmbeddings(
            model="nvidia/nv-embedqa-e5-v5",
            nvidia_api_key=nvidia_api_key,
            model_type="passage"
        )

        vectorstore = FAISS.from_documents(docs, embedding=embeddings)
        return vectorstore.as_retriever(search_kwargs={"k": 4})
    except Exception:
        return None

retriever = inicializar_rag() if nvidia_api_key else None

# ============================================================
# PAINEL LATERAL (SIDEBAR) - LOGO INTEGRADA
# ============================================================
with st.sidebar:
    # Se a logo existir na pasta assets, renderiza a imagem; caso contrário, usa o texto padrão
    if PATH_LOGO:
        st.image(PATH_LOGO, use_container_width=True)
    else:
        st.markdown("<h2 style='color:#00A67E; font-weight:700; margin-bottom:0;'>PowerTech</h2>", unsafe_allow_html=True)
        
    st.markdown("<p style='color:#9AA4B2; font-size:0.85rem; margin-top:0;'>Solutions & Automation</p>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 10px 0; border-color: #1E2A3A;'>", unsafe_allow_html=True)
    
    # Cards de Informações com a Paleta Técnica
    st.markdown("""
    <div class="sidebar-card">
        <div class="sidebar-label">⚙️ Equipamento Alvo</div>
        <div class="sidebar-value">CLP Industrial PT-500</div>
    </div>
    <div class="sidebar-card">
        <div class="sidebar-label">👨‍💻 Técnico Responsável</div>
        <div class="sidebar-value">Pedro</div>
    </div>
    <div class="sidebar-card">
        <div class="sidebar-label">🧠 Modelo LLM</div>
        <div class="sidebar-value" style="font-family: monospace; color: #E6EDF3;">Llama 3.1 8B</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 15px 0; border-color: #1E2A3A;'>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.8rem; font-weight:bold; color:#9AA4B2; text-transform:uppercase;'>📡 Telemetria do Sistema</p>", unsafe_allow_html=True)
    
    # Lógica Dinâmica dos Badges Estilizados
    if os.path.exists("manual.pdf"):
        st.markdown('<div class="badge badge-success"><span class="badge-dot" style="background-color:#00A67E;"></span>Manual: Ativo</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="badge badge-error"><span class="badge-dot" style="background-color:#FF4D4D;"></span>Manual: Ausente</div>', unsafe_allow_html=True)
        
    if retriever is not None:
        st.markdown('<div class="badge badge-success"><span class="badge-dot" style="background-color:#00A67E;"></span>Vetorização: OK</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="badge badge-warning"><span class="badge-dot" style="background-color:#9AA4B2;"></span>Vetorização: Pendente</div>', unsafe_allow_html=True)
        
    if nvidia_api_key:
        st.markdown('<div class="badge badge-success"><span class="badge-dot" style="background-color:#00A67E;"></span>API Core: Online</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="badge badge-error"><span class="badge-dot" style="background-color:#FF4D4D;"></span>API Core: Offline</div>', unsafe_allow_html=True)
        
    st.markdown("<hr style='margin: 15px 0; border-color: #1E2A3A;'>", unsafe_allow_html=True)
    
    if st.button("🗑️ Resetar Terminal"):
        st.session_state.messages = []
        st.session_state.titulo_carregado = False
        st.rerun()

# ============================================================
# ÁREA CENTRAL DA INTERFACE (CANVAS DE TEXTO)
# ============================================================
if "titulo_carregado" not in st.session_state:
    st.session_state.titulo_carregado = False

title_placeholder = st.empty()
subtitle_placeholder = st.empty()

texto_titulo = "🤖 PowerTech AI Support"
texto_subtitulo = "Assistente Avançado de Diagnóstico Cooperativo"

# Efeito máquina de escrever
if not st.session_state.titulo_carregado:
    for i in range(1, len(texto_titulo) + 1):
        title_placeholder.markdown(f'<h1 class="main-title">{texto_titulo[:i]}</h1>', unsafe_allow_html=True)
        time.sleep(0.12)
    
    subtitle_placeholder.markdown(f'<p style="color:#9AA4B2; font-size:1.1rem; margin-top:5px; text-align: center;">{texto_subtitulo}</p>', unsafe_allow_html=True)
    st.session_state.titulo_carregado = True
else:
    title_placeholder.markdown(f'<h1 class="main-title">{texto_titulo}</h1>', unsafe_allow_html=True)
    subtitle_placeholder.markdown(f'<p style="color:#9AA4B2; font-size:1.1rem; margin-top:5px; text-align: center;">{texto_subtitulo}</p>', unsafe_allow_html=True)

st.markdown("<hr style='margin: 10px 0; border-color: #162235;'>", unsafe_allow_html=True)

if not nvidia_api_key:
    st.markdown(f'<div style="color:#FF4D4D; background-color:rgba(255,77,77,0.1); padding:15px; border-radius:8px; border:1px solid #FF4D4D;">💡 Terminal de Inteligência aguardando credenciais. Insira sua chave NVIDIA_API_KEY no arquivo .env.</div>', unsafe_allow_html=True)
    st.stop()

# ==========================
# CONFIGURAÇÃO DO MODELO E PROMPT
# ==========================
llm = ChatNVIDIA(
    model="meta/llama-3.1-8b-instruct",
    nvidia_api_key=nvidia_api_key,
    temperature=0.2
)

template_prompt = """
Você é um engenheiro especialista em manutenção industrial e automação da PowerTech Solutions.
Sua tarefa é auxiliar técnicos de campo a diagnosticar falhas no CLP Industrial PT-500.

Regras Estritas de Operação:
1. Analise detalhadamente os fragmentos do manual fornecidos no contexto abaixo. Eles podem conter termos em inglês.
2. Responda obrigatoriamente em PORTUGUÊS DO BRASIL de forma técnica, limpa, objetiva e estruturada (use bullet points se ajudar a explicar o procedimento).
3. Baseie-se estritamente nas informações repassadas. Nunca invente dados técnicos ou normas de segurança.
4. Caso a resposta exata para a pergunta do técnico NÃO esteja explícita no manual, responda rigorosamente com a seguinte frase:
   "Desculpe, esta informação não consta no manual técnico."

Contexto extraído do Manual:
{context}

Pergunta do Técnico:
{question}

Resposta Técnica Otimizada:
"""

prompt = ChatPromptTemplate.from_template(template_prompt)

if retriever:
    rag_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

# ==========================
# HISTÓRICO DA CONVERSA
# ==========================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "🛠️ **Sistemas prontos para operação.** Base de conhecimento do CLP PT-500 carregada com sucesso. Qual a anomalia ou rotina que deseja reportar?"
        }
    ]

for message in st.session_state.messages:
    avatar_escolhido = ICON_USER if message["role"] == "user" else ICON_IA
    with st.chat_message(message["role"], avatar=avatar_escolhido):
        if message["role"] == "user":
            st.markdown('<span class="user-marker"></span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="assistant-marker"></span>', unsafe_allow_html=True)
        st.markdown(message["content"])

# ==========================
# PROCESSAMENTO DE ENTRADA
# ==========================
if prompt_usuario := st.chat_input("Digite o código de falha ou sintoma do equipamento..."):

    st.session_state.messages.append({"role": "user", "content": prompt_usuario})
    
    with st.chat_message("user", avatar=ICON_USER):
        st.markdown('<span class="user-marker"></span>', unsafe_allow_html=True)
        st.markdown(prompt_usuario)

    with st.chat_message("assistant", avatar=ICON_IA):
        st.markdown('<span class="assistant-marker"></span>', unsafe_allow_html=True)
        with st.spinner("Varrendo registros do manual técnico..."):
            try:
                if retriever:
                    resposta = rag_chain.invoke(prompt_usuario)
                    st.markdown(resposta)
                    st.session_state.messages.append({"role": "assistant", "content": resposta})
                else:
                    st.markdown(f'<span style="color:#FF4D4D;">Erro no subsistema de leitura vetorial. Verifique o arquivo "manual.pdf".</span>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<span style="color:#FF4D4D;">Falha de comunicação com a malha neural NVIDIA: {e}</span>', unsafe_allow_html=True)