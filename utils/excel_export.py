import pandas as pd
from tkinter import messagebox
import os

def exportar_excel(nome_arquivo, dados):
    if not dados:
        messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
        return

    df = pd.DataFrame(dados)
    caminho = os.path.join(os.getcwd(), nome_arquivo)
    df.to_excel(caminho, index=False)
    messagebox.showinfo("Excel gerado", f"Arquivo salvo em:\n{caminho}")
