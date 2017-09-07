from httplib import NO_CONTENT
from zato.server.service import Service
from dao import *
from peewee import *

class CadastraCurso(Service):
    
    def handle_POST(self):

        # Recebe dados via POST
        dados_curso = self.request.payload

        # Persiste dados no BD
        curso = Curso(nome=dados_curso['nome'], envio_mec=dados_curso['envio_mec'])
        curso.save()
        
        for disciplina in dados_curso['disciplinas']:
            professor = Professor.get(Professor.nome == disciplina['professor'])
            disciplina['professor'] = professor

            disciplina['curso'] = curso
            Disciplina(**disciplina).save()

        # Envia dados para o MEC
        if dados_curso['envio_mec'] == "True":
            servico_mec = self.outgoing.plain_http.get('MEC')
            reposta_mec = servico_mec.conn.send(self.cid, self.request.payload)

            erro_reposta_mec = (reposta_mec['recebido'] == 'True')
                
        # Define Reposta
        resposta = {}
        resposta['Persistencia'] = 'True'
        resposta['Envio_MEC'] = 'True' 

        # Retorna a resposta se houve persistencia e envio p/ MEC
        self.response.payload = resposta
