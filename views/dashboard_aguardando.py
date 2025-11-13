# views/dashboard_aguardando.py
import streamlit as st
import plotly.express as px
import pandas as pd
import re

def mostrar_dashboard_aguardando(df):
    st.title("Dashboard Aguardando Aceite")

    # =========================================================
    # 1. KPI
    # =========================================================
    col1 = st.columns(3)[1]
    col1.metric("Chamados Totais (Abertos)", len(df))

    # =========================================================
    # 2. Botão de atualização
    # =========================================================
    if st.button("Atualizar Dados do Google Sheets", key="refresh_google"):
        st.cache_data.clear()
        st.success("Dados atualizados manualmente!")
        st.rerun()

    # =========================================================
    # 3. EXTRAIR DIAS (ROBUSTO)
    # =========================================================
    def extrair_dias(texto):
        if pd.isna(texto):
            return None
        texto = str(texto).strip()
        match = re.search(r'\((\d+)\s*days?', texto, re.IGNORECASE)
        return int(match.group(1)) if match else None

    # Aplica nas duas colunas
    df["Dias Restantes PMA"] = df["Dias Restantes PMA"].apply(extrair_dias)
    df["Dias Restantes Geral"] = df["Dias Restantes Geral"].apply(extrair_dias)

    # =========================================================
    # 4. GRÁFICO: Técnicos
    # =========================================================
    df_tec = df[
        df["Técnico"].astype(str).str.contains("Gustavo|Igor|Raissa|Leticia", na=False)
    ].copy()

    if not df_tec.empty:
        contagem = df_tec["Técnico"].value_counts().reset_index()
        contagem.columns = ["Técnico", "Quantidade"]

        fig = px.pie(
            contagem,
            names="Técnico",
            values="Quantidade",
            title="Distribuição por Técnico",
            hole=0.3,
            color_discrete_sequence=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
        )
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhum chamado com os técnicos especificados.")

    # =========================================================
    # 5. PRAZO CRÍTICO
    # =========================================================
    st.subheader("Chamados com Prazo Crítico")

    df_critico = df[
        (df["Dias Restantes PMA"] <= 2) |
        (df["Dias Restantes Geral"] <= 2)
    ].copy()

    if not df_critico.empty:
        tabela = df_critico[[
            "Id", "Data Criação", "Técnico",
            "Dias Restantes PMA", "Dias Restantes Geral"
        ]].copy()
        tabela["Data Criação"] = pd.to_datetime(tabela["Data Criação"], errors="coerce").dt.strftime("%d/%m/%Y")
        st.dataframe(tabela, use_container_width=True)
    else:
        st.success("Nenhum chamado com prazo crítico (≤2 dias)")

    # =========================================================
    # 6. TABELA COMPLETA
    # =========================================================
    st.subheader("Todos os Chamados")
    df_todos = df[[
        "Id", "Data Criação", "Técnico",
        "Dias Restantes PMA", "Dias Restantes Geral"
    ]].copy()
    df_todos["Data Criação"] = pd.to_datetime(df_todos["Data Criação"], errors="coerce").dt.strftime("%d/%m/%Y")
    df_todos = df_todos.sort_values("Id", ascending=False)
    st.dataframe(df_todos, use_container_width=True)