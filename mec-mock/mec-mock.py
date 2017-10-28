#!/usr/bin/python

import ssl
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/mec/envia', methods = ['GET'])
def mec_envia():
    resposta = {}
    resposta['recebido'] = 'True'
    return jsonify(resposta)

if __name__ == '__main__':

	context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
	context.load_cert_chain('mec-certf.crt', 'mec-priv.key')

	app.run(host='0.0.0.0', ssl_context=context)
