# views/dashboard_aguardando.py
import streamlit as st
import plotly.express as px
import pandas as pd

def mostrar_dashboard_aguardando(df):
    st.title("⏳ Dashboard Aguardando Aceite")

    # --- KPI: Apenas Chamados Totais ---
    col1 = st.columns(3)[1]  # Centraliza
    col1.metric("Chamados Totais (Abertos)", len(df))

    # --- Botão de atualização manual ---
    if st.button("🔄 Atualizar Dados do Google Sheets", key="refresh_google"):
        st.cache_data.clear()
        st.success("Dados atualizados manualmente!")
        st.rerun()

    # --- Gráfico de Pizza: Distribuição por Técnico ---
    tecnicos = ["Igor", "Gustavo", "Raissa", "Leticia"]
    df_tec = df[df["Técnico"].isin(tecnicos)].copy()

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
        st.info("Nenhum chamado atribuído a Igor, Gustavo, Raissa ou Leticia.")

    # --- Chamados com Prazo Crítico ---
    st.subheader("⏳ Chamados com Prazo Crítico")

    # Converte colunas para numérico
    df["Dias Restantes PMA"] = pd.to_numeric(df["Dias Restantes PMA"], errors="coerce")
    df["Dias Restantes Geral"] = pd.to_numeric(df["Dias Restantes Geral"], errors="coerce")

    # Filtra por qualquer um dos dois <= 2
    df_critico = df[(df["Dias Restantes PMA"] <= 2) | (df["Dias Restantes Geral"] <= 2)].copy()

    if not df_critico.empty:
        tabela = df_critico[[
            "Id", "Data Criação", "Técnico",
            "Dias Restantes PMA", "Dias Restantes Geral"
        ]].copy()

        # Formata data
        if "Data Criação" in tabela.columns:
            tabela["Data Criação"] = pd.to_datetime(tabela["Data Criação"], errors="coerce").dt.strftime("%d/%m/%Y")

        st.dataframe(tabela, use_container_width=True)
    else:
        st.success("✅ Nenhum chamado com prazo crítico (≤2 dias)")

    # --- Tabela completa ---
    st.subheader("📋 Todos os Chamados")
    df_todos = df[[
        "Id", "Data Criação", "Técnico",
        "Dias Restantes PMA", "Dias Restantes Geral"
    ]].copy()
    df_todos["Data Criação"] = pd.to_datetime(df_todos["Data Criação"], errors="coerce").dt.strftime("%d/%m/%Y")
    df_todos = df_todos.sort_values("Id", ascending=False)
    st.dataframe(df_todos, use_container_width=True)