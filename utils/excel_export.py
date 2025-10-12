import os
import pandas as pd
from tkinter import messagebox

def exportar_excel(titulo, nome_arquivo, dados):
    try:
        if not dados:
            messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
            return

        # Converte os dados para DataFrame
        df = pd.DataFrame(dados)

        # Define caminho completo
        caminho = os.path.join(os.getcwd(), nome_arquivo)
        df.to_excel(caminho, index=False, sheet_name=titulo[:30])

        # Mostra aviso de sucesso
        messagebox.showinfo("Exportação concluída", f"Planilha salva em:\n{caminho}")
        print(f"📊 Excel salvo em: {caminho}")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao exportar Excel:\n{e}")