import customtkinter as ctk
from ui.equipamento_view import EquipamentoView
from ui.inventario_view import InventarioView
from ui.tarifa_view import TarifaView
from ui.consumo_view import ConsumoView
from ui.comparativo_view import ComparativoView
from ui.relatorio_view import RelatorioView

class MainWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        sidebar = ctk.CTkFrame(self, width=220)
        sidebar.pack(side="left", fill="y")

        botoes = [
            ("Equipamentos", EquipamentoView),
            ("Inventário", InventarioView),
            ("Tarifas", TarifaView),
            ("Consumos", ConsumoView),
            ("Comparativos", ComparativoView),
            ("Relatórios", RelatorioView)
        ]

        for nome, tela in botoes:
            ctk.CTkButton(sidebar, text=nome, width=200,
                          command=lambda t=tela: self.trocar_tela(t)).pack(pady=8)

        self.frame_principal = None
        self.trocar_tela(EquipamentoView)

    def trocar_tela(self, tela):
        if self.frame_principal:
            self.frame_principal.destroy()
        self.frame_principal = tela(self)
        self.frame_principal.pack(fill="both", expand=True)