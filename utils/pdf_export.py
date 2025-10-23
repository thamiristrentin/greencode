import os
from tkinter import messagebox
from fpdf import FPDF

def exportar_pdf(titulo, nome_arquivo, dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, titulo, ln=True, align="C")

    pdf.set_font("Helvetica", "B", 12)
    pdf.ln(8)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(25, 8, "ID", 1, 0, "C", True)
    pdf.cell(70, 8, "Nome", 1, 0, "C", True)
    pdf.cell(45, 8, "Setor", 1, 0, "C", True)
    pdf.cell(40, 8, "Valor (R$)", 1, 1, "C", True)

    pdf.set_font("Helvetica", "", 11)
    for item in dados:
        pdf.cell(25, 8, str(item["id_inventario"]), 1, 0, "C")
        pdf.cell(70, 8, item["nome"][:35], 1, 0, "L")
        pdf.cell(45, 8, item["setor"] or "-", 1, 0, "C")
        pdf.cell(40, 8, f"{item['valor']:.2f}" if item["valor"] else "-", 1, 1, "R")

    caminho = os.path.join(os.getcwd(), nome_arquivo)
    pdf.output(caminho)
    messagebox.showinfo("Exportação concluída", f"PDF salvo em:\n{caminho}")
    print(f"📄 PDF salvo em: {caminho}")