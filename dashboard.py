import streamlit as st
import pandas as pd
import plotly.express as px
import io
import os
import socket
from urllib.parse import urlparse, urlunparse
from sqlalchemy import create_engine, text

# Configuração da página
st.set_page_config(page_title="Dashboard de Logística", layout="wide")

# --- 1. CARREGAMENTO E TRATAMENTO DE DADOS ---

# CONFIGURAÇÃO DO BANCO DE DADOS

# Tenta carregar a URL dos segredos (para quando estiver Online/Seguro)
try:
    DATABASE_URL = st.secrets["DATABASE_URL"]
except Exception:
    # Fallback ou erro se não encontrar os segredos.
    # Para rodar localmente, crie um arquivo .streamlit/secrets.toml
    st.error("A configuração DATABASE_URL não foi encontrada nos segredos (st.secrets).")
    st.stop()

@st.cache_resource
def get_database_engine(url):
    """
    Cria a engine do banco de dados com cache e força IPv4 para evitar erros de conexão
    com Supabase em redes que priorizam IPv6 incorretamente.
    """
    try:
        # Tenta resolver o hostname para IPv4 explicitamente
        parsed = urlparse(url)
        hostname = parsed.hostname
        if hostname and not hostname.replace('.', '').isdigit():
            ip_v4 = None
            # Tentativa 1: gethostbyname (mais simples e direto)
            try:
                ip_v4 = socket.gethostbyname(hostname)
            except Exception:
                # Tentativa 2: getaddrinfo (fallback)
                try:
                    infos = socket.getaddrinfo(hostname, 5432, family=socket.AF_INET)
                    if infos:
                        ip_v4 = infos[0][4][0]
                except Exception as e:
                    print(f"Falha secundária DNS: {e}")
                    pass
            
            if ip_v4:
                new_netloc = parsed.netloc.replace(hostname, ip_v4)
                url = urlunparse(parsed._replace(netloc=new_netloc))
                print(f"Conexão forçada via IPv4: {hostname} -> {ip_v4}")
            else:
                st.error(f"⚠️ ERRO DE REDE: Não foi possível encontrar o servidor {hostname}. Verifique se seu projeto no Supabase não está PAUSADO.")
    except Exception as e:
        print(f"Erro ao resolver DNS: {e}")
    
    return create_engine(url, pool_pre_ping=True)

engine = get_database_engine(DATABASE_URL)
TABLE_NAME = 'performance_logistica'

@st.cache_data
def load_data(uploaded_file=None):
    df = None
    # 1. Tenta carregar do upload
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, sep=None, engine='python', decimal=',')
            else:
                df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")
            return None
    # 2. Tenta carregar do Banco de Dados SQL
    else:
        try:
            df = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", con=engine)
        except Exception:
            # Se a tabela não existir (primeira execução), retorna None ou DataFrame vazio
            return None

    if df is None:
        return None
    
    # Padronizar nomes das colunas (remover espaços e maiúsculas) para evitar KeyError
    if df is not None:
        df.columns = df.columns.str.strip().str.upper()

    # Converter coluna DATA para datetime
    if 'DATA' in df.columns:
        df['DATA'] = pd.to_datetime(df['DATA'], dayfirst=True, errors='coerce')

    # Garantir que colunas numéricas sejam números (corrige erro de soma de strings)
    for col in ['LIBERADOS', 'MALHA']:
        if col in df.columns:
            # Remove pontos de milhar se existirem como string antes de converter
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.')
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    return df


# --- 2. BARRA LATERAL (UPLOAD E FILTROS) ---
#st.sidebar.header("Logo / Imagem")

# Tenta carregar logo localmente (logo.png, logo.jpg, etc.)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Busca arquivos no diretório de forma insensível a maiúsculas/minúsculas (importante para Linux/Streamlit Cloud)
files_in_dir = os.listdir(script_dir)
possible_logos = ["logo.png", "logo.jpg", "logo.jpeg"]
found_logo = next((f for f in files_in_dir if f.lower() in possible_logos), None)
local_logo = os.path.join(script_dir, found_logo) if found_logo else None

logo_image = None
if local_logo:
    logo_image = local_logo
    st.sidebar.image(local_logo)
else:
    logo = st.sidebar.file_uploader("Carregar Logo", type=['png', 'jpg', 'jpeg'])
    if logo:
        logo_image = logo
        st.sidebar.image(logo)

