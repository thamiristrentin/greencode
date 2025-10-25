import customtkinter as ctk
from tkinter import messagebox
from models.equipamento_model import EquipamentoModel
from models.inventario_model import InventarioModel
from models.consumo_model import ConsumoModel
from models.comparativo_model import ComparativoModel
from utils.pdf_export import exportar_pdf_tabela
from utils.excel_export import exportar_excel
from datetime import datetime

class RelatorioView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="📊 Relatórios Gerais", font=("Helvetica", 22, "bold")).pack(pady=15)

        # --- FRAME GERAL ---
        content = ctk.CTkFrame(self, fg_color="#F5F5F5")
        content.pack(fill="both", expand=True, padx=20, pady=10)

        # --- CARDS RESUMO ---
        self.cards_frame = ctk.CTkFrame(content, fg_color="white")
        self.cards_frame.pack(pady=10, padx=10, fill="x")

        self.cards = {
            "equipamentos": ctk.CTkLabel(self.cards_frame, text="", font=("Helvetica", 16), anchor="center"),
            "inventario": ctk.CTkLabel(self.cards_frame, text="", font=("Helvetica", 16), anchor="center"),
            "consumo": ctk.CTkLabel(self.cards_frame, text="", font=("Helvetica", 16), anchor="center"),
            "economia": ctk.CTkLabel(self.cards_frame, text="", font=("Helvetica", 16), anchor="center"),
        }

        grid_opts = {"padx": 15, "pady": 10, "sticky": "nsew"}
        titles = ["⚙️ Equipamentos", "📦 Itens de Inventário", "⚡ Registros de Consumo", "💰 Economia Total (R$)"]

        for i, (key, label) in enumerate(self.cards.items()):
            frame = ctk.CTkFrame(self.cards_frame, fg_color="#E8F5E9", corner_radius=10)
            frame.grid(row=0, column=i, **grid_opts)
            ctk.CTkLabel(frame, text=titles[i], font=("Helvetica", 14, "bold")).pack(pady=(10, 5))
            label.pack(pady=(0, 10), padx=20)

        # --- BOTÕES DE EXPORTAÇÃO ---
        btn_frame = ctk.CTkFrame(content)
        btn_frame.pack(pady=20)
        ctk.CTkButton(btn_frame, text="📄 Exportar Relatório PDF", command=self.exportar_pdf, fg_color="#5A5AAD").grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="📊 Exportar Excel", command=self.exportar_excel, fg_color="#DAA520").grid(row=0, column=1, padx=10)
        ctk.CTkButton(btn_frame, text="🔄 Atualizar Dados", command=self.atualizar_dados, fg_color="#2E8B57").grid(row=0, column=2, padx=10)

        self.atualizar_dados()

    def atualizar_dados(self):
        equipamentos = EquipamentoModel.listar_todos()
        inventario = InventarioModel.listar_todos()
        consumo = ConsumoModel.listar_todos()
        comparativos = ComparativoModel.listar_todos()

        total_equip = len(equipamentos)
        total_inv = len(inventario)
        total_consumo = len(consumo)
        total_economia = sum([c["economia_reais"] for c in comparativos]) if comparativos else 0

        self.cards["equipamentos"].configure(text=f"{total_equip}")
        self.cards["inventario"].configure(text=f"{total_inv}")
        self.cards["consumo"].configure(text=f"{total_consumo}")
        self.cards["economia"].configure(text=f"R$ {total_economia:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    def exportar_pdf(self):
        try:
            dados = [{
                "Total de Equipamentos": self.cards["equipamentos"].cget("text"),
                "Itens no Inventário": self.cards["inventario"].cget("text"),
                "Registros de Consumo": self.cards["consumo"].cget("text"),
                "Economia Total (R$)": self.cards["economia"].cget("text"),
                "Data de Geração": datetime.now().strftime("%d/%m/%Y %H:%M")
            }]
            exportar_pdf_tabela("relatorio_geral.pdf", "Relatório Geral - GreenCode", dados, list(dados[0].keys()))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF: {e}")

    def exportar_excel(self):
        try:
            dados = [{
                "Total de Equipamentos": self.cards["equipamentos"].cget("text"),
                "Itens no Inventário": self.cards["inventario"].cget("text"),
                "Registros de Consumo": self.cards["consumo"].cget("text"),
                "Economia Total (R$)": self.cards["economia"].cget("text"),
                "Data de Geração": datetime.now().strftime("%d/%m/%Y %H:%M")
            }]
            exportar_excel("relatorio_geral.xlsx", dados)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar Excel: {e}")