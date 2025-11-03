# Camada de apresentação (telas, gráficos, componentes)
# Tudo que é exibido no Streamlit

import streamlit as st
import plotly.express as px

def mostrar_dashboard(df):
    st.title("📊 Dashboard de Chamados")
    
    # No início do arquivo dashboard_view.py, adicione:
    print("Colunas disponíveis:", df.columns.tolist())
    

    # --- KPIs ---
    #col1, col2, col3 = st.columns(3)
    #col1.metric("Chamados Totais", len(df))
    #col2.metric("Abertos", (df["Status"] == "Aberto").sum())
    #col3.metric("Fechados", (df["Status"] == "Fechado").sum())

    # --- Filtros ---
    #st.sidebar.header("Filtros")
    #status_filtro = st.sidebar.selectbox(
    #       "Filtrar por Status", ["Todos"] + list(df["Status"].unique())
    #)
    #prioridade_filtro = st.sidebar.multiselect(
     #   "Filtrar por Prioridade", df["Prioridade"].unique(), default=df["Prioridade"].unique()
    #)

    #if status_filtro != "Todos":
       # df = df[df["Status"] == status_filtro]
    #df = df[df["Prioridade"].isin(prioridade_filtro)]

    #st.divider()

    # --- Gráfico por Prioridade ---
    #fig1 = px.bar(
    #    df,
     #   x="Prioridade",
      #  color="Status",
       # title="Chamados por Prioridade e Status",
        #barmode="group",
        #text_auto=True
    #)
    #st.plotly_chart(fig1, use_container_width=True)

    # --- Gráfico por Tipo de Chamado ---
    #if "Tipo de Chamado" in df.columns:
        fig2 = px.pie(df, names="Tipo de Chamado", title="Distribuição por Tipo de Chamado")
        st.plotly_chart(fig2, use_container_width=True)

    # --- SLA ---
    if "Dias Restantes" in df.columns:
        st.subheader("⏳ Chamados com Prazo Crítico")
        df_vencendo = df[df["Dias Restantes"] <= 2]
        st.dataframe(df_vencendo[["ID", "Prioridade", "Status", "Dias Restantes"]])

    # --- Tabela completa ---
    st.subheader("📋 Chamados Recentes")
    st.dataframe(df.tail(15))
