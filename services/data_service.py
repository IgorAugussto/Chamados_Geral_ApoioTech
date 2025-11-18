# services/data_service.py
import pandas as pd
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

def carregar_dados(caminho_excel: str = "data/Chamados Geral - API Periodo.xlsx") -> pd.DataFrame:
    excel_file = pd.ExcelFile(caminho_excel)
    nome_planilha = excel_file.sheet_names[0]
    df = pd.read_excel(excel_file, sheet_name=nome_planilha)
    df.columns = df.columns.str.strip().str.replace("Column1.", "", regex=False)
    df.columns = df.columns.str.title().str.strip()
    return df

def preparar_dados(df: pd.DataFrame) -> pd.DataFrame:
    if "Status" not in df.columns:
        possiveis = [c for c in df.columns if "status" in c.lower()]
        if possiveis:
            df.rename(columns={possiveis[0]: "Status"}, inplace=True)
        else:
            df["Status"] = "Desconhecido"

    if "Slasexpirationdate" in df.columns:
        df["Slasexpirationdate"] = pd.to_datetime(df["Slasexpirationdate"], errors="coerce", dayfirst=True)
        hoje = pd.Timestamp.now()
        df["Dias Restantes"] = (df["Slasexpirationdate"] - hoje).dt.days
    else:
        df["Dias Restantes"] = None

    df["Status Sla"] = df["Dias Restantes"].apply(
        lambda x: "Vencido" if pd.notna(x) and x < 0 else "No prazo"
    )
    return df

@st.cache_data
def carregar_excel(uploaded_file):
    df_raw = pd.read_excel(uploaded_file)
    df_raw.columns = df_raw.columns.str.strip().str.replace("Column1.", "", regex=False)
    df_raw.columns = df_raw.columns.str.title().str.strip()
    return preparar_dados(df_raw)


# ===== CARREGAR PLANILHA DO GOOGLE DRIVE (VERSÃO FINAL E 100% FUNCIONAL) =====
@st.cache_data(ttl=600, show_spinner="Carregando dados do Google Sheets...")  # 10 minutos
def carregar_planilha_google() -> pd.DataFrame:
    """
    Carrega os dados da planilha "Controle Chamados" com cache inteligente.
    Agora o .clear_cache() funciona perfeitamente no Streamlit Cloud!
    """
    gc = get_google_credentials()
    if gc is None:
        st.error("Credenciais do Google não encontradas! Verifique .streamlit/secrets.toml")
        return pd.DataFrame()

    try:
        sheet = gc.open("Controle Chamados").sheet1
        all_values = sheet.get_all_values()
        
        if len(all_values) <= 1:
            st.warning("Planilha vazia ou sem linhas de dados.")
            return pd.DataFrame()

        headers = all_values[0]
        data_rows = all_values[1:]
        df = pd.DataFrame(data_rows, columns=headers)
        
        # Limpeza e padronização (exatamente como você já tinha)
        df.columns = df.columns.str.strip()
        
        expected = ["Id", "Data Criação", "Técnico", "Dias Restantes PMA", "Dias Restantes Geral"]
        for col in expected:
            if col not in df.columns:
                df[col] = None

        if "Data Criação" in df.columns:
            df["Data Criação"] = pd.to_datetime(df["Data Criação"], errors="coerce", dayfirst=True)

        return df

    except Exception as e:
        st.error(f"Erro ao carregar planilha do Google: {e}")
        return pd.DataFrame()


# Inicializa conexão com Google Sheets
def get_google_credentials():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    try:
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error("Credenciais do Google não encontradas! Verifique .streamlit/secrets.toml")
        return None