st.sidebar.header("Importar Dados")
uploaded_file = st.sidebar.file_uploader("Carregar arquivo (CSV ou Excel)", type=['csv', 'xlsx'])

# --- FORMULÁRIO DE INSERÇÃO ---
st.sidebar.markdown("---")
st.sidebar.header("Inserir Dados Manualmente")
with st.sidebar.form("form_insercao"):
    f_data = st.date_input("Data", format="DD/MM/YYYY")
    f_transp = st.text_input("Transportadora")
    f_op = st.selectbox("Operação", ["LML", "Direta"])
    f_lib = st.number_input("Liberados (Vol)", min_value=0, step=1)
    f_malha = st.number_input("Malha (Qtd)", min_value=0, step=1)
    
    btn_salvar = st.form_submit_button("Salvar Registro")
    
    if btn_salvar:
        # Prepara os dados. Nota: Para SQL, é melhor salvar a data em formato ISO (YYYY-MM-DD) ou datetime object
        new_row = {'DATA': [pd.to_datetime(f_data)], 'TRANSPORTADORA': [f_transp], 'LIBERADOS': [f_lib], 'MALHA': [f_malha], 'OPERAÇÃO': [f_op]}
        df_new = pd.DataFrame(new_row)
        
        try:
            # Salva no banco de dados (append adiciona ao final)
            df_new.to_sql(TABLE_NAME, engine, if_exists='append', index=False)
            st.success("Salvo no Banco de Dados com sucesso!")
            load_data.clear() # Limpa o cache para recarregar os dados novos
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao salvar no banco: {e}")

df = load_data(uploaded_file)

if df is None:
    st.stop()

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

# Assinatura do Desenvolvedor
st.sidebar.markdown("---")
st.sidebar.markdown("Desenvolvido por **Clayton S. Silva**")

# Aplicar Filtros
df_filtered = df[
    (df['DATA'] >= pd.to_datetime(start_date)) &
    (df['DATA'] <= pd.to_datetime(end_date)) &
    (df['OPERAÇÃO'].isin(operacoes)) &
    (df['TRANSPORTADORA'].isin(transportadoras))
].copy()

# Criar colunas de período para agrupamento
df_filtered['Mês_Ano'] = df_filtered['DATA'].dt.strftime('%Y-%m')
df_filtered['Ano'] = df_filtered['DATA'].dt.strftime('%Y')

# --- 3. DASHBOARD PRINCIPAL ---
if logo_image:
    st.image(logo_image, width=200)

st.title("📊 Dashboard de Performance Logística")

