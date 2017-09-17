from zato.server.service import Service
from dao import Chave
from json import dumps
import qrcode
import rsa
import bz2

class AssinaDoc(Service):

	def handle(self):
		dados = dumps(self.request.payload)

		chave_priv_pem = Chave.get(Chave.tipo == 'privada')
		chave_priv = rsa.PrivateKey.load_pkcs1(chave_priv_pem.valor)

		dados_bz2 = bz2.compress(dados)
		dados_cript = rsa.sign(dados_bz2, chave_priv, 'SHA-1')
		qr = qrcode.make(dados_cript)

		reposta = {}
		reposta['mode'] = qr.mode
		reposta['size'] = qr.size
		reposta['data'] = qr.tobytes().encode('base64')

		self.response.payload = dumps(reposta)