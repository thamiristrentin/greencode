import customtkinter as ctk
from models.comparativo_model import ComparativoModel
from utils.pdf_export import exportar_pdf
from utils.excel_export import exportar_excel

class ComparativoView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Comparativos de Economia", font=("Arial", 18, "bold")).pack(pady=10)

        form = ctk.CTkFrame(self)
        form.pack(pady=5)

        self.descricao = ctk.CTkEntry(form, placeholder_text="Descrição")
        self.descricao.grid(row=0, column=0, padx=5)
        self.atual = ctk.CTkEntry(form, placeholder_text="Consumo Atual (kWh)")
        self.atual.grid(row=0, column=1, padx=5)
        self.futuro = ctk.CTkEntry(form, placeholder_text="Consumo Futuro (kWh)")
        self.futuro.grid(row=0, column=2, padx=5)

        ctk.CTkButton(form, text="Adicionar", command=self.adicionar).grid(row=0, column=3, padx=10)
        ctk.CTkButton(form, text="Atualizar Lista", command=self.atualizar_lista).grid(row=0, column=4, padx=10)
        ctk.CTkButton(form, text="Exportar PDF", command=self.exportar_pdf).grid(row=0, column=5, padx=10)
        ctk.CTkButton(form, text="Exportar Excel", command=self.exportar_excel).grid(row=0, column=6, padx=10)

        self.lista = ctk.CTkTextbox(self, width=950, height=400)
        self.lista.pack(pady=10)
        self.atualizar_lista()

    def adicionar(self):
        ComparativoModel.adicionar(
            self.descricao.get(),
            float(self.atual.get()),
            float(self.futuro.get())
        )
        self.atualizar_lista()

    def atualizar_lista(self):
        self.lista.delete("1.0", "end")
        dados = ComparativoModel.listar()
        for c in dados:
            linha = f"{c['id_comparativo']} | {c['descricao']} | Atual: {c['consumo_atual_kwh']} | Futuro: {c['consumo_futuro_kwh']} | Economia: {c['economia_reais']} R$\n"
            self.lista.insert("end", linha)

    def exportar_pdf(self):
        dados = ComparativoModel.listar()
        exportar_pdf("Relatório de Comparativos", dados, "comparativos.pdf")

    def exportar_excel(self):
        dados = ComparativoModel.listar()
        exportar_excel(dados, "comparativos.xlsx")