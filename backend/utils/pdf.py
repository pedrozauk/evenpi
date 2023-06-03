from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from svglib.svglib import svg2rlg

from io import BytesIO

def gerar_certificado(dados: dict):
    """
    Espera um dict com { "nome": valor,
                         "cpf": valor,
                         "descricao":valor,
                         "carga_horaria":valor
                            }
    """
    # Cria um objeto Canvas usando o tamanho da página 'letter'
    template = svg2rlg("backend/utils/templates_pdf/certificado.svg")
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    renderPDF.draw(template, c, 0, 0)

    # Adicione o conteúdo dinâmico ao certificado
    c.drawString(100, 750, f'Certificado da atividade {dados.get("descricao")}')
    c.drawString(100, 700, f'Nome:  {dados.get("nome")} ')
    c.drawString(100, 650, f'Carga Horaria: {dados.get("carga_horaria")} horas')

    # Fecha o Canvas
    c.showPage()
    c.save()

    return pdf_buffer