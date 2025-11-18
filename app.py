import streamlit as st
import pandas as pd
from services.data_service import (
    preparar_dados,
    carregar_planilha_google,   # ← agora sem parâmetro _gc
    get_google_credentials
)
#from views.dashboard_view_INATIVO import mostrar_dashboard
from views.dashboard_aguardando import mostrar_dashboard_aguardando

# ===== CONFIGURAÇÃO GERAL =====
st.set_page_config(page_title="Controle de Chamados - ApoioTech", layout="wide")

# ===== ESTILO CUSTOMIZADO PARA O BOTÃO DE ATUALIZAR (FUNCIONA EM 2025) =====
st.markdown("""
<style>
    /* Nova forma correta de pegar botão primary no sidebar (Streamlit 1.28+) */
    section[data-testid="stSidebar"] div.stButton > button {
        background-color: #3498db !important;
        border-color: #3498db !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        height: 4em !important;
        width: 100% !important;
    }
    
    section[data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #2980b9 !important;
        border-color: #2980b9 !important;
        box-shadow: 0 4px 12px rgba(0, 210, 211, 0.4) !important;
        transform: translateY(-1px);
    }
    
    /* Força o botão a ficar bonito mesmo se o Streamlit mudar de novo */
    section[data-testid="stSidebar"] div.stButton > button:active {
        background-color: #16a085 !important;
    }
</style>
""", unsafe_allow_html=True)

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

# ===== BOTÃO DE ATUALIZAÇÃO MANUAL + INFO DE ÚLTIMA ATUALIZAÇÃO =====
st.sidebar.markdown("---")
st.sidebar.caption(f"Última atualização automática: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}")

if st.sidebar.button("🔄 Atualizar Dados do Google Sheets Agora", key="btn_refresh", use_container_width=True):
    carregar_planilha_google.clear_cache()   # ← Limpa só o cache dos dados do Sheets
    st.success("Dados atualizados manualmente!")
    st.rerun()

# ===== ABAS DE DASHBOARD =====
tab_aguardando_aceite = st.tabs(["Dashboard Aguardando Aceite"])[0]
#tab1, tab2 = st.tabs(["Dashboard Geral", "Dashboard Aguardando Aceite"])


#with tab1:
    #mostrar_dashboard(df)

with tab_aguardando_aceite:
    # Carrega os dados com cache (atualiza a cada 10 minutos automaticamente)
    df_aguardando = carregar_planilha_google()
    
    if df_aguardando is None or df_aguardando.empty:
        st.error("Não foi possível carregar os dados do Google Sheets. Verifique as credenciais ou a conexão.")
    else:
        mostrar_dashboard_aguardando(df_aguardando)