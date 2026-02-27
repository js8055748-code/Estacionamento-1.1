from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def gerar_cupom_pdf(mov_id, placa, entrada_br, saida_br, valor, caminho=None):
    if caminho is None:
        caminho = f"cupom_{mov_id}.pdf"

    c = canvas.Canvas(caminho, pagesize=A4)
    larg, alt = A4

    y = alt - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "CUPOM FISCAL - ESTACIONAMENTO")
    y -= 40

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"ID: {mov_id}")
    y -= 20
    c.drawString(50, y, f"Placa: {placa}")
    y -= 20
    c.drawString(50, y, f"Entrada: {entrada_br}")
    y -= 20
    c.drawString(50, y, f"Saída:   {saida_br}")
    y -= 30

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"Total a pagar: R$ {valor:.2f}")
    y -= 40

    c.setFont("Helvetica-Oblique", 10)
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    c.drawString(50, y, f"Gerado em: {agora}")
    y -= 20
    c.drawString(50, y, "Obrigado pela preferência!")

    c.showPage()
    c.save()

    return caminho


