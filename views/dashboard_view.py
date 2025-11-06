# Camada de apresentação (telas, gráficos, componentes)
# Tudo que é exibido no Streamlit

import streamlit as st
import plotly.express as px
import pandas as pd

def mostrar_dashboard(df):
    st.title("📊 Dashboard de Chamados")

    # --- KPIs ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Chamados Totais", len(df))
    col2.metric("Abertos", (df["Status"] == "Aberto").sum())
    col3.metric("Fechados", (df["Status"] == "Fechado").sum())

    # --- Filtros ---
    st.sidebar.header("Filtros")
    status_filtro = st.sidebar.selectbox(
           "Filtrar por Status", ["Todos"] + list(df["Status"].unique())
    )
    
    # CORREÇÃO: Remover valores NaN antes de criar o filtro
    prioridades_disponiveis = df["Priority"].dropna().unique()
    prioridade_filtro = st.sidebar.multiselect(
        "Filtrar por Prioridade", 
        prioridades_disponiveis, 
        default=prioridades_disponiveis
    )

    # Aplicar filtros
    if status_filtro != "Todos":
        df = df[df["Status"] == status_filtro]
    
    # CORREÇÃO: Incluir também registros com Priority vazia se nenhum filtro foi selecionado
    if prioridade_filtro:
        df = df[df["Priority"].isin(prioridade_filtro)]

    st.divider()

    #--- Gráfico por Prioridade ---
    # CORREÇÃO: Remover NaN antes de plotar
    df_prioridade = df[df["Priority"].notna()]
    if not df_prioridade.empty:
        fig1 = px.bar(
            df_prioridade,
            x="Priority",
            color="Status",
            title="Chamados por Prioridade e Status",
            barmode="group",
            text_auto=True
        )
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Nenhum chamado com prioridade definida")

        #--- Gráfico por Tipo de Chamado ---
    if "Tickettype" in df.columns:
        df_tipo = df[df["Tickettype"].notna()].copy()

        if not df_tipo.empty:
            # Conta quantos por tipo
            contagem = df_tipo["Tickettype"].value_counts().reset_index()
            contagem.columns = ["Tickettype", "Quantidade"]

            # Define quantos mostrar (ex: top 8)
            top_n = 8
            top_tipos = contagem.head(top_n)

            # O resto vira "Outros"
            outros = pd.DataFrame({
                "Tickettype": ["Outros"],
                "Quantidade": [contagem["Quantidade"].iloc[top_n:].sum()]
            })

            # Junta top + outros
            dados_grafico = pd.concat([top_tipos, outros], ignore_index=True)

            # Gráfico de pizza LIMPO
            fig2 = px.pie(
                dados_grafico,
                names="Tickettype",
                values="Quantidade",
                title="Distribuição por Tipo de Chamado (Top 8 + Outros)",
                hole=0.3  # donut (fica mais moderno)
            )
            fig2.update_traces(textinfo="percent+label")  # mostra % e nome na fatia
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Nenhum tipo de chamado definido")

    # --- SLA ---
    if "Dias Restantes" in df.columns:
        st.subheader("⏳ Chamados com Prazo Crítico")
        df_vencendo = df[df["Dias Restantes"] <= 2]
        if not df_vencendo.empty:
            st.dataframe(df_vencendo[["Id", "Priority", "Status", "Dias Restantes"]])
        else:
            st.success("✅ Nenhum chamado próximo do vencimento")

        # --- Tabela completa (ordenada por SLA) ---
    st.subheader("📋 Chamados Recentes")

    # Cria uma cópia para não bagunçar os filtros
    df_tabela = df.copy()

    # Se tiver a coluna de data do SLA, ordena por ela
    if "Slasexpirationdate" in df_tabela.columns:
        df_tabela = df_tabela.sort_values("Slasexpirationdate", ascending=True)  # mais antigo primeiro
    else:
        df_tabela = df_tabela.sort_values("Id", ascending=False)  # senão, por ID (mais novo)

    # Mostra só os 15 primeiros
    st.dataframe(df_tabela.head(15))