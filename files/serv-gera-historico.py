from httplib import NO_CONTENT
from zato.server.service import Service
from dao import *
from peewee import *
from reportlab.pdfgen import canvas

def genera_pdf(aluno, historico):
    canva = canvas.Canvas(None)
    canva.setLineWidth(.3)
    canva.setFont('Helvetica', 12)
     
    canva.drawString(30, 750, 'Aluno:')
    canva.drawString(80, 750, aluno['nome'])
    canva.drawString(30, 735, 'Curso:')
    canva.drawString(80, 735, aluno['curso'])
    canva.line(30, 730, 580, 730)
    
    coord_y = 713 
    canva.drawString(30, 718,'Disciplina')
    canva.drawString(550, 718,'Nota')
    canva.line(30, coord_y, 580, coord_y)

    for hist in historico:
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
        aluno['obj'] = Aluno.get(Aluno.matricula == dados_historico['matricula'])
        aluno['nome'] = aluno['obj'].nome
        aluno['curso']= Curso.get(Curso.id == aluno['obj'].curso).nome

        historico = []
        for hist in Historico.select().where(Historico.aluno == aluno['obj']):
            disc = Disciplina.get(Disciplina.id == hist.disciplina)
            historico.append({'disciplina': disc.nome, 'nota': hist.nota})

        # PDF
        pdf = genera_pdf(aluno, historico)

        # Retorna o pdf como resposta
        self.response.content_type = 'application/pdf'
        self.response.payload = pdf
