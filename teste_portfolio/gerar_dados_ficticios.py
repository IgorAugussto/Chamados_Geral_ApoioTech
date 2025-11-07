# gerar_dados_ficticios.py
import pandas as pd
import random
from datetime import datetime, timedelta
import os

random.seed(42)

# Cria a pasta data se não existir
os.makedirs("teste_portfolio/data", exist_ok=True)

colunas = [
    'Workflow_Fields', 'Id', 'Start', 'Requester', 'Location', 'Ticket', 'Description', 'End', 'Analysis',
    'Reopening', 'Category', 'Subcategory', 'Id_Local', 'Department', 'Agent', 'Stage', 'Impact', 'Asset',
    'Serial', 'Manner', 'Level', 'Priority', 'Problem', 'Solution', 'Status', 'Tickettype', 'Urgency',
    'Observation', 'Contactphone', 'Contract', 'Impactdetails', 'Change', 'Satisfaction', 'Satisfactioncomment',
    'Resolution', 'Group', 'Slasexpirationdate', 'Starttime', 'Endtime', 'Analysistime', 'Charge_Hour',
    'Worked_Hour'
]

prioridades = ['1 - Crítica', '2 - Alta', '3 - Média', '4 - Normal', '5 - Baixa']
status_list = ['Aberto', 'Fechado', 'Em Análise', 'Aguardando Usuário', 'Em Pausa']
tipos = ['Falha de Funcionamento', 'Suporte Técnico', 'Dúvida', 'Acesso à Aplicação', 'Relatório', 'Outros']
nomes = ['Ana Silva', 'Carlos Oliveira', 'Mariana Costa', 'Pedro Santos', 'Julia Ferreira', 'Lucas Almeida']

dados = []
hoje = datetime(2025, 11, 6)

for i in range(2407):
    sla = hoje + timedelta(days=random.randint(-30, 60))
    linha = {
        'Id': 35000 + i,
        'Requester': random.choice(nomes),
        'Location': random.choice(['Prefeitura de Campinas', 'Prefeitura de Anápolis']),
        'Ticket': f'Chamado #{35000+i} - Erro no relatório',
        'Description': f'Detalhamento fictício do chamado {35000+i}. Tudo inventado para portfólio.',
        'Priority': random.choice(prioridades),
        'Status': random.choice(status_list),
        'Tickettype': random.choice(tipos),
        'Department': random.choice(['TI', 'Financeiro', 'RH', 'Contábil']),
        'Agent': random.choice(['João Silva', 'Maria Oliveira']),
        'Slasexpirationdate': sla.strftime('%d/%m/%Y'),
        'Group': 'ApoioTech',
        'Level': 'Nível 2',
        'Starttime': round(45967.35 + random.random(), 5),
        'Charge_Hour': '0,0000',
        'Worked_Hour': '0,0000',
    }
    dados.append(linha)

df = pd.DataFrame(dados, columns=colunas)
df.to_excel('teste_portfolio/data/Chamados Geral - API Periodo (teste).xlsx', index=False)

print("ARQUIVO CRIADO COM SUCESSO!")
print("Local: teste_portfolio/data/Chamados Geral - API Periodo (teste).xlsx")
print("Agora é só dar git push e seu portfólio está 100% seguro!")