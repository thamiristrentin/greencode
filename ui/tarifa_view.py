import customtkinter as ctk
from models.tarifa_model import TarifaModel
from utils.pdf_export import exportar_pdf
from utils.excel_export import exportar_excel

class TarifaView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Gerenciamento de Tarifas", font=("Arial", 18, "bold")).pack(pady=10)

        form = ctk.CTkFrame(self)
        form.pack(pady=5)

        self.valor = ctk.CTkEntry(form, placeholder_text="Valor kWh")
        self.valor.grid(row=0, column=0, padx=5)
        self.inicio = ctk.CTkEntry(form, placeholder_text="Início (AAAA-MM-DD)")
        self.inicio.grid(row=0, column=1, padx=5)
        self.fim = ctk.CTkEntry(form, placeholder_text="Fim (AAAA-MM-DD ou NULL)")
        self.fim.grid(row=0, column=2, padx=5)

        ctk.CTkButton(form, text="Adicionar", command=self.adicionar).grid(row=0, column=3, padx=10)
        ctk.CTkButton(form, text="Atualizar Lista", command=self.atualizar_lista).grid(row=0, column=4, padx=10)
        ctk.CTkButton(form, text="Exportar PDF", command=self.exportar_pdf).grid(row=0, column=5, padx=10)
        ctk.CTkButton(form, text="Exportar Excel", command=self.exportar_excel).grid(row=0, column=6, padx=10)

        self.lista = ctk.CTkTextbox(self, width=950, height=400)
        self.lista.pack(pady=10)
        self.atualizar_lista()

    def adicionar(self):
        TarifaModel.adicionar(
            float(self.valor.get()),
            self.inicio.get(),
            self.fim.get() if self.fim.get().lower() != "null" else None
        )
        self.atualizar_lista()

    def atualizar_lista(self):
        self.lista.delete("1.0", "end")
        dados = TarifaModel.listar()
        for t in dados:
            linha = f"{t['id_tarifa']} | R${t['valor_kwh']} | {t['vigencia_inicio']} → {t['vigencia_fim']}\n"
            self.lista.insert("end", linha)

    def exportar_pdf(self):
        dados = TarifaModel.listar()
        exportar_pdf("Relatório de Tarifas", dados, "tarifas.pdf")

    def exportar_excel(self):
        dados = TarifaModel.listar()
        exportar_excel(dados, "tarifas.xlsx")
