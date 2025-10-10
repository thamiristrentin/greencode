import customtkinter as ctk
from models.consumo_model import ConsumoModel
from utils.pdf_export import exportar_pdf
from utils.excel_export import exportar_excel

class ConsumoView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="Cálculo de Consumos", font=("Arial", 18, "bold")).pack(pady=10)
        form = ctk.CTkFrame(self)
        form.pack(pady=5)

        self.id_equip = ctk.CTkEntry(form, placeholder_text="ID Equipamento")
        self.id_equip.grid(row=0, column=0, padx=5)
        self.id_tarifa = ctk.CTkEntry(form, placeholder_text="ID Tarifa")
        self.id_tarifa.grid(row=0, column=1, padx=5)
        self.data = ctk.CTkEntry(form, placeholder_text="Data (AAAA-MM-DD)")
        self.data.grid(row=0, column=2, padx=5)

        ctk.CTkButton(form, text="Calcular e Salvar", command=self.calcular).grid(row=0, column=3, padx=10)
        ctk.CTkButton(form, text="Atualizar Lista", command=self.atualizar_lista).grid(row=0, column=4, padx=10)
        ctk.CTkButton(form, text="Exportar PDF", command=self.exportar_pdf).grid(row=0, column=5, padx=10)
        ctk.CTkButton(form, text="Exportar Excel", command=self.exportar_excel).grid(row=0, column=6, padx=10)

        self.lista = ctk.CTkTextbox(self, width=950, height=400)
        self.lista.pack(pady=10)
        self.atualizar_lista()

    def calcular(self):
        id_equip = int(self.id_equip.get())
        id_tarifa = int(self.id_tarifa.get())
        data = self.data.get()

        resultado = ConsumoModel.calcular_consumo(id_equip, id_tarifa)
        if resultado:
            ConsumoModel.adicionar(id_equip, id_tarifa, data, *resultado)
            self.atualizar_lista()

    def atualizar_lista(self):
        self.lista.delete("1.0", "end")
        dados = ConsumoModel.listar()
        for c in dados:
            linha = f"{c['id_consumo']} | {c['equipamento']} | {c['data_calculo']} | {c['consumo_mensal_kwh']} kWh | R${c['custo_mensal']}\n"
            self.lista.insert("end", linha)

    def exportar_pdf(self):
        dados = ConsumoModel.listar()
        exportar_pdf("Relatório de Consumos", dados, "consumos.pdf")

    def exportar_excel(self):
        dados = ConsumoModel.listar()
        exportar_excel(dados, "consumos.xlsx")
