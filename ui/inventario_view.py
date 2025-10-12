import customtkinter as ctk
from tkinter import messagebox
from models.inventario_model import InventarioModel
from utils.pdf_export import exportar_pdf
from utils.excel_export import exportar_excel  # ✅ adiciona isso

class InventarioView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.configure(fg_color="#f5f5f5")

        self.label_titulo = ctk.CTkLabel(
            self,
            text="📦 Inventário de Equipamentos",
            font=("Helvetica", 20, "bold"),
            text_color="#2b2b2b"
        )
        self.label_titulo.pack(pady=15)

        self.text_area = ctk.CTkTextbox(self, width=850, height=400, corner_radius=10)
        self.text_area.pack(pady=10)

        # Botões
        self.btn_atualizar = ctk.CTkButton(
            self, text="🔄 Atualizar Lista",
            command=self.atualizar_lista,
            fg_color="#2E8B57", hover_color="#3CB371"
        )
        self.btn_atualizar.pack(pady=5)

        self.btn_pdf = ctk.CTkButton(
            self, text="📄 Exportar PDF",
            command=self.exportar_pdf_inventario,
            fg_color="#4682B4", hover_color="#5B9BD5"
        )
        self.btn_pdf.pack(pady=5)

        # ✅ Novo botão Excel
        self.btn_excel = ctk.CTkButton(
            self,
            text="📊 Exportar Excel",
            command=self.exportar_excel_inventario,
            fg_color="#DAA520",
            hover_color="#FFD700"
        )
        self.btn_excel.pack(pady=5)

        self.atualizar_lista()

    def atualizar_lista(self):
        self.text_area.delete("1.0", "end")
        inventario = InventarioModel().listar_todos()
        if not inventario:
            self.text_area.insert("end", "Nenhum item cadastrado.\n")
            return

        for item in inventario:
            linha = (
                f"id_inventario: {item['id_inventario']} | "
                f"nome: {item['nome']} | "
                f"marca: {item['marca']} | "
                f"descricao: {item['descricao']} | "
                f"identificacao: {item['identificacao']} | "
                f"setor: {item['setor']} | "
                f"valor: {item['valor']} | "
                f"id_equipamento: {item['id_equipamento']} | "
                f"equipamento: {item['equipamento']}\n\n"
            )
            self.text_area.insert("end", linha)

    def exportar_pdf_inventario(self):
        try:
            dados = InventarioModel().listar_todos()
            if not dados:
                messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
                return
            exportar_pdf("Relatório de Inventário", "inventario.pdf", dados)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF:\n{e}")

    # ✅ Função nova para Excel
    def exportar_excel_inventario(self):
        try:
            dados = InventarioModel().listar_todos()
            if not dados:
                messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
                return
            exportar_excel("Relatório de Inventário", "inventario.xlsx", dados)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar Excel:\n{e}")