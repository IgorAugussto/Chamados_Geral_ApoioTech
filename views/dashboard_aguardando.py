# views/dashboard_aguardando.py
import streamlit as st
import plotly.express as px
import pandas as pd
import re

def mostrar_dashboard_aguardando(df):
    st.title("Dashboard Aguardando Aceite")
    
    # =========================================================
    # CORRIGE O CURSOR CHATO DO SELECTBOX
    # =========================================================
    st.markdown("""
    <style>
        /* Remove cursor de texto dos selectbox, multiselect e radio */
        div[data-baseweb="select"] > div:hover,
        div[data-baseweb="select"] > div,
        div[data-testid="stSelectbox"] > div:hover,
        div[data-testid="stMultiSelect"] > div:hover,
        div[data-testid="stRadio"] > div:hover {
            cursor: pointer !important;
        }
    
        /* Garante que o dropdown em si também tenha cursor normal */
        div[role="listbox"] {
            cursor: pointer !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # =========================================================
    # 1. KPI
    # =========================================================
    col1 = st.columns(3)[1]
    col1.metric("Chamados Totais (Abertos)", len(df))

    # =========================================================
    # 2. Botão de Atualização
    # =========================================================
    if st.button("Atualizar Dados do Google Sheets", key="refresh_google"):
        st.cache_data.clear()
        st.success("Dados atualizados manualmente!")
        st.rerun()

    # =========================================================
    # 3. EXTRAIR NÚMERO DA COLUNA "GERAL"
    # =========================================================
    def extrair_numero(texto):
        if pd.isna(texto):
            return None
        match = re.search(r'\((\d+)', str(texto))
        return int(match.group(1)) if match else None

    df["Geral_Numerico"] = df["Dias Restantes Geral"].apply(extrair_numero)

    # =========================================================
    # 4. FILTRO POR TÉCNICO (SIDEBAR)
    # =========================================================
    st.sidebar.header("Filtros")

    # Lista de técnicos únicos
    tecnicos_unicos = sorted([t for t in df["Técnico"].dropna().unique() if str(t).strip()])
    tecnico_filtro = st.sidebar.selectbox(
        "Filtrar por Técnico",
        options=["Todos"] + tecnicos_unicos,
        index=0,
        key="filtro_tecnico_sidebar"
    )

    # Aplica filtro
    if tecnico_filtro != "Todos":
        df_filtrado = df[df["Técnico"] == tecnico_filtro].copy()
    else:
        df_filtrado = df.copy()

        # =========================================================
    # 5. GRÁFICO: Barras Duplas → Dentro do Prazo vs Atrasados
    # =========================================================
    st.subheader("Distribuição por Status de Prazo")

    # Classifica os chamados
    df_filtrado["Status Prazo"] = df_filtrado["Geral_Numerico"].apply(
        lambda x: "Atrasado" if pd.notna(x) and x <= 0 else "Dentro do Prazo" if pd.notna(x) else "Sem Prazo"
    )

    # Conta por técnico e status
    df_grafico = (
        df_filtrado.groupby(["Técnico", "Status Prazo"])
        .size()
        .reset_index(name="Quantidade")
    )

    # Ordem desejada nas barras
    ordem_status = ["Dentro do Prazo", "Atrasado"]
    df_grafico["Status Prazo"] = pd.Categorical(
        df_grafico["Status Prazo"], categories=ordem_status, ordered=True
    )
    df_grafico = df_grafico.sort_values(["Técnico", "Status Prazo"])

    if not df_grafico.empty:
        fig = px.bar(
            df_grafico,
            x="Técnico",
            y="Quantidade",
            color="Status Prazo",
            title="Chamados Dentro do Prazo vs Atrasados por Técnico",
            barmode="group",
            color_discrete_map={
                "Dentro do Prazo": "#2ecc71",   # verde bonito
                "Atrasado": "#e74c3c"           # vermelho forte
            },
            text="Quantidade",
            category_orders={"Status Prazo": ordem_status}
        )

        fig.update_traces(textposition="outside")
        fig.update_layout(
            xaxis_title="Técnico",
            yaxis_title="Quantidade de Chamados",
            legend_title="Status do Prazo",
            bargap=0.3
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhum chamado para exibir no gráfico.")

    # =========================================================
    # 6. PRAZO CRÍTICO (com filtro)
    # =========================================================
    st.subheader("Chamados com Prazo Crítico")
    df_critico = df_filtrado[df_filtrado["Geral_Numerico"] <= 2].copy()

    if not df_critico.empty:
        tabela = df_critico[["Id", "Data Criação", "Técnico", "Dias Restantes Geral"]].copy()
        tabela["Data Criação"] = pd.to_datetime(tabela["Data Criação"], errors="coerce").dt.strftime("%d/%m/%Y")
        st.dataframe(tabela, use_container_width=True)
    else:
        st.success("Nenhum chamado com prazo crítico (≤2 dias no Geral)")

    # =========================================================
    # 7. TABELA COMPLETA (com filtro)
    # =========================================================
    st.subheader("Todos os Chamados")
    df_todos = df_filtrado[["Id", "Data Criação", "Técnico", "Dias Restantes Geral"]].copy()
    df_todos["Data Criação"] = pd.to_datetime(df_todos["Data Criação"], errors="coerce").dt.strftime("%d/%m/%Y")
    df_todos = df_todos.sort_values("Id", ascending=False)
    st.dataframe(df_todos, use_container_width=True)