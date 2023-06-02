from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from io import BytesIO

def gerar_certificado(dados: dict):
    # Cria um objeto Canvas usando o tamanho da página 'letter'
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)


    # Adicione o conteúdo dinâmico ao certificado
    c.drawString(100, 750, 'Certificado de Participação')
    c.drawString(100, 700, 'Nome: John Doe')
    c.drawString(100, 650, 'Evento: Workshop de Python')

    # Fecha o Canvas
    c.showPage()
    c.save()

    return pdf_buffer