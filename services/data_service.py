import pandas as pd
from datetime import datetime

def carregar_dados(caminho_excel: str = "data/Chamados Geral - API Periodo.xlsx") -> pd.DataFrame:
    """Carrega o Excel e trata os dados iniciais"""
    # abre o arquivo e identifica o nome real da planilha
    excel_file = pd.ExcelFile(caminho_excel)
    nome_planilha = excel_file.sheet_names[0]  # pega a primeira (Texto Exibido)
    
    df = pd.read_excel(excel_file, sheet_name=nome_planilha)

    # limpa nomes das colunas
    df.columns = df.columns.str.strip().str.replace("Column1.", "", regex=False)
    df.columns = df.columns.str.title().str.strip()

    return df


def preparar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Cria colunas calculadas e padroniza os dados"""

    # Garante que 'Status' exista
    if "Status" not in df.columns:
        possiveis = [c for c in df.columns if "status" in c.lower()]
        if possiveis:
            df.rename(columns={possiveis[0]: "Status"}, inplace=True)
        else:
            df["Status"] = "Desconhecido"

    # Converte a data e calcula dias restantes
    if "Slasexpirationdate" in df.columns:
        df["Slasexpirationdate"] = pd.to_datetime(df["Slasexpirationdate"], errors="coerce", dayfirst=True)
        hoje = pd.Timestamp.now()
        df["Dias Restantes"] = (df["Slasexpirationdate"] - hoje).dt.days
    else:
        df["Dias Restantes"] = None

    # Cria o status do SLA
    df["Status Sla"] = df["Dias Restantes"].apply(
        lambda x: "Vencido" if pd.notna(x) and x < 0 else "No prazo"
    )

    return df
