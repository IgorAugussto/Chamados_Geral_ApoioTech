# app.py (raiz)
import streamlit as st
<<<<<<< Updated upstream
from views.dashboard_view import mostrar_dashboard
from services.data_service import carregar_excel
=======
import pandas as pd
from services.data_service import preparar_dados, carregar_planilha_google, get_google_credentials
from views.dashboard_view import mostrar_dashboard
from views.dashboard_aguardando import mostrar_dashboard_aguardando
>>>>>>> Stashed changes

# ===== CONFIGURAÇÃO DA PÁGINA =====
st.set_page_config(page_title="Controle de Chamados - ApoioTech", layout="wide")

# ===== SIDEBAR COM LOGO E MENU =====
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/906/906343.png", width=80)
<<<<<<< Updated upstream
st.sidebar.title("Menu")
escolha = st.sidebar.radio("Selecione uma opção", ["Dashboard", "Sobre"])

# ===== FUNÇÃO PARA CARREGAR DADOS COM UPLOAD =====
def carregar_com_upload():
    st.sidebar.header("Upload do Excel")
    uploaded_file = st.sidebar.file_uploader(
        "Arraste ou clique para subir o arquivo Excel",
        type=["xlsx", "xls"],
        help="Arquivo: Chamados Geral - API Periodo.xlsx"
    )

    # Tenta recuperar df já carregado na sessão
    df = st.session_state.get("df_cache", None)

    # Se o usuário fez um upload novo, processa e guarda na sessão
    if uploaded_file is not None:
        try:
            df = carregar_excel(uploaded_file)  # usa a função cacheada do service
            st.session_state.df_cache = df       # persiste para manter após reload
            st.success("✔ Dados carregados com sucesso!")
            # opcional: guardar metadados do arquivo
            st.session_state.upload_name = getattr(uploaded_file, "name", "arquivo.xlsx")
            return df
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")
            return None

    # Se não tem upload na vez, mas existe cache na sessão -> retorna df
    if df is not None:
        # Aqui não mostramos o uploader como "preenchido", mas usamos os dados
        return df

    # Se não tem nada
    st.warning("Aguardando upload do arquivo Excel...")
    st.info("👆 Use o campo na barra lateral para subir o arquivo")
    return None

# ===== MAIN =====
def main():
    df = carregar_com_upload()
    
    if df is not None:
        mostrar_dashboard(df)

if __name__ == "__main__":
    main()
=======
st.sidebar.title("Dashboard de Chamados")
st.sidebar.title("Menu")
st.sidebar.success("✅ Dados fictícios carregados automaticamente!")
st.sidebar.info("Recarregue a página se quiser testar com outro arquivo")

# Menu com abas no topo
tab1, tab2 = st.tabs(["Dashboard Geral", "Dashboard Aguardando Aceite"])

# ===== CARREGA DADOS FIXOS (FÁCIL E RÁPIDO) =====
try:
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

# ===== MOSTRA DASHBOARDS NAS ABAS =====
with tab1:
    mostrar_dashboard(df)

with tab2:
    # Conecta ao Google Sheets
    gc = get_google_credentials()
    if gc:
        df_aguardando = carregar_planilha_google(gc)
        if df_aguardando is not None:
            mostrar_dashboard_aguardando(df_aguardando)
        else:
            st.error("Não foi possível carregar os dados do Google Sheets.")
    else:
        st.error("Credenciais do Google não encontradas.")
>>>>>>> Stashed changes
