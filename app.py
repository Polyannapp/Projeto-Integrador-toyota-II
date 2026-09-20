import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. Configuração Avançada da Página
st.set_page_config(
    page_title="Portal Pós-Venda | Analytics", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Injeção de CSS Customizado (O segredo do Front-End robusto)
st.markdown("""
    <style>
    /* Esconde cabeçalho e rodapé padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Estilização dos Cartões de KPI (Métricas) */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #eb0a1e; /* Cor vermelha remetendo à marca */
    }
    
    /* Cor do texto principal */
    h1, h2, h3 {
        color: #333333;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Gerador de Dados Fictícios (Apenas para rodar o exemplo sem erro de arquivo)
# Substitua esta função pelo seu @st.cache_data que lê o Excel oficial
@st.cache_data
def carregar_dados():
    np.random.seed(42)
    dealers = ['Dealer Norte', 'Dealer Sul', 'Dealer Centro']
    familias = ['Corolla', 'Hilux', 'Yaris', 'RAV4']
    pagamentos = ['À Vista', 'Financiamento', 'Cartão de Crédito']
    
    dados = {
        'Nome Dealer': np.random.choice(dealers, 1000),
        'Familia de veiculo_ultima_compra': np.random.choice(familias, 1000),
        'Forma de Pagamento Preferencial': np.random.choice(pagamentos, 1000),
        'AOV': np.random.uniform(150, 4500, 1000), # Ticket Médio
        'Frequencia': np.random.randint(1, 10, 1000)
    }
    return pd.DataFrame(dados)

df = carregar_dados()

# 4. Construção da Sidebar Profissional
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e7/Toyota.svg", width=100) # Logo de exemplo
    st.markdown("### Painel de Controle RFM")
    st.markdown("---")
    
    dealers_selecionados = st.multiselect(
        "📍 Unidade Concessionária", 
        options=df['Nome Dealer'].unique(), 
        default=df['Nome Dealer'].unique()
    )
    
    familias_selecionadas = st.multiselect(
        "🚗 Família do Veículo", 
        options=df['Familia de veiculo_ultima_compra'].unique(), 
        default=df['Familia de veiculo_ultima_compra'].unique()
    )
    
    st.markdown("---")
    st.caption("Atualizado: Setembro 2026")

# Aplicação dos Filtros
df_filtrado = df[
    (df['Nome Dealer'].isin(dealers_selecionados)) & 
    (df['Familia de veiculo_ultima_compra'].isin(familias_selecionadas))
]

# 5. Corpo Principal do Dashboard
st.title("Performance de Pós-Venda e Comportamento")
st.markdown("Acompanhamento estratégico de retenção de clientes e ticket médio (AOV).")

# 6. Painel de KPIs (Métricas Flutuantes estilizadas via CSS)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de Registros", f"{len(df_filtrado):,}".replace(",", "."))
with col2:
    st.metric("Ticket Médio (AOV)", f"R$ {df_filtrado['AOV'].mean():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
with col3:
    st.metric("Frequência Média", f"{df_filtrado['Frequencia'].mean():.1f} visitas")
with col4:
    st.metric("Maior Ticket Gasto", f"R$ {df_filtrado['AOV'].max():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("<br>", unsafe_allow_html=True) # Espaço em branco

# 7. Organização em Abas (Tabs) para não poluir a tela
aba1, aba2, aba3 = st.tabs(["📊 Visão Geral", "💵 Formas de Pagamento", "📂 Base de Dados Bruta"])

with aba1:
    # Dois gráficos lado a lado usando containers
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        fig1 = px.histogram(
            df_filtrado, x="Familia de veiculo_ultima_compra", 
            color="Nome Dealer", barmode="group",
            title="Volume de Vendas por Veículo e Dealer",
            template="simple_white"
        )
        # Ajustes finos no Plotly para ficar mais limpo
        fig1.update_layout(xaxis_title="", yaxis_title="Quantidade")
        st.plotly_chart(fig1, use_container_width=True)
        
    with col_graf2:
        fig2 = px.box(
            df_filtrado, x="Familia de veiculo_ultima_compra", y="AOV",
            color="Familia de veiculo_ultima_compra",
            title="Distribuição do AOV (Monetary) por Veículo",
            template="simple_white"
        )
        fig2.update_layout(xaxis_title="", yaxis_title="Valor (R$)")
        st.plotly_chart(fig2, use_container_width=True)

with aba2:
    st.subheader("Análise de Preferência de Pagamento")
    fig3 = px.pie(
        df_filtrado, names="Forma de Pagamento Preferencial", values="AOV",
        title="Receita Total (AOV) por Forma de Pagamento",
        hole=0.4 # Transforma a torta em um gráfico de rosca (Donut) moderno
    )
    st.plotly_chart(fig3, use_container_width=True)

with aba3:
    st.subheader("Extração de Dados")
    st.markdown("Utilize o botão no cabeçalho da tabela para exportar para CSV.")
    # Tabela com barra de rolagem nativa e download
    st.dataframe(df_filtrado, use_container_width=True, height=400)