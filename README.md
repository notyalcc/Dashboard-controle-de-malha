# Dashboard de Performance Logística 🚛📊

Este projeto é um dashboard interativo desenvolvido em Python com **Streamlit** para monitoramento e análise de performance logística. Ele permite visualizar indicadores de volume (Liberados) e participação de malha por transportadora, operação e período.

## 🚀 Funcionalidades

- **KPIs Principais:** Visualização rápida de totais de volume, malha e médias diárias.
- **Gráficos Interativos:** Análises temporais (Diária, Mensal, Anual) utilizando **Plotly**.
- **Filtros Dinâmicos:** Segmentação por data, tipo de operação e transportadora.
- **Conexão Híbrida:** Suporta upload de arquivos (CSV/Excel) e conexão direta com banco de dados SQL (PostgreSQL/Supabase).
- **Inserção de Dados:** Formulário lateral para cadastro manual de novos registros diretamente no banco de dados.
- **Rankings:** Top transportadoras por volume e frequência na malha.

## 🛠️ Tecnologias Utilizadas

- [Python 3.13+](https://www.python.org/)
- [Streamlit](https://streamlit.io/) - Framework para web apps de dados.
- [Pandas](https://pandas.pydata.org/) - Manipulação e análise de dados.
- [Plotly](https://plotly.com/python/) - Visualização de dados.
- [SQLAlchemy](https://www.sqlalchemy.org/) & [Psycopg2](https://pypi.org/project/psycopg2/) - Conexão com Banco de Dados SQL.

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

3. **Configure o Banco de Dados:**
   Para segurança, crie um arquivo `.streamlit/secrets.toml` na raiz do projeto com suas credenciais:
   ```toml
   [DATABASE_URL]
   url = "postgresql://usuario:senha@host:porta/nome_banco"
   ```

4. **Execute o Dashboard:**
   ```bash
   streamlit run dashboard.py
   ```

## ☁️ Deploy

Este projeto está pronto para ser implantado no **Streamlit Community Cloud**. Basta conectar seu repositório GitHub e configurar a `DATABASE_URL` na seção de "Secrets" do painel do Streamlit.

## 👨‍💻 Autor

Desenvolvido por **Clayton S. Silva**