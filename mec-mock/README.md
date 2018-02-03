# Dependências
* Python 2.7
* Flask

# Criando o certificado
```
$ openssl req -newkey rsa:2048 -nodes -keyout mec-priv.key -x509 -days 365 -out mec-certf.crt
```

Atentar para campo que pede o hostname (ou o nome, ele é solicitado antes do email), colocar o ip do servidor ou o endereço (ex.: 10.0.0.104)

# Adicionando o certificado ao Zato
Security > SSL/TLS > Outgoing > CA Certs > Upload a CA Certificate

# Integrando o serviço externo ao Zato
Connections > Outgoing > Plain HTTP > Create a new Plain HTTP outgoing connection

* No campo "host", substituir http por https;
* No campo "security definition", selecionar "No Security definition";
* No campo "TLS CA Certs", selecionar o adicionado anteriormente;

# Rodando o servidor
```
$ python mec-mock.py
```

# Requisitando via CURL
```
$ curl --cacert <path>/mec-certf.crt https://<host>:5000/mec/envia; echo
```
