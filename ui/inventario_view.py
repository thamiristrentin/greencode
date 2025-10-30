
import customtkinter as ctk
from tkinter import messagebox, ttk
from models.inventario_model import InventarioModel
from utils.pdf_export import exportar_pdf_tabela
from utils.excel_export import exportar_excel

class InventarioView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="📦 Inventário de Equipamentos", font=("Helvetica", 20, "bold")).pack(pady=10)

        tabela_frame = ctk.CTkFrame(self)
        tabela_frame.pack(pady=8, padx=10, fill="both", expand=True)

        self.tree = ttk.Treeview(tabela_frame, columns=(
            "id_inventario", "nome", "marca", "descricao", "setor", "valor", "equipamento"
        ), show="headings", height=10)

        col_titles = {
            "id_inventario": "ID",
            "nome": "Nome",
            "marca": "Marca",
            "descricao": "Descrição",
            "setor": "Setor",
            "valor": "Valor (R$)",
            "equipamento": "Equipamento"
        }

        for col, title in col_titles.items():
            self.tree.heading(col, text=title)
            self.tree.column(col, anchor="center", width=120)

        vsb = ttk.Scrollbar(tabela_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="🔄 Atualizar Lista", command=self.atualizar_lista, fg_color="#2E8B57").grid(row=0, column=0, padx=6)
        ctk.CTkButton(btn_frame, text="➕ Adicionar Item", command=self.adicionar_item, fg_color="#4682B4").grid(row=0, column=1, padx=6)
        ctk.CTkButton(btn_frame, text="📄 Exportar PDF", command=self.exportar_pdf_inventario, fg_color="#5A5AAD").grid(row=0, column=2, padx=6)
        ctk.CTkButton(btn_frame, text="📊 Exportar Excel", command=self.exportar_excel_inventario, fg_color="#DAA520").grid(row=0, column=3, padx=6)

        form = ctk.CTkFrame(self)
        form.pack(pady=15, padx=10, fill="x")
        self.entry_nome = ctk.CTkEntry(form, placeholder_text="Nome"); self.entry_nome.grid(row=0,column=0,padx=4)
        self.entry_marca = ctk.CTkEntry(form, placeholder_text="Marca"); self.entry_marca.grid(row=0,column=1,padx=4)
        self.entry_desc = ctk.CTkEntry(form, placeholder_text="Descrição"); self.entry_desc.grid(row=0,column=2,padx=4)
        self.entry_setor = ctk.CTkEntry(form, placeholder_text="Setor"); self.entry_setor.grid(row=0,column=3,padx=4)
        self.entry_valor = ctk.CTkEntry(form, placeholder_text="Valor (R$)"); self.entry_valor.grid(row=0,column=4,padx=4)
        self.entry_id_equip = ctk.CTkEntry(form, placeholder_text="ID Equipamento"); self.entry_id_equip.grid(row=0,column=5,padx=4)

        self.atualizar_lista()

    def atualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        inventario = InventarioModel.listar_todos()
        if not inventario:
            messagebox.showinfo("Aviso", "Nenhum item cadastrado no inventário.")
            return

        for item in inventario:
            self.tree.insert("", "end", values=(
                item["id_inventario"],
                item["nome"],
                item["marca"],
                item["descricao"],
                item["setor"],
                f"{item['valor']:.2f}",
                item["equipamento"]
            ))

    def adicionar_item(self):
        try:
            InventarioModel.inserir(
                self.entry_nome.get(),
                self.entry_marca.get(),
                self.entry_desc.get(),
                self.entry_setor.get(),
                float(self.entry_valor.get()) if self.entry_valor.get() else 0,
                int(self.entry_id_equip.get()) if self.entry_id_equip.get() else None,
                None
            )
            messagebox.showinfo("Sucesso", "Item adicionado ao inventário!")
            self.entry_nome.delete(0, "end")
            self.atualizar_lista()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def exportar_pdf_inventario(self):
        dados = InventarioModel.listar_todos()
        if not dados:
            messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
            return
        colunas = ["id_inventario", "nome", "marca", "descricao", "setor", "valor", "equipamento"]
        exportar_pdf_tabela("inventario.pdf", "Inventário de Equipamentos", dados, colunas)

    def exportar_excel_inventario(self):
        dados = InventarioModel.listar_todos()
        if not dados:
            messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
            return
        exportar_excel("inventario.xlsx", dados)