# 📊 Dashboard de Controle Logístico - Malha Fina & Liberados

> **Desenvolvido por:** Clayton S. Silva

Este projeto é um Dashboard interativo desenvolvido em **Python** utilizando **Streamlit** para o monitoramento e auditoria de processos logísticos. O foco principal é a gestão do fluxo de saída de veículos, comparando o volume de **Liberados** (fluxo normal) versus **Malha Fina** (veículos retidos para reconferência/auditoria).

## 🎯 Objetivo

Fornecer uma visão clara e analítica sobre a operação logística, permitindo:
*   Acompanhamento de KPIs de fluxo e retenção.
*   Identificação de gargalos e tendências de auditoria.
*   Rankings de performance por transportadora.
*   Análises temporais (Diária, Mensal e Anual).

## 🚀 Funcionalidades

*   **KPIs em Tempo Real:** Visualização imediata do Fluxo Total, Veículos Liberados, Retidos e Taxa de Retenção Global (%).
*   **Gráficos Interativos (Plotly):**
    *   Rankings de Volume e Retenção.
    *   Evolução temporal do fluxo e da taxa de malha.
    *   Distribuição por Operação e Transportadora (Gráficos de Rosca).
*   **Gestão de Dados (CRUD):**
    *   **Importação:** Upload de arquivos `.csv` ou `.xlsx` (Excel).
    *   **Inserção Manual:** Formulário lateral para adicionar registros individuais.
    *   **Persistência:** Os dados são salvos automaticamente em um banco de dados local SQLite (`dados.db`).
    *   **Backup:** Botão para baixar o banco de dados atualizado.
*   **Filtros Avançados:**
    *   Filtro global por Período, Operação e Transportadora.
    *   Filtro independente para análise de um dia específico.
    *   Seletor de meses para comparação.
*   **Controle de Acesso:** Sistema de login para proteger funções administrativas (Upload, Edição, Filtros).

## 🛠️ Tecnologias Utilizadas

-   Python 3.x
-   Streamlit - Framework para Web Apps de Data Science.
-   Pandas - Manipulação e análise de dados.
-   Plotly Express - Visualização de dados interativa.
-   SQLAlchemy - Integração com banco de dados SQL.
-   SQLite - Banco de dados local leve.

## 📦 Instalação e Execução Local

Siga os passos abaixo para rodar o projeto na sua máquina:

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
    cd NOME_DO_REPOSITORIO
    ```

2.  **Crie um ambiente virtual (Opcional, mas recomendado):**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o Dashboard:**
    ```bash
    streamlit run app.py
    ```

5.  **Acesse no navegador:**
    O app abrirá automaticamente em `http://localhost:8501`.

## 🔐 Acesso Administrativo

Para acessar as funcionalidades de edição, upload e filtros na barra lateral, utilize a senha padrão configurada no código:
*   **Senha:** `0000000`

## ☁️ Como colocar Online (Deploy)

A maneira mais fácil de publicar este dashboard gratuitamente é usando o **Streamlit Cloud**:

1.  Suba este código para um repositório no **GitHub**.
2.  Crie uma conta no Streamlit Cloud.
3.  Conecte sua conta do GitHub e selecione o repositório deste projeto.
4.  O Streamlit detectará automaticamente o arquivo `requirements.txt` e instalará as dependências.
5.  Pronto! Seu dashboard estará online.

## 📂 Estrutura de Arquivos

*   `app.py`: Código principal da aplicação.
*   `requirements.txt`: Lista de bibliotecas necessárias.
*   `dados.db`: Banco de dados SQLite (gerado automaticamente ao rodar o app).
*   `README.md`: Documentação do projeto.

---
© 2025 Clayton S. Silva
