# 🤖 PowerTech AI Support - Assistente Técnico Inteligente (CLP PT-500)

### 🚀 Projeto de Finalização de Curso - SENAI
**Desenvolvedor:** Pedro  
**Contexto Industrial:** PowerTech Solutions & Automation  

---

## 📄 Contextualização do Projeto

A **PowerTech Solutions** é responsável pela manutenção e suporte técnico de equipamentos industriais automatizados. Com o aumento significativo no volume de chamados de campo, tornou-se crítico para os técnicos localizar rapidamente códigos de falha, alarmes e rotinas de segurança dentro de manuais densos.

Para solucionar este problema, foi desenvolvido o **PowerTech AI Support**: um assistente virtual inteligente baseado em Inteligência Artificial Generativa com arquitetura **RAG (Retrieval-Augmented Generation)**. O sistema é capaz de ler o manual técnico do **CLP Industrial PT-500** em formato PDF, vetorizar suas páginas e responder com precisão cirúrgica às dúvidas dos técnicos em tempo real, mitigando erros humanos no chão de fábrica.

---

## 🛠️ Tecnologias e Arquitetura Utilizadas

O pipeline inteligente do sistema foi construído utilizando as ferramentas mais modernas do mercado de IA:

* **Interface de Usuário (UI):** [Streamlit](https://streamlit.io/) (Configurado com Layout Wide e Injeção Customizada de CSS).
* **Orquestração de IA:** [LangChain](https://www.langchain.com/) (Uso de LCEL - LangChain Expression Language).
* **Processamento de Documentos:** `PyPDFLoader` (Leitura do Manual Técnico) e `RecursiveCharacterTextSplitter` (Fatiamento inteligente de texto).
* **Modelo de Embeddings:** `NVIDIA Embeddings` (Modelo `nvidia/nv-embedqa-e5-v5` de alta performance).
* **Banco de Dados Vetorial:** [FAISS](https://github.com/facebookresearch/faiss) (Facebook AI Similarity Search - Executado localmente em CPU).
* **Modelo de Linguagem (LLM):** [ChatNVIDIA](https://build.nvidia.com/) (Modelo `meta/llama-3.1-8b-instruct` via API NVIDIA AI Endpoints).

---

## 🎨 Design System: Paleta Industrial Tech Premium

Para garantir uma experiência de uso imersiva de nível corporativo e excelente legibilidade sob diferentes condições de luz em ambientes industriais, a interface adota um padrão *Dark Mode* estrito:

* **Fundo Principal:** `#0B1220` (Azul-escuro profundo espacial)
* **Painel Lateral (Sidebar):** `#111A2E` (Tom de controle de console)
* **Containers e Cards:** `#162235` (Cinza-azulado industrial)
* **Balões de Chat da IA:** `#1E2A3A` (Tom neutro e equilibrado alinhado à esquerda)
* **Balões do Usuário (Destaque):** `#00A67E` (Verde esmeralda corporativo alinhado à direita)
* **Texto Principal:** `#E6EDF3` | **Texto Secundário:** `#9AA4B2`
* **Sinalizadores de Erro/Alerta:** `#FF4D4D`

### 📱 Recursos Exclusivos de UX Implementados:
1.  **Efeito Typewriter (Máquina de Escrever):** O título central é renderizado letra por letra a uma taxa de `0.12s` exclusivamente no primeiro acesso, adicionando dinamismo visual ao sistema.
2.  **Conversa Estilo WhatsApp:** Os balões possuem margens dinâmicas, limitados a `75%` da tela, separando o diálogo de forma orgânica e intuitiva.
3.  **Telemetria Dinâmica:** A barra lateral monitora os componentes em tempo real por meio de badges com LEDs pilotos digitais (Verde para Ativo, Amarelo para Atenção e Vermelho para Erros).
4.  **Mecanismo de Segurança de Mídia:** O sistema auto-detecta mídias na pasta raiz; caso imagens de logo ou avatar sumam, ele injeta fallbacks em emoji para manter o app estável.

---

## 📂 Estrutura de Pastas do Projeto

Para o correto funcionamento do ecossistema e suporte a execuções em ambientes de homologação ou offline, mantenha a árvore de diretórios organizada exatamente assim:

```text
PowerTech_AI_Assistant/
│
├── app.py                  # Código-fonte principal do Streamlit
├── manual.pdf              # Manual técnico fictício do CLP PT-500 (Mín. 10 págs)
├── .env                    # Arquivo de credenciais protegidas (API Key)
├── requirements.txt        # Manifesto de dependências do Python
│
└── assets/                 # Diretório de mídias e identidades visuais local
    ├── logo.png            # Logotipo da PowerTech exibido na Sidebar (PNG/JPG)
    ├── user.png            # Avatar de alta resolução do Técnico (512x512px)
    └── ai.png              # Avatar de alta resolução do Engenheiro IA (512x512px)
