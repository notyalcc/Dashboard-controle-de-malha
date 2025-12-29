import streamlit as st
import pandas as pd
import plotly.express as px
import io
import os
import tempfile
from sqlalchemy import create_engine
from pandas.api.types import is_datetime64_any_dtype

# --- Configuração da Página ---
st.set_page_config(page_title="Dashboard de Logística", layout="wide")

# --- 1. CARREGAMENTO E TRATAMENTO DE DADOS ---

# CONFIGURAÇÃO DO BANCO DE DADOS
DATABASE_URL = "sqlite:///dados.db"
TABLE_NAME = 'performance_logistica'

@st.cache_resource
def get_database_engine(url):
    return create_engine(url)

engine = get_database_engine(DATABASE_URL)

# --- INICIALIZAÇÃO DOS DADOS NA MEMÓRIA (SESSION STATE) ---
if 'df_dados' not in st.session_state:
    try:
        # Lê do banco local
        df_start = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", con=engine, parse_dates=['DATA'])
        # Garante tipos corretos
        df_start.columns = df_start.columns.str.strip().str.upper()
        if 'DATA' in df_start.columns:
            df_start['DATA'] = pd.to_datetime(df_start['DATA'])
        st.session_state['df_dados'] = df_start
    except Exception:
        # Se der erro (ex: banco não existe), inicia vazio
        st.session_state['df_dados'] = pd.DataFrame(columns=['DATA', 'TRANSPORTADORA', 'OPERAÇÃO', 'LIBERADOS', 'MALHA'])

