import streamlit as st
import pandas as pd
from services.data_service import preparar_dados, carregar_planilha_google, get_google_credentials
#from views.dashboard_view_INATIVO import mostrar_dashboard
from views.dashboard_aguardando import mostrar_dashboard_aguardando

# ===== CONFIGURAÇÃO GERAL =====
st.set_page_config(page_title="Controle de Chamados - ApoioTech", layout="wide")

# ===== SIDEBAR =====
st.sidebar.title("Dashboard de Chamados")
#st.sidebar.success("✅ Dados fictícios carregados automaticamente!")
#st.sidebar.info("Recarregue a página se quiser testar com outro arquivo")

# ===== CARREGA DADOS FIXOS =====
#try:
    # Arquivo local fictício
    #df_raw = pd.read_excel("teste_portfolio/Chamados Geral - API Periodo (teste).xlsx")
    #df_raw.columns = df_raw.columns.str.strip().str.replace("Column1.", "", regex=False)
    #df_raw.columns = df_raw.columns.str.title().str.strip()
    #df = preparar_dados(df_raw)
    #st.sidebar.success("Arquivo fictício carregado com sucesso! (2.407 chamados)")
#except Exception as e:
    #st.error("Arquivo não encontrado. Rode o gerar_dados_ficticios.py primeiro!")
    #st.stop()

# ===== UPLOAD OPCIONAL =====
#st.sidebar.markdown("---")
#uploaded_file = st.sidebar.file_uploader("Ou suba seu próprio Excel", type=["xlsx"])

#if uploaded_file is not None:
    #df_raw = pd.read_excel(uploaded_file)
    #df_raw.columns = df_raw.columns.str.strip().str.replace("Column1.", "", regex=False)
    #df_raw.columns = df_raw.columns.str.title().str.strip()
    #df = preparar_dados(df_raw)
    #st.sidebar.success("Seu arquivo foi carregado com sucesso!")

# ===== ABAS DE DASHBOARD =====
tab_aguardando_aceite = st.tabs(["Dashboard Aguardando Aceite"])[0]
#tab1, tab2 = st.tabs(["Dashboard Geral", "Dashboard Aguardando Aceite"])


#with tab1:
    #mostrar_dashboard(df)

with tab_aguardando_aceite:
    gc = get_google_credentials()
    if gc:
        df_aguardando = carregar_planilha_google(gc)
        if df_aguardando is not None:
            mostrar_dashboard_aguardando(df_aguardando)
        else:
            st.error("Não foi possível carregar os dados do Google Sheets.")
    else:
        st.error("Credenciais do Google não encontradas.")
