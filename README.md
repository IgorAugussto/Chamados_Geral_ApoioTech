# 📊 Dashboard de Controle de Chamados - ApoioTech (Portfólio)

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)

**Link do app online (100% funcional):**  
🔗 https://seu-app-streamlit-aqui.streamlit.app *(substitua pelo seu link real)*

---

## 🎯 Objetivo do Projeto

Criar um **dashboard web interativo** para análise rápida de chamados técnicos (Milldesk) com:
- Cálculo automático de SLA (dias restantes + status)
- KPIs em tempo real
- Filtros por status e prioridade
- Gráficos limpos e profissionais (Plotly)
- Alertas visuais para SLA crítico
- 100% seguro para portfólio (dados fictícios)

---

## 🚀 Funcionalidades Implementadas

| Funcionalidade                        | Descrição                                                                 |
|--------------------------------------|---------------------------------------------------------------------------|
| **Upload de Excel**                  | Qualquer pessoa abre o link e sobe o arquivo → dashboard atualiza na hora |
| **KPIs**                             | Total de chamados · Abertos · Fechados                                    |
| **Filtros interativos**              | Status + Prioridade (múltipla escolha)                                    |
| **Gráfico de Prioridade**            | Barras agrupadas por Status                                               |
| **Gráfico de Tipos (Top 8 + Outros)**| Pizza/donut limpa – evita poluição visual                                 |
| **SLA Crítico (≤ 3 dias)**           | Tabela com destaque vermelho para vencidos                                |
| **Tabela ordenada por vencimento**   | Os que vencem primeiro aparecem no topo                                   |
| **Responsivo**                       | Funciona perfeitamente no celular                                         |

---

## 🛠️ Tecnologias Utilizadas

Python 3.11
´´´├── Streamlit          → interface web
├── Pandas             → tratamento de dados
├── Plotly Express     → gráficos interativos
├── Openpyxl           → leitura do Excel
└── GitHub + Streamlit Community Cloud → deploy gratuito´´´

---

## 📁 Estrutura do Projeto

Chamados_Geral_ApoioTech/
├── app.py                        # arquivo principal (Streamlit)
├── gerar_dados_ficticios.py      # script que gera 2.407 registros 100% fictícios
├── teste_portfolio/
│   └── data/
│       └── Chamados Geral - API Periodo.xlsx
├── services/
│   └── data_service.py
├── views/
│   └── dashboard_view.py
├── venv/
├── requirements.txt
└── README.md


---

## 🔒 Dados 100% Fictícios (Seguro para Portfólio)

> **Nenhum dado real da empresa foi usado.**

- 2.407 registros gerados por script Python  
- Estrutura idêntica ao Milldesk original (40 colunas)  
- Nomes, e-mails, descrições, IDs, prazos → tudo inventado  
- Distribuição de SLA, prioridades e tipos mantida (gráficos ficam realistas)  

**Script de geração (incluído):**
```bash
python gerar_dados_ficticios.py
