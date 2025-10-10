import pandas as pd

def exportar_excel(dados, nome_arquivo):
    df = pd.DataFrame(dados)
    df.to_excel(nome_arquivo, index=False)
    print(f"✅ Excel exportado: {nome_arquivo}")