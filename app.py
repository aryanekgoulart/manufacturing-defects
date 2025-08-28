import streamlit as st
import pandas as pd
import plotly.express as px

# Título da página, o ícone e o layout para ocupar a largura inteira.
st.set_page_config(
    page_title="Dashboard de Defeitos de Fabricação",
    page_icon="📊",
    layout="wide",
)

# --- Carregamento dos dados ---
df = pd.read_csv("https://raw.githubusercontent.com/aryanekgoulart/manufacturing-defects/refs/heads/main/defects_data_final.csv")

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

# Filtro de Ano/Mês
ano_mes_disponiveis = sorted(df['ano_mes'].unique())
ano_mes_selecionados = st.sidebar.multiselect("Ano/Mês", ano_mes_disponiveis, default=ano_mes_disponiveis)

# Filtro de Tipos de Defeitos
tipo_defeito_disponiveis = sorted(df['tipo_defeito'].unique())
tipo_defeito_selecionadas = st.sidebar.multiselect("Tipos de Defeitos", tipo_defeito_disponiveis, default=tipo_defeito_disponiveis)

# Filtro por Local de Defeito
local_defeito_disponiveis = sorted(df['local_defeito'].unique())
local_defeito_selecionados = st.sidebar.multiselect("Local de Defeito", local_defeito_disponiveis, default=local_defeito_disponiveis)

# Filtro por Gravidade
gravidade_disponiveis = sorted(df['gravidade'].unique())
gravidade_selecionados = st.sidebar.multiselect("Gravidade", gravidade_disponiveis, default=gravidade_disponiveis)

# Filtro por Método de Detecção
metodo_inspecao_disponiveis = sorted(df['metodo_inspecao'].unique())
metodo_inspecao_selecionados = st.sidebar.multiselect("Método de Inspeção", metodo_inspecao_disponiveis, default=metodo_inspecao_disponiveis)

# --- Filtragem do DataFrame ---
# O dataframe principal é filtrado com base nas seleções feitas na barra lateral.
df_filtrado = df[
    (df['ano_mes'].isin(ano_mes_selecionados)) &
    (df['tipo_defeito'].isin(tipo_defeito_selecionadas)) &
    (df['local_defeito'].isin(local_defeito_selecionados)) &
    (df['gravidade'].isin(gravidade_disponiveis)) &
    (df['metodo_inspecao'].isin(metodo_inspecao_selecionados))
]

# --- Conteúdo Principal ---
st.title("🎲 Defeitos de Fabricação")
st.markdown("Este conjunto de dados contém dados simulados relacionados a defeitos de fabricação observados durante processos de controle de qualidade. " \
"Inclui informações como tipo de defeito, data de detecção, localização no produto, nível de gravidade, método de inspeção utilizado e custos de reparo. " \
"Utilize os filtros à esquerda para refinar sua análise.")

# --- Métricas Principais (KPIs) ---
st.subheader("Métricas gerais (em USD)")

if not df_filtrado.empty:
    custo_total = df_filtrado['custo_reparo'].sum()
    media_custo = df_filtrado['custo_reparo'].mean()
    total_defeitos = df_filtrado.value_counts().sum()
    produto_com_mais_defeito = df_filtrado["id_produto"].mode()[0]
else:
    custo_total, media_custo, total_defeitos, produto_com_mais_defeito = 0, 0, 0, ""

col1, col2, col3, col4 = st.columns(4)
col1.metric("Custo Total", f"${custo_total:,.0f}")
col2.metric("Média de Custo", f"${media_custo:,.0f}")
col3.metric("Total de registros", f"{total_defeitos:}")
col4.metric("ID Produto mais frequente", produto_com_mais_defeito)

st.markdown("---")

# --- Análises Descritivas / VAR ---
# --- AGRUPAMENTOS RESPEITANDO O FILTRO ---

# Top produtos por defeito
id_produto = df_filtrado.groupby("id_produto").agg(
    defect_count=('id_produto', 'count'),
    total_custo_reparo=('custo_reparo', 'sum')
).sort_values(by='defect_count', ascending=False).reset_index()

top_10 = id_produto.sort_values(by='defect_count', ascending=False).head(10).copy()

# Custo de reparo por mês
custo_reparo_mes = df_filtrado.groupby('ano_mes').agg(
    total_custo_reparo=('custo_reparo', 'sum')
).reset_index()

# Tipo de defeito + local + gravidade
tipo_defeito = df_filtrado.groupby(['tipo_defeito', 'local_defeito', 'gravidade']).agg(
    defect_count=('id_defeito', 'count'),
    total_custo_reparo=('custo_reparo', 'sum')
).reset_index()

# --- Análises Visuais com Plotly ---
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_10["id_produto"] = top_10["id_produto"].astype(str)
        top_10_defeitos = px.bar(
            top_10,
            x="id_produto",
            y="defect_count",
            title="Top 10: Número de Defeitos",
            labels={"id_produto": "ID Produto", "defect_count": "Número de Defeitos"},
            color="defect_count",
            color_continuous_scale="viridis",
            height=470,
            width=600
        )
        top_10_defeitos.update_layout(
            xaxis=dict(type="category", categoryorder="total descending")  # força categórico
        )
        st.plotly_chart(top_10_defeitos, use_container_width=True, key="grafico_top10_produtos")
    else:
        st.warning("Nenhum dado para exibir no gráfico de produtos.")



with col_graf2:
    if not df_filtrado.empty:
        distr_ano_mes = px.area(custo_reparo_mes, x='ano_mes', y='total_custo_reparo',
                title='Custo de Reparo por Ano/Mês',
                labels={'ano_mes': 'Mês/Ano', 'total_custo_reparo': 'Custo'},
                color_discrete_sequence=px.colors.sequential.Viridis,
                text='total_custo_reparo',
                height=470, width=600)
        distr_ano_mes.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(distr_ano_mes, use_container_width=True, key="grafico_distribuicao_ano_mes")
    else:
        st.warning("Nenhum dado para exibir no gráfico de tipos de defeitos.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        tipo_frequencia = px.bar(tipo_defeito, x='tipo_defeito', y='defect_count', color='local_defeito',
                title='Tipo de Defeito x Frequência',
                labels={'tipo_defeito': 'Tipo de Defeito', 'defect_count': 'Frequência', 'local_defeito': 'Local do Defeito'},
                height=400, 
                width=600, 
                color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(tipo_frequencia, use_container_width=True, key="grafico_tipo_frequencia")
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

with col_graf4:
    if not df_filtrado.empty:
        gravidade_frequencia = px.bar(tipo_defeito, x='gravidade', y='defect_count', color='local_defeito',
                title='Gravidade x Frequência',
                labels={'gravidade': 'Gravidade', 'defect_count': 'Frequência', 'local_defeito': 'Local do Defeito'},
                height=400, 
                width=600, 
                color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(gravidade_frequencia, use_container_width=True, key="grafico_gravidade_frequencia")
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.")

# --- Tabela de Dados Detalhados ---
st.subheader("Dados Detalhados")

st.dataframe(df_filtrado)

