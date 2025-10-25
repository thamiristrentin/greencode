import customtkinter as ctk
from tkinter import messagebox, ttk
from models.tarifa_model import TarifaModel
from utils.pdf_export import exportar_pdf_tabela
from utils.excel_export import exportar_excel

class TarifaView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="💰 Tarifas de Energia", font=("Helvetica", 20, "bold")).pack(pady=10)

        frame = ctk.CTkFrame(self)
        frame.pack(pady=8, padx=10, fill="both", expand=True)

        cols = ["id_tarifa", "valor_kwh", "vigencia_inicio", "vigencia_fim"]
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
        for t in TarifaModel.listar_todas():
            self.tree.insert("", "end", values=tuple(t.values()))

    def pdf(self):
        dados = TarifaModel.listar_todas()
        exportar_pdf_tabela("tarifas.pdf", "Tabela de Tarifas", dados, list(dados[0].keys()) if dados else [])

    def excel(self):
        exportar_excel("tarifas.xlsx", TarifaModel.listar_todas())
