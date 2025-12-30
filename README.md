# Dashboard de Controle Logístico - Malha Fina & Liberados 2026

Este projeto é um dashboard interativo desenvolvido em Python utilizando a biblioteca **Streamlit**. O objetivo é monitorar e analisar o processo de auditoria logística (Malha Fina), permitindo o acompanhamento do fluxo de veículos liberados e retidos para conferência.

**Desenvolvido por:** Clayton S. Silva

## 📋 Funcionalidades

*   **Gestão de Dados:**
    *   Importação de arquivos (CSV, Excel, SQLite).
    *   Inserção manual de registros via formulário na barra lateral.
    *   Limpeza automática de dados (tratamento robusto de datas e formatos numéricos).
    *   Persistência de dados local utilizando SQLite (`dados.db`).
    *   Backup e download do banco de dados completo.
*   **Visualização e Análise:**
    *   **KPIs em Tempo Real:** Fluxo total, veículos liberados, retidos e taxa de retenção global.
    *   **Rankings:** Top transportadoras por volume (fluxo) e por retenção (malha).
    *   **Visão Temporal:** Gráficos interativos com análises diárias, mensais e anuais.
    *   **Análise de Risco:** Mapa de calor (Heatmap) por dia da semana e Funil do processo de sorteio.
*   **Relatórios:**
    *   Exportação de dados filtrados para Excel (`.xlsx`) com formatação correta.
*   **Segurança:**
    *   Sistema de login administrativo para proteger funções de edição e filtros sensíveis.

## 🛠️ Tecnologias Utilizadas

*   **Python 3**
*   **Streamlit:** Interface web interativa e responsiva.
*   **Pandas:** Manipulação e análise de dados de alta performance.
*   **Plotly Express:** Gráficos dinâmicos e interativos.
*   **SQLAlchemy / SQLite:** Gerenciamento de banco de dados local.
*   **OpenPyXL:** Suporte para leitura e escrita de arquivos Excel.

## 🚀 Como Executar

1.  **Instale as dependências:**
    Certifique-se de ter o Python instalado e execute o comando abaixo na pasta do projeto:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Execute a aplicação:**
    ```bash
    streamlit run app.py
    ```

3.  **Acesse no navegador:**
    O Streamlit abrirá automaticamente uma aba no seu navegador (geralmente em `http://localhost:8501`).

## 🔐 Acesso Administrativo

Para acessar as funcionalidades de edição, inserção manual e download de relatórios, utilize a senha de administrador configurada no código (Padrão: `admin123`).

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

