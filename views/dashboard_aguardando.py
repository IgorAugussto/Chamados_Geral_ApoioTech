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
        load_data.cache_clear()
        st.cache_data.clear()
        st.success("Dados atualizados manualmente!")
        st.rerun()

    # =========================================================
    # 3. EXTRAIR NÚMERO DA COLUNA "GERAL" (VERSÃO 100% CORRETA)
    # =========================================================
    def extrair_numero_correto(texto):
        if pd.isna(texto):
            return None
        
        texto = str(texto).lower()
        
        # Procura qualquer sequência de números
        match = re.search(r'\d+', texto)
        if not match:
            return None
            
        numero = int(match.group())
        
        # SE tiver a palavra "atrasado" → número é NEGATIVO
        if "atrasado" in texto or "vencido" in texto or "overdue" in texto:
            return -numero
        else:
            # Caso contrário (dentro do prazo) → número positivo
            return numero

    # Aplica a função nova
    df["Geral_Numerico"] = df["Dias Restantes Geral"].apply(extrair_numero_correto)

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
    # 5. GRÁFICO: Dentro do Prazo vs Atrasados + TOTAL POR TÉCNICO (MELHOR VISUALIZAÇÃO)
    # =========================================================
    st.subheader("Distribuição por Status de Prazo")

    def classificar_prazo(texto):
        if pd.isna(texto):
            return "Sem Informação"
        texto = str(texto).lower()
        if "atrasado" in texto or "vencido" in texto or "overdue" in texto:
            return "Atrasado"
        if "dentro" in texto or "within" in texto:
            return "Dentro do Prazo"
        return "Sem Informação"

    df_filtrado["Status Prazo"] = df_filtrado["Dias Restantes Geral"].apply(classificar_prazo)

    # Contagem correta por técnico e status
    df_grafico = (
        df_filtrado.groupby(["Técnico", "Status Prazo"], dropna=False)
        .size()
        .reset_index(name="Quantidade")
    )

    # Garante que todos os técnicos apareçam com as duas categorias
    todos_tecnicos = df_filtrado["Técnico"].dropna().unique()
    base = pd.DataFrame([
        {"Técnico": tec, "Status Prazo": status}
        for tec in todos_tecnicos
        for status in ["Dentro do Prazo", "Atrasado"]
    ])
    df_grafico = base.merge(df_grafico, on=["Técnico", "Status Prazo"], how="left").fillna(0)
    df_grafico["Quantidade"] = df_grafico["Quantidade"].astype(int)

    # === CÁLCULO DO TOTAL POR TÉCNICO (é aqui que você queria!) ===
    total_por_tecnico = df_grafico.groupby("Técnico")["Quantidade"].sum().reset_index()
    total_por_tecnico.rename(columns={"Quantidade": "Total"}, inplace=True)

    # Adiciona o total como uma linha extra (vai aparecer no topo das barras)
    df_total = total_por_tecnico.copy()
    df_total["Status Prazo"] = "TOTAL"  # nome que vai aparecer na legenda (opcional)

    # Junta o total com os dados do gráfico (só para exibir o número grande)
    df_grafico_com_total = pd.concat([df_grafico, df_total], ignore_index=True)

    # Ordenação dos técnicos por total (decrescente)
    ordem_tecnicos = total_por_tecnico.sort_values("Total", ascending=False)["Técnico"]
    df_grafico["Técnico"] = pd.Categorical(df_grafico["Técnico"], categories=ordem_tecnicos, ordered=True)
    df_grafico = df_grafico.sort_values(["Técnico", "Status Prazo"])

    if not df_grafico.empty:
        fig = px.bar(
            df_grafico,
            x="Técnico",
            y="Quantidade",
            color="Status Prazo",
            title="Chamados Dentro do Prazo vs Atrasados por Técnico",
            barmode="group",  # mudamos para stack para ficar mais limpo com o total em cima
            color_discrete_map={
                "Dentro do Prazo": "#2ecc71",
                "Atrasado": "#e74c3c",
            },
            category_orders={"Status Prazo": ["Dentro do Prazo", "Atrasado"]},
            text_auto=True,  # mostra o número em cada barra
        )

        # === ADICIONA O TOTAL BEM GRANDE EM CIMA DE CADA GRUPO ===
        for idx, row in total_por_tecnico.iterrows():
            fig.add_annotation(
                x=row["Técnico"],
                y=row["Total"],
                text=f"<b>{int(row['Total'])}</b>",
                font=dict(size=16, color="#2c3e50"),
                showarrow=False,
                yshift=10,
                xanchor="center"
            )

        fig.update_traces(textposition="inside")
        fig.update_layout(
            xaxis_title="Técnico",
            yaxis_title="Quantidade de Chamados",
            legend_title="Status do Prazo",
            bargap=0.3,
            yaxis=dict(range=[0, total_por_tecnico["Total"].max() * 1.2]),
            uniformtext=dict(mode="hide"),
            title_x=0.5,
        )

        st.plotly_chart(fig, use_container_width=True)

        # Opcional: mostrar uma tabelinha pequena com os totais
        st.caption("**Total de chamados por técnico (em dia + atrasados):**")
        total_display = total_por_tecnico.sort_values("Total", ascending=False).copy()
        total_display = total_display.rename(columns={"Técnico": "Técnico", "Total": "Total de Chamados"})
        st.dataframe(total_display, use_container_width=True, hide_index=True)

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