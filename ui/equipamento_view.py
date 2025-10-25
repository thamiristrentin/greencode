import customtkinter as ctk
from tkinter import messagebox, ttk
from models.equipamento_model import EquipamentoModel
from utils.pdf_export import exportar_pdf_tabela
from utils.excel_export import exportar_excel

class EquipamentoView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="⚙️ Equipamentos", font=("Helvetica", 20, "bold")).pack(pady=10)

        tabela_frame = ctk.CTkFrame(self)
        tabela_frame.pack(pady=8, padx=10, fill="both", expand=True)

        self.tree = ttk.Treeview(tabela_frame, columns=(
            "id_equipamento", "nome", "quantidade", "potencia_watts", "horas_uso_diario"
        ), show="headings", height=10)

        for col, title in {
            "id_equipamento": "ID",
            "nome": "Nome",
            "quantidade": "Qtd",
            "potencia_watts": "Potência (W)",
            "horas_uso_diario": "Horas/dia"
        }.items():
            self.tree.heading(col, text=title)
            self.tree.column(col, anchor="center", width=120)

        vsb = ttk.Scrollbar(tabela_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="🔄 Atualizar", command=self.atualizar_lista, fg_color="#2E8B57").grid(row=0, column=0, padx=6)
        ctk.CTkButton(btn_frame, text="➕ Adicionar", command=self.adicionar, fg_color="#4682B4").grid(row=0, column=1, padx=6)
        ctk.CTkButton(btn_frame, text="📄 PDF", command=self.exportar_pdf, fg_color="#5A5AAD").grid(row=0, column=2, padx=6)
        ctk.CTkButton(btn_frame, text="📊 Excel", command=self.exportar_excel, fg_color="#DAA520").grid(row=0, column=3, padx=6)

        form = ctk.CTkFrame(self)
        form.pack(pady=15, padx=10, fill="x")
        self.entry_nome = ctk.CTkEntry(form, placeholder_text="Nome"); self.entry_nome.grid(row=0,column=0,padx=4)
        self.entry_qtd = ctk.CTkEntry(form, placeholder_text="Qtd"); self.entry_qtd.grid(row=0,column=1,padx=4)
        self.entry_pot = ctk.CTkEntry(form, placeholder_text="Potência (W)"); self.entry_pot.grid(row=0,column=2,padx=4)
        self.entry_horas = ctk.CTkEntry(form, placeholder_text="Horas/dia"); self.entry_horas.grid(row=0,column=3,padx=4)

        self.atualizar_lista()

    def atualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for e in EquipamentoModel.listar_todos():
            self.tree.insert("", "end", values=(
                e["id_equipamento"], e["nome"], e["quantidade"], e["potencia_watts"], e["horas_uso_diario"]
            ))

    def adicionar(self):
        try:
            EquipamentoModel.inserir(
                self.entry_nome.get(),
                int(self.entry_qtd.get()),
                float(self.entry_pot.get()),
                float(self.entry_horas.get())
            )
            messagebox.showinfo("Sucesso", "Equipamento adicionado!")
            self.atualizar_lista()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def exportar_pdf(self):
        dados = EquipamentoModel.listar_todos()
        exportar_pdf_tabela("equipamentos.pdf", "Equipamentos Cadastrados", dados,
                            ["id_equipamento", "nome", "quantidade", "potencia_watts", "horas_uso_diario"])

    def exportar_excel(self):
        exportar_excel("equipamentos.xlsx", EquipamentoModel.listar_todos())