# KPIs (Indicadores Chave)
total_liberados = df_filtered['LIBERADOS'].sum()
total_malha = df_filtered['MALHA'].sum()
media_liberados = df_filtered['LIBERADOS'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Liberados (Vol)", f"{total_liberados:,.0f}")
col2.metric("Total Malha (Qtd)", f"{total_malha:,.0f}")
col3.metric("Média Diária por Transp.", f"{media_liberados:.1f}")

st.markdown("---")

st.subheader("🏆 Rankings")
col_r1, col_r2 = st.columns(2)

with col_r1:
    top_vol = df_filtered.groupby('TRANSPORTADORA')['LIBERADOS'].sum().reset_index().sort_values(by='LIBERADOS', ascending=True)
    fig_top_vol = px.bar(top_vol, x='LIBERADOS', y='TRANSPORTADORA', orientation='h', text_auto=True,
                         title="Top Volume (Liberados)")
    st.plotly_chart(fig_top_vol, key="rank_vol")

with col_r2:
    top_malha = df_filtered.groupby('TRANSPORTADORA')['MALHA'].sum().reset_index().sort_values(by='MALHA', ascending=True)
    fig_top_malha = px.bar(top_malha, x='MALHA', y='TRANSPORTADORA', orientation='h', text_auto=True,
                           title="Top Frequência na Malha")
    st.plotly_chart(fig_top_malha, key="rank_malha")

# Abas para análises temporais (Dia, Mês, Ano)
tab_geral, tab_dia, tab_mes, tab_ano = st.tabs(["🔍 Visão Geral", "📅 Visão Diária", "📆 Visão Mensal", "📅 Visão Anual"])

with tab_geral:
    st.subheader("Visão Geral Integrada")
    
    # --- Seção Diária ---
    st.markdown("#### 📅 Indicadores Diários")
    
    # Filtro Padrão: Semana Atual (Visão Geral)
    filtrar_semana_g = st.checkbox("Filtrar Semana Atual", value=True, key="chk_semana_geral")
    df_dia_geral = df_filtered.copy()
    if filtrar_semana_g and not df_dia_geral.empty:
        max_date_g = df_dia_geral['DATA'].max()
        start_of_week_g = max_date_g - pd.Timedelta(days=max_date_g.weekday())
        df_dia_geral = df_dia_geral[df_dia_geral['DATA'] >= start_of_week_g]

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        fig_vol_dia_g = px.bar(df_dia_geral, x='DATA', y='LIBERADOS', color='TRANSPORTADORA',
                             title="Volume Liberado por Dia", 
                             labels={'LIBERADOS': 'Volume', 'DATA': 'Data'},
                             text_auto=True)
        st.plotly_chart(fig_vol_dia_g, key="geral_vol_dia")
    with col_g2:
        df_dia_malha_g = df_dia_geral.groupby(['DATA', 'TRANSPORTADORA'])['MALHA'].sum().reset_index()
        df_dia_malha_g['MALHA_PCT'] = df_dia_malha_g.groupby('DATA')['MALHA'].transform(lambda x: (x / x.sum() * 100) if x.sum() > 0 else 0)
        fig_malha_dia_g = px.bar(df_dia_malha_g, x='DATA', y='MALHA_PCT', color='TRANSPORTADORA',
                               title="Distribuição de Malha (%) por Dia",
                               labels={'MALHA_PCT': '% Malha', 'DATA': 'Data'},
                               text_auto='.1f')
        st.plotly_chart(fig_malha_dia_g, key="geral_malha_dia")
        
    st.markdown("---")
    
    # --- Seção Mensal ---
    st.markdown("#### 📆 Indicadores Mensais")
    
    # Filtro Padrão: Mês Atual e Anterior (Visão Geral)
    filtrar_mes_g = st.checkbox("Filtrar Mês Atual e Anterior", value=True, key="chk_mes_geral")
    df_mes_geral = df_filtered.copy()
    if filtrar_mes_g and not df_mes_geral.empty:
        max_date_mg = df_mes_geral['DATA'].max()
        start_date_mes_g = (max_date_mg.replace(day=1) - pd.DateOffset(months=1))
        df_mes_geral = df_mes_geral[df_mes_geral['DATA'] >= start_date_mes_g]

    df_mes_g = df_mes_geral.groupby(['Mês_Ano', 'TRANSPORTADORA'])[['LIBERADOS', 'MALHA']].sum().reset_index()
    col_g3, col_g4 = st.columns(2)
    with col_g3:
        fig_vol_mes_g = px.bar(df_mes_g, x='Mês_Ano', y='LIBERADOS', color='TRANSPORTADORA', barmode='group',
                             title="Total Liberados por Mês", text_auto=True)
        st.plotly_chart(fig_vol_mes_g, key="geral_vol_mes")
    with col_g4:
        df_mes_g['MALHA_PCT'] = df_mes_g.groupby('Mês_Ano')['MALHA'].transform(lambda x: (x / x.sum() * 100) if x.sum() > 0 else 0)
        fig_malha_mes_g = px.bar(df_mes_g, x='Mês_Ano', y='MALHA_PCT', color='TRANSPORTADORA',
                               title="Share de Malha (%) por Mês",
                               text_auto='.1f')
        st.plotly_chart(fig_malha_mes_g, key="geral_malha_mes")

    st.markdown("---")

    # --- Seção Anual ---
    st.markdown("#### 📅 Indicadores Anuais")
    df_ano_g = df_filtered.groupby(['Ano', 'TRANSPORTADORA'])[['LIBERADOS', 'MALHA']].sum().reset_index()
    fig_vol_ano_g = px.bar(df_ano_g, x='Ano', y='LIBERADOS', color='TRANSPORTADORA', barmode='group',
                            title="Total Liberados por Ano", text_auto=True)
    st.plotly_chart(fig_vol_ano_g, key="geral_vol_ano")


with tab_dia:
    st.subheader("Análise Diária")
    
    # Filtro Padrão: Semana Atual (baseado na maior data disponível)
    filtrar_semana = st.checkbox("Filtrar Semana Atual", value=True, key="chk_semana")
    df_dia_view = df_filtered.copy()
    
    if filtrar_semana and not df_dia_view.empty:
        max_date = df_dia_view['DATA'].max()
        # Calcula o início da semana (Segunda-feira)
        start_of_week = max_date - pd.Timedelta(days=max_date.weekday())
        df_dia_view = df_dia_view[df_dia_view['DATA'] >= start_of_week]

    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        # Total Liberados por Transportadora (Dia)
        fig_vol_dia = px.bar(df_dia_view, x='DATA', y='LIBERADOS', color='TRANSPORTADORA',
                             title="Volume Liberado por Dia (Por Transportadora)", 
                             labels={'LIBERADOS': 'Volume', 'DATA': 'Data'},
                             text_auto=True)
        st.plotly_chart(fig_vol_dia, key="dia_vol")
    
    with col_d2:
        # % Malha (Share)
        # Calcular porcentagem diária
        df_dia_malha = df_dia_view.groupby(['DATA', 'TRANSPORTADORA'])['MALHA'].sum().reset_index()
        df_dia_malha['MALHA_PCT'] = df_dia_malha.groupby('DATA')['MALHA'].transform(lambda x: (x / x.sum() * 100) if x.sum() > 0 else 0)
        fig_malha_dia = px.bar(df_dia_malha, x='DATA', y='MALHA_PCT', color='TRANSPORTADORA',
                               title="Distribuição de Malha (%) por Dia",
                               labels={'MALHA_PCT': '% Malha', 'DATA': 'Data'},
                               text_auto='.1f')
        st.plotly_chart(fig_malha_dia, key="dia_malha")

with tab_mes:
    st.subheader("Análise Mensal")
    
    # Filtro Padrão: Mês Atual e Anterior
    filtrar_mes = st.checkbox("Filtrar Mês Atual e Anterior", value=True, key="chk_mes")
    df_mes_view = df_filtered.copy()
    
    if filtrar_mes and not df_mes_view.empty:
        max_date = df_mes_view['DATA'].max()
        # Calcula o primeiro dia do mês anterior
        start_date_mes = (max_date.replace(day=1) - pd.DateOffset(months=1))
        df_mes_view = df_mes_view[df_mes_view['DATA'] >= start_date_mes]

    # Agrupamento por Mês
    df_mes = df_mes_view.groupby(['Mês_Ano', 'TRANSPORTADORA'])[['LIBERADOS', 'MALHA']].sum().reset_index()
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        fig_vol_mes = px.bar(df_mes, x='Mês_Ano', y='LIBERADOS', color='TRANSPORTADORA', barmode='group',
                             title="Total Liberados por Mês", text_auto=True)
        st.plotly_chart(fig_vol_mes, key="mes_vol")
    with col_m2:
        # Calcular porcentagem mensal
        df_mes['MALHA_PCT'] = df_mes.groupby('Mês_Ano')['MALHA'].transform(lambda x: (x / x.sum() * 100) if x.sum() > 0 else 0)
        fig_malha_mes = px.bar(df_mes, x='Mês_Ano', y='MALHA_PCT', color='TRANSPORTADORA',
                               title="Share de Malha (%) por Mês",
                               text_auto='.1f')
        st.plotly_chart(fig_malha_mes, key="mes_malha")

with tab_ano:
    st.subheader("Análise Anual")
    # Agrupamento por Ano
    df_ano = df_filtered.groupby(['Ano', 'TRANSPORTADORA'])[['LIBERADOS', 'MALHA']].sum().reset_index()
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        fig_vol_ano = px.bar(df_ano, x='Ano', y='LIBERADOS', color='TRANSPORTADORA', barmode='group',
                             title="Total Liberados por Ano", text_auto=True)
        st.plotly_chart(fig_vol_ano, key="ano_vol")
    with col_a2:
        # Calcular porcentagem anual
        df_ano['MALHA_PCT'] = df_ano.groupby('Ano')['MALHA'].transform(lambda x: (x / x.sum() * 100) if x.sum() > 0 else 0)
        fig_malha_ano = px.bar(df_ano, x='Ano', y='MALHA_PCT', color='TRANSPORTADORA',
                               title="Share de Malha (%) por Ano",
                               text_auto='.1f')
        st.plotly_chart(fig_malha_ano, key="ano_malha")

# --- 4. TABELA DE DADOS ---
with st.expander("Ver Dados Detalhados"):
    st.dataframe(df_filtered.sort_values(by=['DATA', 'TRANSPORTADORA']), width="stretch")

# Assinatura no rodapé da página principal
st.markdown("---")
st.markdown("<div style='text-align: center'>Desenvolvido por <b>Clayton S. Silva</b></div>", unsafe_allow_html=True)




#   streamlit run dashboard.py



