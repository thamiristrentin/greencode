import customtkinter as ctk
from ui.equipamento_view import EquipamentoView
from ui.inventario_view import InventarioView
from ui.relatorio_view import RelatorioView
from ui.consumo_view import ConsumoView
from ui.tarifa_view import TarifaView
from ui.comparativo_view import ComparativoView

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GreenCode - Gestão de Energia")
        self.geometry("1100x700")
        self.resizable(True, True)

        ctk.set_appearance_mode("light")

        menu = ctk.CTkFrame(self, width=200, fg_color="#1E3D34")
        menu.pack(side="left", fill="y")

        self.content = ctk.CTkFrame(self, fg_color="#f5f5f5")
        self.content.pack(side="right", fill="both", expand=True)

        botoes = [
            ("Equipamentos", lambda: self.mostrar_tela(EquipamentoView)),
            ("Inventário", lambda: self.mostrar_tela(InventarioView)),
            ("Consumos", lambda: self.mostrar_tela(ConsumoView)),
            ("Tarifas", lambda: self.mostrar_tela(TarifaView)),
            ("Comparativos", lambda: self.mostrar_tela(ComparativoView)),
            ("📊 Relatórios Gerais", lambda: self.mostrar_tela(RelatorioView))
        ]

        for texto, comando in botoes:
            ctk.CTkButton(menu, text=texto, command=comando, fg_color="#3CB371").pack(pady=10, padx=15, fill="x")

        self.tela_atual = None
        self.mostrar_tela(EquipamentoView)

    def mostrar_tela(self, TelaClasse):
        if self.tela_atual:
            self.tela_atual.pack_forget()
        self.tela_atual = TelaClasse(self.content)
        self.tela_atual.pack(fill="both", expand=True)