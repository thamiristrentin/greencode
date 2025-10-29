import customtkinter as ctk
from tkinter import ttk, messagebox
from models.relatorios_model import RelatoriosModel
from utils.pdf_export import exportar_pdf_tabela
from utils.excel_export import exportar_excel
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class RelatorioView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#f5f5f5")

        # === TÍTULO ===
        ctk.CTkLabel(
            self, text="📊 Relatórios Gerais",
            font=("Helvetica", 20, "bold")
        ).pack(pady=10)

        # === CARDS DE DADOS ===
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(pady=5)

        self.card_eqp = self.criar_card(cards_frame, "⚙️ Equipamentos", "0", 0)
        self.card_inv = self.criar_card(cards_frame, "📦 Itens de Inventário", "0", 1)
        self.card_cons = self.criar_card(cards_frame, "⚡ Registros de Consumo", "0", 2)
        self.card_eco = self.criar_card(cards_frame, "💰 Economia Total (R$)", "0.00", 3)

        # === TABELA ===
        tabela_frame = ctk.CTkFrame(self)
        tabela_frame.pack(pady=15, padx=10, fill="both", expand=True)

        self.tree = ttk.Treeview(
            tabela_frame,
            columns=("equipamento", "setor", "potencia", "consumo", "custo", "economia"),
            show="headings", height=10
        )

        colunas = {
            "equipamento": "Equipamento",
            "setor": "Setor",
            "potencia": "Potência (W)",
            "consumo": "Consumo (kWh)",
            "custo": "Custo (R$)",
            "economia": "Economia (R$)"
        }

        for col, titulo in colunas.items():
            self.tree.heading(col, text=titulo)
            self.tree.column(col, anchor="center", width=150)

        vsb = ttk.Scrollbar(tabela_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # === GRÁFICO ===
        self.grafico_frame = ctk.CTkFrame(self)
        self.grafico_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # === BOTÕES ===
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="🔄 Atualizar", command=self.atualizar_tela, fg_color="#2E8B57").grid(row=0, column=0, padx=6)
        ctk.CTkButton(btn_frame, text="📄 Exportar PDF", command=self.exportar_pdf, fg_color="#5A5AAD").grid(row=0, column=1, padx=6)
        ctk.CTkButton(btn_frame, text="📊 Exportar Excel", command=self.exportar_excel, fg_color="#DAA520").grid(row=0, column=2, padx=6)

        self.atualizar_tela()

    # === CARD TEMPLATE ===
    def criar_card(self, parent, titulo, valor, coluna):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=8)
        card.grid(row=0, column=coluna, padx=10, pady=5)
        ctk.CTkLabel(card, text=titulo, font=("Helvetica", 13, "bold")).pack(pady=(8, 0))
        label_valor = ctk.CTkLabel(card, text=valor, font=("Helvetica", 15))
        label_valor.pack(pady=(0, 8))
        return label_valor

    # === ATUALIZAR TELA COMPLETA ===
    def atualizar_tela(self):
        try:
            dados = RelatoriosModel.listar_todos()

            # Atualiza cards
            self.card_eqp.configure(text=str(dados["equipamentos"]))
            self.card_inv.configure(text=str(dados["inventario"]))
            self.card_cons.configure(text=str(dados["consumo"]))
            self.card_eco.configure(text=f"R$ {dados['economia_total']:.2f}")

            # Limpa tabela
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insere tabela formatada
            for d in dados["tabela"]:
                self.tree.insert("", "end", values=(
                    d["equipamento"],
                    d["setor"],
                    d["potencia"],
                    d["consumo_kwh"],
                    f"{d['custo']:.2f}",
                    f"{d['economia']:.2f}"
                ))

            # Atualiza gráfico
            self.atualizar_grafico(dados["tabela"])

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar relatório:\n{e}")

    # === GRÁFICO DE CONSUMO X ECONOMIA ===
    def atualizar_grafico(self, dados):
        # Limpa gráfico anterior
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()

        equipamentos = [d["equipamento"] for d in dados]
        consumo = [d["consumo_kwh"] for d in dados]
        economia = [d["economia"] for d in dados]

        if not equipamentos:
            return

        fig = Figure(figsize=(6, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(equipamentos, consumo, label="Consumo (kWh)", alpha=0.7)
        ax.bar(equipamentos, economia, label="Economia (R$)", alpha=0.7)
        ax.set_title("Comparativo de Consumo e Economia", fontsize=10)
        ax.set_ylabel("Valores")
        ax.legend()
        ax.tick_params(axis="x", rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # === EXPORTAR PDF ===
    def exportar_pdf(self):
        try:
            dados = RelatoriosModel.listar_todos()["tabela"]
            exportar_pdf_tabela(
                "relatorios_gerais.pdf",
                "Relatórios Gerais",
                dados,
                ["equipamento", "setor", "potencia", "consumo_kwh", "custo", "economia"]
            )
            messagebox.showinfo("Sucesso", "PDF salvo como 'relatorios_gerais.pdf'")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar PDF:\n{e}")

    # === EXPORTAR EXCEL ===
    def exportar_excel(self):
        try:
            dados = RelatoriosModel.listar_todos()["tabela"]
            exportar_excel("relatorios_gerais.xlsx", dados)
            messagebox.showinfo("Sucesso", "Excel salvo como 'relatorios_gerais.xlsx'")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar Excel:\n{e}")
