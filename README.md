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
    *   **Atualização Dinâmica:** Botão para recarregar dados do banco sem reiniciar o servidor.
*   **Filtros e Navegação:**
    *   **Filtro de Ano:** Seletor múltiplo de anos (ex: 2024, 2025) para otimizar a performance e focar a análise em períodos históricos específicos.
    *   **Refinamento de Dados:** Combinação de filtros por Data, Tipo de Operação e Transportadora.
*   **Visualização e Análise:**
    *   **Contexto Visual Dinâmico:** Os títulos dos gráficos e o cabeçalho do dashboard se adaptam automaticamente para exibir o período exato da análise (ex: "01/01 a 31/01"), facilitando a interpretação em reuniões e relatórios.
    *   **KPIs Inteligentes:** Painel com métricas de Fluxo Total, Liberados, Retidos e Taxa de Retenção Global. Inclui indicadores de variação (Delta) comparando com o período anterior.
    *   **Rankings Interativos:**
        *   Top Transportadoras por Volume (Fluxo).
        *   Top Transportadoras por Retenção (Malha Absoluta).
    *   **Análise de Risco e Processo:**
        *   **Funil do Sorteio:** Visualização do gargalo entre veículos na portaria vs. veículos enviados para reconferência.
        *   **Mapa de Calor (Heatmap):** Identifica padrões de retenção por dia da semana e transportadora.
    *   **Visão Temporal:**
        *   **Diária:** Análise granular com filtro independente para isolar dias específicos.
        *   **Mensal e Anual:** Visão macro para identificar sazonalidade e tendências de longo prazo.
*   **Relatórios:**
    *   Exportação de dados filtrados para Excel (`.xlsx`) com formatação correta.
*   **Segurança:**
    *   Sistema de login administrativo para proteger funções de edição e filtros sensíveis.

## 🚛 Entenda o Processo (Malha Fina)

O dashboard foi desenhado para monitorar o seguinte fluxo operacional:

1.  **Carregamento:** A transportadora carrega e segue para a portaria.
2.  **Sorteio (Portaria):** O veículo passa por um sorteio aleatório.
3.  **Decisão:**
    *   🟢 **Liberado:** Segue viagem imediatamente.
    *   🔴 **Malha:** O veículo é bloqueado e deve retornar ao **Setor de Retorno** para uma nova conferência física.
4.  **Conclusão:** Após a reconferência, divergências são apontadas ou o veículo é liberado.

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

*   ![alt text](image-2.png) 
    ![alt text](image-4.png)
    ![alt text](image-5.png)
    ![alt text](image-6.png)




---
© 2025 Clayton S. Silva



