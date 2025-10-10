import customtkinter as ctk
from models.inventario_model import InventarioModel
from utils.pdf_export import exportar_pdf
from utils.excel_export import exportar_excel

class InventarioView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Inventário de Equipamentos", font=("Arial", 18, "bold")).pack(pady=10)
        
        form = ctk.CTkFrame(self)
        form.pack(pady=5)

        self.nome = ctk.CTkEntry(form, placeholder_text="Nome")
        self.nome.grid(row=0, column=0, padx=5)
        self.marca = ctk.CTkEntry(form, placeholder_text="Marca")
        self.marca.grid(row=0, column=1, padx=5)
        self.descricao = ctk.CTkEntry(form, placeholder_text="Descrição")
        self.descricao.grid(row=0, column=2, padx=5)
        self.identificacao = ctk.CTkEntry(form, placeholder_text="Identificação")
        self.identificacao.grid(row=1, column=0, padx=5, pady=5)
        self.setor = ctk.CTkEntry(form, placeholder_text="Setor")
        self.setor.grid(row=1, column=1, padx=5, pady=5)
        self.valor = ctk.CTkEntry(form, placeholder_text="Valor (R$)")
        self.valor.grid(row=1, column=2, padx=5, pady=5)
        self.id_equipamento = ctk.CTkEntry(form, placeholder_text="ID Equipamento")
        self.id_equipamento.grid(row=1, column=3, padx=5, pady=5)

        ctk.CTkButton(form, text="Adicionar", command=self.adicionar).grid(row=2, column=0, padx=10, pady=10)
        ctk.CTkButton(form, text="Atualizar Lista", command=self.atualizar_lista).grid(row=2, column=1, padx=10)
        ctk.CTkButton(form, text="Exportar PDF", command=self.exportar_pdf).grid(row=2, column=2, padx=10)
        ctk.CTkButton(form, text="Exportar Excel", command=self.exportar_excel).grid(row=2, column=3, padx=10)

        self.lista = ctk.CTkTextbox(self, width=950, height=400)
        self.lista.pack(pady=10)
        self.atualizar_lista()

    def adicionar(self):
        InventarioModel.adicionar(
            self.nome.get(),
            self.marca.get(),
            self.descricao.get(),
            self.identificacao.get(),
            self.setor.get(),
            float(self.valor.get()),
            int(self.id_equipamento.get())
        )
        self.atualizar_lista()

    def atualizar_lista(self):
        self.lista.delete("1.0", "end")
        dados = InventarioModel.listar()
        for i in dados:
            linha = f"{i['id_inventario']} | {i['nome']} | {i['marca']} | {i['setor']} | {i['valor']} | Equip: {i['equipamento']}\n"
            self.lista.insert("end", linha)

    def exportar_pdf(self):
        dados = InventarioModel.listar()
        exportar_pdf("Relatório de Inventário", dados, "inventario.pdf")

    def exportar_excel(self):
        dados = InventarioModel.listar()
        exportar_excel(dados, "inventario.xlsx")