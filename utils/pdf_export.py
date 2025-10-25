import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from tkinter import messagebox

def exportar_pdf_tabela(nome_arquivo, titulo, dados, colunas):
    caminho = os.path.join(os.getcwd(), nome_arquivo)
    doc = SimpleDocTemplate(caminho, pagesize=landscape(A4))
    styles = getSampleStyleSheet()

    story = [Paragraph(titulo, styles["Title"]), Spacer(1, 15)]

    table_data = [colunas]
    for item in dados:
        linha = [str(item.get(c, "")) for c in colunas]
        table_data.append(linha)

    table = Table(table_data, repeatRows=1, hAlign="CENTER")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    story.append(table)
    doc.build(story)
    messagebox.showinfo("PDF gerado", f"PDF salvo em:\n{caminho}")
