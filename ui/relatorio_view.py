import customtkinter as ctk
from models.relatorios_model import RelatoriosModel
from utils.pdf_export import exportar_pdf
from utils.excel_export import exportar_excel
import matplotlib.pyplot as plt

class RelatorioView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Relatórios e Gráficos", font=("Arial", 18, "bold")).pack(pady=10)

        ctk.CTkButton(self, text="Gerar Relatório Geral", command=self.mostrar_relatorio).pack(pady=5)
        ctk.CTkButton(self, text="Exportar PDF", command=self.exportar_pdf).pack(pady=5)
        ctk.CTkButton(self, text="Exportar Excel", command=self.exportar_excel).pack(pady=5)
        ctk.CTkButton(self, text="Mostrar Gráfico", command=self.gerar_grafico).pack(pady=5)

        self.texto = ctk.CTkTextbox(self, width=950, height=400)
        self.texto.pack(pady=10)

    def mostrar_relatorio(self):
        self.texto.delete("1.0", "end")
        consumos = RelatoriosModel.resumo_consumo()
        economia = RelatoriosModel.economia_total()

        self.texto.insert("end", "=== RESUMO DE CONSUMOS ===\n")
        for c in consumos:
            linha = f"{c['equipamento']}: {c['consumo_total']} kWh | R$ {c['custo_total']}\n"
            self.texto.insert("end", linha)

        self.texto.insert("end", "\n=== ECONOMIA TOTAL ===\n")
        self.texto.insert("end", f"Economia total: {economia['total_kwh']} kWh | R$ {economia['total_reais']}\n")

    def exportar_pdf(self):
        dados = RelatoriosModel.resumo_consumo()
        exportar_pdf("Relatório Geral de Consumo", dados, "relatorio_geral.pdf")

    def exportar_excel(self):
        dados = RelatoriosModel.resumo_consumo()
        exportar_excel(dados, "relatorio_geral.xlsx")

    def gerar_grafico(self):
        dados = RelatoriosModel.resumo_consumo()
        equipamentos = [d['equipamento'] for d in dados]
        consumo = [float(d['consumo_total']) for d in dados]
        custo = [float(d['custo_total']) for d in dados]

        plt.figure(figsize=(10, 5))
        plt.bar(equipamentos, consumo, color='green', alpha=0.7, label='Consumo (kWh)')
        plt.plot(equipamentos, custo, color='orange', marker='o', label='Custo (R$)')
        plt.title("Consumo Mensal e Custo por Equipamento")
        plt.xlabel("Equipamento")
        plt.ylabel("Consumo / Custo")
        plt.xticks(rotation=30)
        plt.legend()
        plt.tight_layout()
        plt.show()