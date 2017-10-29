from httplib import NO_CONTENT
from zato.server.service import Service
from dao import *
from peewee import *
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
from json import dumps, loads
from zato.common import DATA_FORMAT
from base64 import b64encode

def genera_pdf(aluno, qrcode):
    canva = canvas.Canvas(None)
    canva.setLineWidth(.3)
    canva.setFont('Helvetica', 12)
    
    canva.drawImage(ImageReader(qrcode), 30, 770, width=50, height=50)

    canva.drawString(30, 750, 'Aluno:')
    canva.drawString(80, 750, aluno['nome'])
    canva.drawString(30, 735, 'Curso:')
    canva.drawString(80, 735, aluno['curso'])
    canva.line(30, 730, 580, 730)
    
    coord_y = 713 
    canva.drawString(30, 718,'Disciplina')
    canva.drawString(550, 718,'Nota')
    canva.line(30, coord_y, 580, coord_y)

    for hist in aluno['historico']:
        coord_y = coord_y - 20
        canva.drawString(30, coord_y, hist['disciplina'])
        canva.drawString(555, coord_y, str(hist['nota']))

    return canva.getpdfdata()

class GeraHistorico(Service):
    
    def handle_POST(self):
        # Recebe dados via POST
        dados_historico = self.request.payload

        # busca no BD
        aluno = {}
        aluno_obj = Aluno.get(Aluno.matricula == dados_historico['matricula'])
        aluno['nome'] = aluno_obj.nome
        aluno['curso']= Curso.get(Curso.id == aluno_obj.curso).nome

        historico = []
        for hist in Historico.select().where(Historico.aluno == aluno_obj):
            disc = Disciplina.get(Disciplina.id == hist.disciplina)
            historico.append({'disciplina': disc.nome, 'nota': hist.nota})
        
        aluno['historico'] = historico

        # Assinatura Eletronica
        serv_assinatura = 'serv-assinatura-eletronica.assina-doc'
        resp_assin = self.invoke(serv_assinatura, dumps(aluno), data_format=DATA_FORMAT.JSON)
        resp_assin = loads(resp_assin)
        qrcode = Image.frombytes(resp_assin['mode'], 
                                 resp_assin['size'], 
                                 resp_assin['data'].decode('base64'))

        # PDF
        pdf = genera_pdf(aluno, qrcode)

        # Retorna o pdf como resposta
        self.response.payload = b64encode(pdf)
        self.response.content_type = 'application/pdf'