import streamlit as st
import pandas as pd
from services.data_service import preparar_dados
from views.dashboard_view import mostrar_dashboard

st.set_page_config(page_title="Controle de Chamados - ApoioTech", layout="wide")

# ===== SIDEBAR =====
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/906/906343.png", width=80)
st.sidebar.title("Dashboard de Chamados")
st.sidebar.success("✅ Dados fictícios carregados automaticamente!")
st.sidebar.info("Recarregue a página se quiser testar com outro arquivo")

# ===== CARREGA DADOS FIXOS (FÁCIL E RÁPIDO) =====
try:
    # ARQUIVO FIXO FICTÍCIO (já está no repo)
    df_raw = pd.read_excel("teste_portfolio/Chamados Geral - API Periodo (teste).xlsx")
    df_raw.columns = df_raw.columns.str.strip().str.replace("Column1.", "", regex=False)
    df_raw.columns = df_raw.columns.str.title().str.strip()
    df = preparar_dados(df_raw)
    
    st.sidebar.success("Arquivo fictício carregado com sucesso! (2.407 chamados)")
    
except Exception as e:
    st.error("Arquivo não encontrado. Rode o gerar_dados_ficticios.py primeiro!")
    st.stop()

# ===== OPCIONAL: upload pra quem quiser testar outro arquivo =====
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("Ou suba seu próprio Excel", type=["xlsx"])
if uploaded_file is not None:
    df_raw = pd.read_excel(uploaded_file)
    df_raw.columns = df_raw.columns.str.strip().str.replace("Column1.", "", regex=False)
    df_raw.columns = df_raw.columns.str.title().str.strip()
    df = preparar_dados(df_raw)
    st.sidebar.success("Seu arquivo foi carregado!")

# ===== MOSTRA O DASHBOARD =====
mostrar_dashboard(df)