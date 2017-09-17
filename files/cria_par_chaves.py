from peewee import *
from dao import Chave
import rsa

(chave_pub, chave_priv) = rsa.newkeys(512)

Chave.create(tipo='privada', valor=chave_priv.save_pkcs1('PEM'))
Chave.create(tipo='publica', valor=chave_pub.save_pkcs1('PEM'))