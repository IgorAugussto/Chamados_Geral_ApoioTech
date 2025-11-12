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

# ===== CARREGAR PLANILHA DO GOOGLE DRIVE =====
@st.cache_data(ttl=300)  # Atualiza a cada 5 minutos
def carregar_planilha_google(_gc):
    try:
        sheet = _gc.open("Chamados_Aguardando_Aceite").sheet1
        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        df.columns = df.columns.str.strip()
        expected = ["Id", "Data Criação", "Técnico", "Dias Restantes PMA", "Dias Restantes Geral"]
        for col in expected:
            if col not in df.columns:
                df[col] = None

        if "Data Criação" in df.columns:
            df["Data Criação"] = pd.to_datetime(df["Data Criação"], errors="coerce", dayfirst=True)

        return df
    except Exception as e:
        st.error(f"Erro ao carregar planilha: {e}")
        return None

# Inicializa conexão com Google Sheets
def get_google_credentials():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    try:
        creds_dict = st.secrets["credencial/service_account.json"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    except:
        if os.path.exists("credentials.json"):
            creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        else:
            st.error("Credenciais do Google não encontradas!")
            return None
    return gspread.authorize(creds)