from httplib import NO_CONTENT
from zato.server.service import Service
from json import dumps
from dao import *
from peewee import *
from enviomec import EnvioMEC

class CadastraCurso(Service):
    
    def handle_POST(self):

        # Recebe dados via POST
        dados_curso = self.request.payload

        # Envia dados para o MEC
        if dados_curso['envio_mec'] == "True":

            servico_mec = self.outgoing.plain_http.get('MEC')
            resposta_mec = servico_mec.conn.post(self.cid, dumps(self.request.payload))

            if not resposta_mec.ok:
                self.logger.info('Envio para o mec não foi realizado com sucesso.')


        # Persiste dados no BD
        curso = Curso(nome=dados_curso['nome'], envio_mec=dados_curso['envio_mec'])
        curso.save()
        
        for disciplina in dados_curso['disciplinas']:
            professor = Professor.get(Professor.nome == disciplina['professor'])
            disciplina['professor'] = professor

            disciplina['curso'] = curso
            Disciplina(**disciplina).save()

        # Define Reposta
        resposta = {}
        resposta['Persistencia'] = 'True'
        resposta['Envio_MEC'] = 'True' 

        # Retorna a resposta se houve persistencia e envio p/ MEC
        self.response.payload = resposta
