import customtkinter as ctk
from tkinter import messagebox, ttk
from models.comparativo_model import ComparativoModel
from utils.pdf_export import exportar_pdf_tabela
from utils.excel_export import exportar_excel

class ComparativoView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="📊 Comparativos de Economia", font=("Helvetica", 20, "bold")).pack(pady=10)

        frame = ctk.CTkFrame(self)
        frame.pack(pady=8, padx=10, fill="both", expand=True)

        cols = ["id_comparativo", "descricao", "consumo_atual_kwh", "consumo_futuro_kwh", "economia_kwh", "economia_reais"]
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c.replace("_", " ").title())
            self.tree.column(c, anchor="center", width=150)
        self.tree.pack(fill="both", expand=True)

        btns = ctk.CTkFrame(self)
        btns.pack(pady=10)
        ctk.CTkButton(btns, text="🔄 Atualizar", command=self.atualizar, fg_color="#2E8B57").grid(row=0,column=0,padx=6)
        ctk.CTkButton(btns, text="📄 PDF", command=self.pdf, fg_color="#5A5AAD").grid(row=0,column=1,padx=6)
        ctk.CTkButton(btns, text="📊 Excel", command=self.excel, fg_color="#DAA520").grid(row=0,column=2,padx=6)

        self.atualizar()

    def atualizar(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for c in ComparativoModel.listar_todos():
            self.tree.insert("", "end", values=tuple(c.values()))

    def pdf(self):
        dados = ComparativoModel.listar_todos()
        exportar_pdf_tabela("comparativos.pdf", "Relatório de Comparativos", dados, list(dados[0].keys()) if dados else [])

    def excel(self):
        exportar_excel("comparativos.xlsx", ComparativoModel.listar_todos())
