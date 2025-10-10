import customtkinter as ctk
from models.equipamento_model import EquipamentoModel

class EquipamentoView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Cadastro de Equipamentos", font=("Arial", 18, "bold")).pack(pady=10)

        frame = ctk.CTkFrame(self)
        frame.pack(pady=10)

        self.nome = ctk.CTkEntry(frame, placeholder_text="Nome")
        self.nome.grid(row=0, column=0, padx=5)
        self.quantidade = ctk.CTkEntry(frame, placeholder_text="Quantidade")
        self.quantidade.grid(row=0, column=1, padx=5)
        self.potencia = ctk.CTkEntry(frame, placeholder_text="Potência (W)")
        self.potencia.grid(row=0, column=2, padx=5)
        self.horas = ctk.CTkEntry(frame, placeholder_text="Horas/dia")
        self.horas.grid(row=0, column=3, padx=5)

        ctk.CTkButton(frame, text="Adicionar", command=self.adicionar).grid(row=0, column=4, padx=10)
        ctk.CTkButton(frame, text="Atualizar Lista", command=self.atualizar_lista).grid(row=0, column=5, padx=10)

        self.lista = ctk.CTkTextbox(self, width=900, height=400)
        self.lista.pack(pady=10)
        self.atualizar_lista()

    def adicionar(self):
        EquipamentoModel.adicionar(
            self.nome.get(),
            int(self.quantidade.get()),
            float(self.potencia.get()),
            float(self.horas.get())
        )
        self.atualizar_lista()

    def atualizar_lista(self):
        self.lista.delete("1.0", "end")
        equipamentos = EquipamentoModel.listar()
        for eq in equipamentos:
            linha = f"{eq['id_equipamento']} | {eq['nome']} | {eq['quantidade']} | {eq['potencia_watts']}W | {eq['horas_uso_diario']}h/dia\n"
            self.lista.insert("end", linha)