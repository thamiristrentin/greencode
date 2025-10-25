import customtkinter as ctk
from tkinter import messagebox, ttk
from models.consumo_model import ConsumoModel
from utils.pdf_export import exportar_pdf_tabela
from utils.excel_export import exportar_excel

class ConsumoView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="⚡ Consumo de Energia", font=("Helvetica", 20, "bold")).pack(pady=10)

        tabela_frame = ctk.CTkFrame(self)
        tabela_frame.pack(pady=8, padx=10, fill="both", expand=True)

        cols = ["id_consumo", "equipamento", "valor_kwh", "consumo_diario_kwh", "consumo_mensal_kwh", "custo_diario", "custo_mensal"]
        self.tree = ttk.Treeview(tabela_frame, columns=cols, show="headings", height=10)

        for col in cols:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, anchor="center", width=120)

        vsb = ttk.Scrollbar(tabela_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="🔄 Atualizar", command=self.atualizar_lista, fg_color="#2E8B57").grid(row=0,column=0,padx=6)
        ctk.CTkButton(btn_frame, text="📄 PDF", command=self.exportar_pdf, fg_color="#5A5AAD").grid(row=0,column=1,padx=6)
        ctk.CTkButton(btn_frame, text="📊 Excel", command=self.exportar_excel, fg_color="#DAA520").grid(row=0,column=2,padx=6)

        self.atualizar_lista()

    def atualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for c in ConsumoModel.listar_todos():
            self.tree.insert("", "end", values=tuple(c.values()))

    def exportar_pdf(self):
        dados = ConsumoModel.listar_todos()
        exportar_pdf_tabela("consumos.pdf", "Relatório de Consumo", dados, list(dados[0].keys()) if dados else [])

    def exportar_excel(self):
        exportar_excel("consumos.xlsx", ConsumoModel.listar_todos())
