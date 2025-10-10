from fpdf import FPDF

def exportar_pdf(titulo, dados, nome_arquivo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, titulo, ln=True, align="C")

    pdf.set_font("Arial", size=10)
    pdf.ln(10)

    for linha in dados:
        texto = " | ".join([f"{k}: {v}" for k, v in linha.items()])
        pdf.multi_cell(0, 8, texto)
        pdf.ln(2)

    pdf.output(nome_arquivo)
    print(f"✅ PDF exportado: {nome_arquivo}")