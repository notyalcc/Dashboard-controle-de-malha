# Dashboard de Performance Logística 🚛📊

Este projeto é um dashboard interativo desenvolvido em Python com **Streamlit** para monitoramento e análise de performance logística. Ele permite visualizar indicadores de volume (Liberados) e participação de malha por transportadora, operação e período.

## 🚀 Funcionalidades

- **KPIs Principais:** Visualização rápida de totais de volume, malha e médias diárias.
- **Gráficos Interativos:** Análises temporais (Diária, Mensal, Anual) utilizando **Plotly**.
- **Filtros Dinâmicos:** Segmentação por data, tipo de operação e transportadora.
- **Banco de Dados Local:** Utiliza **SQLite** para armazenamento persistente dos dados, eliminando dependências de rede complexas.
- **Conexão Híbrida:** Suporta upload de arquivos (CSV/Excel) e leitura direta do banco de dados local.
- **Inserção de Dados:** Formulário lateral para cadastro manual de novos registros diretamente no banco de dados.
- **Rankings:** Top transportadoras por volume e frequência na malha.

## 🛠️ Tecnologias Utilizadas

- [Python 3.13+](https://www.python.org/)
- [Streamlit](https://streamlit.io/) - Framework para web apps de dados.
- [Pandas](https://pandas.pydata.org/) - Manipulação e análise de dados.
- [Plotly](https://plotly.com/python/) - Visualização de dados.
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM e conexão com Banco de Dados SQL.

## 📦 Como rodar localmente

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/nome-do-repo.git
   cd nome-do-repo
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o Dashboard:**
   O banco de dados `dados.db` será criado automaticamente na primeira execução.
   ```bash
   streamlit run dashboard.py
   ```

## 📂 Estrutura do Projeto

- `dashboard.py`: Código principal da aplicação.
- `dados.db`: Banco de dados SQLite (gerado automaticamente).
- `requirements.txt`: Lista de dependências do projeto.

## ☁️ Deploy

Para implantar no **Streamlit Community Cloud**:
1. Suba o código para o GitHub.
2. Conecte seu repositório no Streamlit Cloud.
3. **Nota Importante:** Como o projeto utiliza SQLite local (`dados.db`), os dados inseridos manualmente no Cloud **não persistirão** após a reinicialização do app (devido à natureza efêmera do container). Para produção em nuvem com persistência, recomenda-se alterar a string de conexão para um banco externo (ex: PostgreSQL/Supabase).

## 👨‍💻 Autor

Desenvolvido por **Clayton S. Silva**