def save_uploaded_data(df, replace=False):
    try:
        # Colunas esperadas
        expected_cols = ['DATA', 'TRANSPORTADORA', 'OPERAÇÃO', 'LIBERADOS', 'MALHA']
        # Filtra colunas existentes no DF carregado
        cols_to_save = [c for c in expected_cols if c in df.columns]
        
        if cols_to_save:
            if replace:
                st.session_state['df_dados'] = df[cols_to_save].copy()
            else:
                st.session_state['df_dados'] = pd.concat([st.session_state['df_dados'], df[cols_to_save]], ignore_index=True)
            
            # Remove duplicatas exatas para evitar sujeira nos dados
            st.session_state['df_dados'] = st.session_state['df_dados'].drop_duplicates()
            
            # Salva no banco físico também para persistir
            st.session_state['df_dados'].to_sql(TABLE_NAME, engine, if_exists='replace', index=False)
            st.sidebar.success(f"✅ Dados atualizados e salvos!")
        else:
            st.sidebar.error("❌ O arquivo não contém as colunas necessárias.")
    except Exception as e:
        st.sidebar.error(f"❌ Erro ao salvar: {e}")

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Realiza a limpeza e padronização dos dados."""
    # Padronizar nomes das colunas
    df.columns = df.columns.str.strip().str.upper()

    if 'DATA' in df.columns:
        # Só executa a limpeza pesada se NÃO for data ainda
        if not is_datetime64_any_dtype(df['DATA']):
            # 1. Converter para string e limpar espaços
            df['DATA'] = df['DATA'].astype(str).str.strip()
            
            # 2. Corrigir erro comum 31/09
            df['DATA'] = df['DATA'].str.replace('31/09', '30/09', regex=False)
            
            # 3. Tentar converter formato padrão (Dia/Mês/Ano)
            # errors='coerce' transforma o que falhar em NaT (Not a Time)
            dates_iso = pd.to_datetime(df['DATA'], dayfirst=True, errors='coerce')
            
            # 4. Recuperar datas que falharam (NaT) tentando ler como Serial Excel (números)
            # Isso recupera as linhas que o Excel salvou como número (ex: 45321)
            mask_nat = dates_iso.isna()
            if mask_nat.any():
                try:
                    # Tenta converter strings numéricas para float e depois para data (Excel base 1899-12-30)
                    numeric_dates = pd.to_numeric(df.loc[mask_nat, 'DATA'], errors='coerce')
                    recovered = pd.to_datetime(numeric_dates, unit='D', origin='1899-12-30')
                    dates_iso = dates_iso.fillna(recovered)
                except:
                    pass
            
            df['DATA'] = dates_iso
            
            # Verifica e remove linhas que continuam inválidas
            linhas_invalidas = df['DATA'].isna().sum()
            if linhas_invalidas > 0:
                st.warning(f"⚠️ Atenção: {linhas_invalidas} linhas foram removidas pois a coluna 'DATA' contém valores inválidos ou vazios.")
                df = df.dropna(subset=['DATA'])

    # Garantir numéricos
    for col in ['LIBERADOS', 'MALHA']:
        if col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.')
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    return df

def load_data(uploaded_file=None):
    df = None
    # 1. Tenta carregar do upload
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                # Lógica robusta para CSV (ponto e vírgula ou vírgula)
                try:
                    df = pd.read_csv(uploaded_file, sep=';')
                    if df.shape[1] < 2:
                        uploaded_file.seek(0)
                        df = pd.read_csv(uploaded_file, sep=',')
                except:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, sep=None, engine='python')
            else:
                df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")
            return None
    # 2. Carrega da Memória (Session State)
    else:
        if 'df_dados' in st.session_state:
            df = st.session_state['df_dados'].copy()

    if df is not None:
        df = clean_dataframe(df)

    return df

# --- 2. BARRA LATERAL (UPLOAD E FILTROS) ---

# Tenta carregar logo localmente
script_dir = os.path.dirname(os.path.abspath(__file__))
files_in_dir = os.listdir(script_dir)
possible_logos = ["logo.png", "logo.jpg", "logo.jpeg"]
found_logo = next((f for f in files_in_dir if f.lower() in possible_logos), None)
local_logo = os.path.join(script_dir, found_logo) if found_logo else None

logo_image = None
if local_logo:
    logo_image = local_logo
    st.sidebar.image(local_logo)
else:
    # Fallback para o GIF se não tiver logo local
    st.sidebar.image("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExNzVseGVsdWtocmNidGU3MDZtYzdmcm1kMzMxM3VhZGJjYzJuNGZiMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/hR12JVvN9GftOzxqGd/giphy.gif", width=150)

# --- SISTEMA DE LOGIN (BARRA LATERAL) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def check_login():
    if st.session_state['logged_in']:
        if st.sidebar.button("🔓 Sair (Logout)"):
            st.session_state['logged_in'] = False
            st.rerun()
        return True
    
    st.sidebar.markdown("### 🔒 Acesso Restrito")
    senha = st.sidebar.text_input("Senha de Admin", type="password")
    if st.sidebar.button("Entrar"):
        if senha == "admin123":  # Defina sua senha aqui
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.sidebar.error("Senha incorreta.")
    return False

acesso_liberado = check_login()

uploaded_file = None

if acesso_liberado:
    st.sidebar.header("Importar Dados")
    uploaded_file = st.sidebar.file_uploader("Carregar arquivo (CSV ou Excel)", type=['csv', 'xlsx'])

    # --- FORMULÁRIO DE INSERÇÃO ---
    st.sidebar.markdown("---")
    st.sidebar.header("Inserir Dados Manualmente")
    with st.sidebar.form("form_insercao"):
        f_data = st.date_input("Data", format="DD/MM/YYYY")
        f_transp = st.text_input("Transportadora")
        f_op = st.selectbox("Operação", ["LML", "Direta", "Reversa", "Outros"])
        f_lib = st.number_input("Liberados (Vol)", min_value=0, step=1)
        f_malha = st.number_input("Malha (Qtd)", min_value=0, step=1)
        
        btn_salvar = st.form_submit_button("Salvar Registro")
        
        if btn_salvar:
            new_row = {'DATA': [pd.to_datetime(f_data)], 'TRANSPORTADORA': [f_transp], 'LIBERADOS': [f_lib], 'MALHA': [f_malha], 'OPERAÇÃO': [f_op]}
            df_new = pd.DataFrame(new_row)
            
            try:
                # Salva no banco de dados
                df_new.to_sql(TABLE_NAME, engine, if_exists='append', index=False)
                # Atualiza session state
                st.session_state['df_dados'] = pd.concat([st.session_state['df_dados'], df_new], ignore_index=True)
                st.success("Salvo no Banco de Dados com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao salvar no banco: {e}")

df = load_data(uploaded_file)

if df is None or df.empty:
    st.info("O banco de dados está vazio. Utilize o menu lateral para carregar um arquivo ou inserir dados manualmente.")
    st.stop()

if acesso_liberado:
    # Botão para salvar dados importados no banco (aparece apenas se houver upload)
    if uploaded_file is not None:
        replace_data = st.sidebar.checkbox("Substituir todo o banco de dados", help="Marque para apagar o banco atual e criar um novo com este arquivo.")
        if st.sidebar.button("💾 Converter/Salvar em dados.db"):
            save_uploaded_data(df, replace=replace_data)

    # Botão para baixar o banco de dados atualizado
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        temp_engine = create_engine(f"sqlite:///{tmp.name}")
        st.session_state['df_dados'].to_sql(TABLE_NAME, temp_engine, if_exists='replace', index=False)
        
        with open(tmp.name, "rb") as fp:
            st.sidebar.download_button(
                label="📥 Baixar dados.db (Backup)",
                data=fp,
                file_name="dados.db",
                mime="application/x-sqlite3"
            )

    st.sidebar.header("Filtros")

    # Filtro de Data
    min_date = df['DATA'].min()
    max_date = df['DATA'].max()
    start_date, end_date = st.sidebar.date_input(
        "Selecione o Período",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date,
        format="DD/MM/YYYY"
    )

    # Filtro de Operação
    operacoes = st.sidebar.multiselect(
        "Tipo de Operação",
        options=df['OPERAÇÃO'].unique(),
        default=df['OPERAÇÃO'].unique()
    )

    # Filtro de Transportadora
    transportadoras = st.sidebar.multiselect(
        "Transportadora",
        options=df['TRANSPORTADORA'].unique(),
        default=df['TRANSPORTADORA'].unique()
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("Desenvolvido por **Clayton S. Silva**")

else:
    # --- MODO LEITURA (SEM LOGIN) ---
    # Define filtros padrão para que o dashboard funcione
    min_date = df['DATA'].min()
    max_date = df['DATA'].max()
    start_date, end_date = min_date, max_date
    operacoes = df['OPERAÇÃO'].unique()
    transportadoras = df['TRANSPORTADORA'].unique()
    
    st.sidebar.info("ℹ️ Faça login para acessar filtros e ferramentas de edição.")

# Aplicar Filtros
df_filtered = df[
    (df['DATA'] >= pd.to_datetime(start_date)) &
    (df['DATA'] <= pd.to_datetime(end_date)) &
    (df['OPERAÇÃO'].isin(operacoes)) &
    (df['TRANSPORTADORA'].isin(transportadoras))
].copy()

# Criar colunas de período
df_filtered['Mês_Ano'] = df_filtered['DATA'].dt.strftime('%Y-%m')
df_filtered['Ano'] = df_filtered['DATA'].dt.strftime('%Y')

# --- 3. DASHBOARD PRINCIPAL ---
if logo_image:
    st.image(logo_image, width=200)

st.title("📊 Dashboard Controle de Malha fina e Liberados 2026")

# KPIs
total_liberados = df_filtered['LIBERADOS'].sum()
total_malha = df_filtered['MALHA'].sum()
total_veiculos = total_liberados + total_malha
taxa_malha_global = (total_malha / total_veiculos * 100) if total_veiculos > 0 else 0
media_liberados = df_filtered['LIBERADOS'].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Fluxo Total (Veículos)", f"{total_veiculos:,.0f}")
col2.metric("Veículos Liberados", f"{total_liberados:,.0f}")
col3.metric("Retidos em Malha", f"{total_malha:,.0f}")
col4.metric("Taxa de Retenção Global", f"{taxa_malha_global:.2f}%")

st.markdown("---")

st.subheader("🏆 Rankings")
col_r1, col_r2 = st.columns(2)

with col_r1:
    top_vol = df_filtered.groupby('TRANSPORTADORA')['LIBERADOS'].sum().reset_index().sort_values(by='LIBERADOS', ascending=True)
    fig_top_vol = px.bar(top_vol, x='LIBERADOS', y='TRANSPORTADORA', orientation='h', text_auto=True, title="Ranking de Fluxo (Veículos Liberados)", color='LIBERADOS', color_continuous_scale='Teal')
    fig_top_vol.update_traces(textfont_size=14)
    fig_top_vol.update_layout(template="plotly_white", xaxis_title="Volume Liberado", yaxis_title=None, showlegend=False)
    st.plotly_chart(fig_top_vol, key="rank_vol", width="stretch")
    st.caption("📝 **Fluxo:** Volume total de veículos que saíram liberados (sem auditoria).")

with col_r2:
    top_malha = df_filtered.groupby('TRANSPORTADORA')['MALHA'].sum().reset_index().sort_values(by='MALHA', ascending=True)
    fig_top_malha = px.bar(top_malha, x='MALHA', y='TRANSPORTADORA', orientation='h', text_auto=True, title="Ranking de Retenção (Malha Fina)", color='MALHA', color_continuous_scale='Reds')
    fig_top_malha.update_traces(textfont_size=14)
    fig_top_malha.update_layout(template="plotly_white", xaxis_title="Qtd. Veículos Retidos", yaxis_title=None, showlegend=False)
    st.plotly_chart(fig_top_malha, key="rank_malha", width="stretch")
    st.caption("📝 **Retenção:** Quantidade absoluta de veículos parados para auditoria (Malha Fina).")

# Abas para análises
tab_geral, tab_dia, tab_mes, tab_ano = st.tabs(["🔍 Visão Geral", "📅 Visão Diária", "📆 Visão Mensal", "📅 Visão Anual"])

with tab_geral:
    st.subheader("Visão Geral Integrada")
    
    # Filtro Semana Atual
    filtrar_semana_g = st.checkbox("Filtrar Semana Atual", value=True, key="chk_semana_geral")
    df_dia_geral = df_filtered.copy()
    if filtrar_semana_g and not df_dia_geral.empty:
        max_date_g = df_dia_geral['DATA'].max()
        start_of_week_g = max_date_g - pd.Timedelta(days=max_date_g.weekday())
        df_dia_geral = df_dia_geral[df_dia_geral['DATA'] >= start_of_week_g]

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        fig_vol_dia_g = px.bar(df_dia_geral, x='DATA', y='LIBERADOS', color='TRANSPORTADORA', barmode='group', title="Fluxo de Saída (Liberados) por Dia", text_auto=True)
        fig_vol_dia_g.update_xaxes(tickformat="%d/%m/%Y")
        fig_vol_dia_g.update_traces(textfont_size=14)
        fig_vol_dia_g.update_layout(template="plotly_white", xaxis_title="Data", yaxis_title="Volume")
        st.plotly_chart(fig_vol_dia_g, key="geral_vol_dia", width="stretch")
        st.caption("📊 **Volume Operacional:** Quantidade de veículos liberados dia a dia.")
    with col_g2:
        df_dia_malha_g = df_dia_geral.groupby(['DATA', 'TRANSPORTADORA'])[['LIBERADOS', 'MALHA']].sum().reset_index()
        # Cálculo da Taxa de Retenção (%)
        df_dia_malha_g['TOTAL_VEICULOS'] = df_dia_malha_g['LIBERADOS'] + df_dia_malha_g['MALHA']
        df_dia_malha_g['MALHA_PCT'] = df_dia_malha_g.apply(lambda row: 0 if row['TOTAL_VEICULOS'] == 0 else (int((row['MALHA'] / row['TOTAL_VEICULOS'] * 100) * 10 + 0.5) / 10.0), axis=1)
        
        fig_malha_dia_g = px.bar(df_dia_malha_g, x='DATA', y='MALHA_PCT', color='TRANSPORTADORA', title="Taxa de Retenção (Malha Fina) % por Dia")
        fig_malha_dia_g.update_xaxes(tickformat="%d/%m/%Y")
        fig_malha_dia_g.update_traces(texttemplate='%{y:.1f}%', textposition='auto', textfont_size=14)
        fig_malha_dia_g.update_layout(template="plotly_white", xaxis_title="Data", yaxis_title="Retenção (%)")
        st.plotly_chart(fig_malha_dia_g, key="geral_malha_dia", width="stretch")
        st.caption("🛡️ **Intensidade da Fiscalização:** Porcentagem de veículos auditados em relação ao total de saídas.")
    
    st.markdown("---")
    st.subheader("Distribuição Operacional")
    col_g3, col_g4 = st.columns(2)
    with col_g3:
        fig_pie_op = px.pie(df_dia_geral, names='OPERAÇÃO', values='LIBERADOS', title="Volume por Operação", hole=0.4)
        fig_pie_op.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie_op, key="pie_op", width="stretch")
    with col_g4:
        fig_pie_transp = px.pie(df_dia_geral, names='TRANSPORTADORA', values='LIBERADOS', title="Share de Volume por Transportadora", hole=0.4)
        fig_pie_transp.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig_pie_transp, key="pie_transp", width="stretch")

with tab_dia:
    st.subheader("Análise Diária")
    
    # Filtro Independente
    modo_filtro = st.radio("Modo de Visualização:", ["Semana Atual (Automático)", "Selecionar Dia Específico (Independente)"], horizontal=True)
    
    if "Independente" in modo_filtro:
        # Cria um dataframe base ignorando o filtro de data global, mas mantendo filtros de categoria
        df_base_indep = df[
            (df['OPERAÇÃO'].isin(operacoes)) &
            (df['TRANSPORTADORA'].isin(transportadoras))
        ].copy()
        
        if not df_base_indep.empty:
            datas_disponiveis = sorted(df_base_indep['DATA'].dt.date.unique())
            data_selecionada = st.date_input(
                "Selecione a Data:", 
                value=datas_disponiveis[-1], 
                min_value=min(datas_disponiveis), 
                max_value=max(datas_disponiveis)
            )
            df_dia_view = df_base_indep[df_base_indep['DATA'].dt.date == data_selecionada]
        else:
            df_dia_view = pd.DataFrame()
            st.warning("Não há dados disponíveis para os filtros de Operação/Transportadora selecionados.")
    else:
        # Lógica original (Semana Atual baseada no filtro global)
        df_dia_view = df_filtered.copy()
        if not df_dia_view.empty:
            max_date = df_dia_view['DATA'].max()
            start_of_week = max_date - pd.Timedelta(days=max_date.weekday())
            df_dia_view = df_dia_view[df_dia_view['DATA'] >= start_of_week]

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        fig_vol_dia = px.bar(df_dia_view, x='DATA', y='LIBERADOS', color='TRANSPORTADORA', barmode='group', title="Fluxo de Saída (Liberados) por Dia", text_auto=True)
        fig_vol_dia.update_xaxes(tickformat="%d/%m/%Y")
        fig_vol_dia.update_traces(textfont_size=14)
        fig_vol_dia.update_layout(template="plotly_white", xaxis_title="Data", yaxis_title="Volume")
        st.plotly_chart(fig_vol_dia, key="dia_vol", width="stretch")
        st.caption("📊 **Volume:** Quantidade de veículos liberados por dia.")
    with col_d2:
        df_dia_malha = df_dia_view.groupby(['DATA', 'TRANSPORTADORA'])[['LIBERADOS', 'MALHA']].sum().reset_index()
        # Cálculo da Taxa de Retenção (%)
        df_dia_malha['TOTAL_VEICULOS'] = df_dia_malha['LIBERADOS'] + df_dia_malha['MALHA']
        df_dia_malha['MALHA_PCT'] = df_dia_malha.apply(lambda row: 0 if row['TOTAL_VEICULOS'] == 0 else (int((row['MALHA'] / row['TOTAL_VEICULOS'] * 100) * 10 + 0.5) / 10.0), axis=1)
        
        fig_malha_dia = px.bar(df_dia_malha, x='DATA', y='MALHA_PCT', color='TRANSPORTADORA', title="Taxa de Retenção (Malha Fina) % por Dia")
        fig_malha_dia.update_xaxes(tickformat="%d/%m/%Y")
        fig_malha_dia.update_traces(texttemplate='%{y:.1f}%', textposition='auto', textfont_size=14)
        fig_malha_dia.update_layout(template="plotly_white", xaxis_title="Data", yaxis_title="Retenção (%)")
        st.plotly_chart(fig_malha_dia, key="dia_malha", width="stretch")
        st.caption("🛡️ **Auditoria:** % de veículos retidos sobre o total.")

with tab_mes:
    st.subheader("Análise Mensal")
    
    # Filtro de Meses
    meses_disponiveis = sorted(df_filtered['Mês_Ano'].unique())
    # Define padrão como os últimos 3 meses
    padrao_meses = meses_disponiveis[-3:] if len(meses_disponiveis) >= 3 else meses_disponiveis
    meses_selecionados = st.multiselect("Selecione os Meses para Visualizar:", options=meses_disponiveis, default=padrao_meses)
    
    if meses_selecionados:
        df_mes_filtered = df_filtered[df_filtered['Mês_Ano'].isin(meses_selecionados)]
    else:
        df_mes_filtered = df_filtered
        
    df_mes = df_mes_filtered.groupby(['Mês_Ano', 'TRANSPORTADORA'])[['LIBERADOS', 'MALHA']].sum().reset_index()
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        fig_vol_mes = px.bar(df_mes, x='Mês_Ano', y='LIBERADOS', color='TRANSPORTADORA', barmode='group', title="Fluxo de Saída (Liberados) por Mês", text_auto=True)
        fig_vol_mes.update_traces(textfont_size=14)
        fig_vol_mes.update_layout(template="plotly_white", xaxis_title="Mês", yaxis_title="Volume")
        st.plotly_chart(fig_vol_mes, key="mes_vol", width="stretch")
        st.caption("📊 **Sazonalidade:** Volume acumulado de liberados por mês.")
    with col_m2:
        # Cálculo da Taxa de Retenção (%)
        df_mes['TOTAL_VEICULOS'] = df_mes['LIBERADOS'] + df_mes['MALHA']
        df_mes['MALHA_PCT'] = df_mes.apply(lambda row: 0 if row['TOTAL_VEICULOS'] == 0 else (int((row['MALHA'] / row['TOTAL_VEICULOS'] * 100) * 10 + 0.5) / 10.0), axis=1)
        
        fig_malha_mes = px.bar(df_mes, x='Mês_Ano', y='MALHA_PCT', color='TRANSPORTADORA', title="Taxa de Retenção (Malha Fina) % por Mês")
        fig_malha_mes.update_traces(texttemplate='%{y:.1f}%', textposition='auto', textfont_size=14)
        fig_malha_mes.update_layout(template="plotly_white", xaxis_title="Mês", yaxis_title="Retenção (%)")
        st.plotly_chart(fig_malha_mes, key="mes_malha", width="stretch")
        st.caption("🛡️ **Tendência:** Variação mensal da taxa de retenção na malha fina.")

with tab_ano:
    st.subheader("Análise Anual")
    df_ano = df_filtered.groupby(['Ano', 'TRANSPORTADORA'])[['LIBERADOS', 'MALHA']].sum().reset_index()
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        fig_vol_ano = px.bar(df_ano, x='Ano', y='LIBERADOS', color='TRANSPORTADORA', barmode='group', title="Fluxo de Saída (Liberados) por Ano", text_auto=True)
        fig_vol_ano.update_traces(textfont_size=14)
        fig_vol_ano.update_layout(template="plotly_white", xaxis_title="Ano", yaxis_title="Volume")
        st.plotly_chart(fig_vol_ano, key="ano_vol", width="stretch")
        st.caption("📊 **Histórico:** Volume total de liberados por ano.")
    with col_a2:
        # Cálculo da Taxa de Retenção (%)
        df_ano['TOTAL_VEICULOS'] = df_ano['LIBERADOS'] + df_ano['MALHA']
        df_ano['MALHA_PCT'] = df_ano.apply(lambda row: 0 if row['TOTAL_VEICULOS'] == 0 else (int((row['MALHA'] / row['TOTAL_VEICULOS'] * 100) * 10 + 0.5) / 10.0), axis=1)
        
        fig_malha_ano = px.bar(df_ano, x='Ano', y='MALHA_PCT', color='TRANSPORTADORA', title="Taxa de Retenção (Malha Fina) % por Ano")
        fig_malha_ano.update_traces(texttemplate='%{y:.1f}%', textposition='auto', textfont_size=14)
        fig_malha_ano.update_layout(template="plotly_white", xaxis_title="Ano", yaxis_title="Retenção (%)")
        st.plotly_chart(fig_malha_ano, key="ano_malha", width="stretch")
        st.caption("🛡️ **Consolidado:** Taxa média anual de retenção para auditoria.")

# --- 4. TABELA DE DADOS ---
with st.expander("Ver Dados Detalhados"):
    # Prepara dataframe para exibição com cálculos idênticos ao Excel
    df_display = df_filtered.copy()
    df_display['TOTAL'] = df_display['LIBERADOS'] + df_display['MALHA']
    
    # Aplica a lógica de arredondamento (Round Half Up) para 1 casa decimal
    df_display['% MALHA'] = df_display.apply(
        lambda row: 0 if row['TOTAL'] == 0 else (int((row['MALHA'] / row['TOTAL'] * 100) * 10 + 0.5) / 10.0), 
        axis=1
    )

    st.dataframe(
        df_display.sort_values(by=['DATA', 'TRANSPORTADORA']),
        width="stretch",
        column_config={
            "DATA": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
            "% MALHA": st.column_config.NumberColumn("% Malha", format="%.1f%%"),
            "TOTAL": st.column_config.NumberColumn("Total", format="%d")
        }
    )

# Assinatura
st.markdown("---")
st.markdown("<div style='text-align: center'>Desenvolvido por <b>Clayton S. Silva</b></div>", unsafe_allow_html=True)



##  streamlit run app.py
