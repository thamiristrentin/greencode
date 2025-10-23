import customtkinter as ctk
from tkinter import messagebox
from models.inventario_model import InventarioModel
from utils.pdf_export import exportar_pdf
from utils.excel_export import exportar_excel

class InventarioView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#f8f9fa")

        # Título
        self.label_titulo = ctk.CTkLabel(
            self, text="📦 Inventário de Equipamentos",
            font=("Helvetica", 20, "bold"), text_color="#222"
        )
        self.label_titulo.pack(pady=(20, 10))

        # Text area
        self.text_area = ctk.CTkTextbox(
            self, width=850, height=300,
            corner_radius=10, fg_color="#2b2b2b", text_color="white"
        )
        self.text_area.pack(padx=20, pady=10, expand=True)

        # Frame dos botões principais
        botoes_frame = ctk.CTkFrame(self, fg_color="transparent")
        botoes_frame.pack(pady=10)

        self.btn_atualizar = ctk.CTkButton(
            botoes_frame, text="🔄 Atualizar Lista",
            command=self.atualizar_lista,
            fg_color="#2E8B57", hover_color="#3CB371", width=150
        )
        self.btn_atualizar.grid(row=0, column=0, padx=5)

        self.btn_pdf = ctk.CTkButton(
            botoes_frame, text="📄 Exportar PDF",
            command=self.exportar_pdf_inventario,
            fg_color="#4682B4", hover_color="#5B9BD5", width=150
        )
        self.btn_pdf.grid(row=0, column=1, padx=5)

        self.btn_excel = ctk.CTkButton(
            botoes_frame, text="📊 Exportar Excel",
            command=self.exportar_excel_inventario,
            fg_color="#DAA520", hover_color="#FFD700", width=150
        )
        self.btn_excel.grid(row=0, column=2, padx=5)

        # --------------------
        # CADASTRO DE ITENS
        # --------------------
        form_frame = ctk.CTkFrame(self, fg_color="#343a40", corner_radius=10)
        form_frame.pack(pady=15, padx=20, fill="x")

        ctk.CTkLabel(
            form_frame, text="Cadastro de Itens",
            font=("Helvetica", 16, "bold")
        ).pack(pady=(10, 5))

        entry_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        entry_frame.pack(pady=10)

        self.entry_nome = ctk.CTkEntry(entry_frame, placeholder_text="Nome", width=150)
        self.entry_nome.grid(row=0, column=0, padx=5)

        self.entry_marca = ctk.CTkEntry(entry_frame, placeholder_text="Marca", width=150)
        self.entry_marca.grid(row=0, column=1, padx=5)

        self.entry_desc = ctk.CTkEntry(entry_frame, placeholder_text="Descrição", width=150)
        self.entry_desc.grid(row=0, column=2, padx=5)

        self.entry_setor = ctk.CTkEntry(entry_frame, placeholder_text="Setor", width=150)
        self.entry_setor.grid(row=0, column=3, padx=5)

        self.entry_valor = ctk.CTkEntry(entry_frame, placeholder_text="Valor", width=100)
        self.entry_valor.grid(row=0, column=4, padx=5)

        self.entry_id_equip = ctk.CTkEntry(entry_frame, placeholder_text="ID Equipamento", width=120)
        self.entry_id_equip.grid(row=0, column=5, padx=5)

        # Botões de cadastro
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(pady=5)

        self.btn_add = ctk.CTkButton(
            btn_frame, text="➕ Adicionar", command=self.adicionar_item,
            fg_color="#2E8B57", hover_color="#3CB371", width=120
        )
        self.btn_add.grid(row=0, column=0, padx=5)

        self.btn_refresh = ctk.CTkButton(
            btn_frame, text="🔁 Atualizar Lista",
            command=self.atualizar_lista,
            fg_color="#2E8B57", hover_color="#3CB371", width=140
        )
        self.btn_refresh.grid(row=0, column=1, padx=5)

        self.atualizar_lista()

    # ---------------------------
    # FUNÇÕES
    # ---------------------------
    def atualizar_lista(self):
        self.text_area.delete("1.0", "end")
        inventario = InventarioModel().listar_todos()
        if not inventario:
            self.text_area.insert("end", "Nenhum item cadastrado.\n")
            return

        for item in inventario:
            linha = (
                f"🆔 {item['id_inventario']} | "
                f"📦 {item['nome']} | "
                f"🏷️ {item['marca']} | "
                f"💬 {item['descricao']} | "
                f"🏢 {item['setor']} | "
                f"💰 R${item['valor']:.2f} | "
                f"🔗 Equipamento: {item['id_equipamento']}\n"
            )
            self.text_area.insert("end", linha)

    def adicionar_item(self):
        nome = self.entry_nome.get()
        marca = self.entry_marca.get()
        descricao = self.entry_desc.get()
        setor = self.entry_setor.get()
        valor = self.entry_valor.get()
        id_equip = self.entry_id_equip.get()

        if not nome or not marca or not descricao:
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")
            return

        InventarioModel().inserir(nome, marca, descricao, setor, valor, id_equip)
        messagebox.showinfo("Sucesso", "Item adicionado ao inventário.")
        self.atualizar_lista()

    def exportar_pdf_inventario(self):
        dados = InventarioModel().listar_todos()
        if not dados:
            messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
            return

        nome_arquivo = "relatorio_inventario.pdf"
        exportar_pdf("Relatório de Inventário", nome_arquivo, dados)
        messagebox.showinfo("PDF Gerado", f"📄 PDF salvo como: {nome_arquivo}")

    def exportar_excel_inventario(self):
        dados = InventarioModel().listar_todos()
        if not dados:
            messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
            return

        nome_arquivo = "relatorio_inventario.xlsx"
        exportar_excel("Inventário", nome_arquivo, dados)
        messagebox.showinfo("Excel Gerado", f"📊 Planilha salva como: {nome_arquivo}")
