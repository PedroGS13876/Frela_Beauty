import pandas as pd
import os

# Verificação e leitura dos arquivos de despesas e receitas
if ("df_despesas.csv" in os.listdir()) and ("df_receitas.csv" in os.listdir()):
    df_despesas = pd.read_csv("df_despesas.csv", index_col=0, parse_dates=True)
    df_receitas = pd.read_csv("df_receitas.csv", index_col=0, parse_dates=True)
    
    # Garantir que a coluna "Data" é do tipo datetime
    df_despesas["Data"] = pd.to_datetime(df_despesas["Data"], errors='coerce')
    df_receitas["Data"] = pd.to_datetime(df_receitas["Data"], errors='coerce')
else:
    data_structure = {
        'Valor': [],
        'Efetuado': [],
        'Fixo': [],
        'Data': [],
        'Categoria': [],
        'Descrição': []
    }

    df_receitas = pd.DataFrame(data_structure)
    df_despesas = pd.DataFrame(data_structure)
    df_despesas.to_csv("df_despesas.csv", index=False)
    df_receitas.to_csv("df_receitas.csv", index=False)

# Verificação e leitura dos arquivos de categorias
if ("df_cat_receita.csv" in os.listdir()) and ("df_cat_despesa.csv" in os.listdir()):
    df_cat_receita = pd.read_csv("df_cat_receita.csv", index_col=0)
    df_cat_despesa = pd.read_csv("df_cat_despesa.csv", index_col=0)
    cat_receita = df_cat_receita['Categoria'].tolist()
    cat_despesa = df_cat_despesa['Categoria'].tolist()
else:
    cat_receita = {'Categoria': ["Salário", "Investimentos", "Comissão"]}
    cat_despesa = {'Categoria': ["Alimentação", "Aluguel", "Gasolina", "Saúde", "Lazer"]}
    
    df_cat_receita = pd.DataFrame(cat_receita)
    df_cat_despesa = pd.DataFrame(cat_despesa)
    df_cat_receita.to_csv("df_cat_receita.csv", index=False)
    df_cat_despesa.to_csv("df_cat_despesa.csv", index=False)