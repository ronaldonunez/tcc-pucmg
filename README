# Descrição

Implementação dos serviços que compõe o sistema acadêmico, tema do TCC
do curso de Arquitetura de Software distribuído da PUC-Minas.

## Dependencias primárias
* Python 2.7
* Zato 2.0.8 (ESB)

## Instalação das bibliotecas necessárias
As bibliotecas complementares do python necessárias são:

* Peewee
* RSA
* QRCode
* Reportlab
* PyMySQL

Algumas bibliotecas possuem dependências, portanto antes de as instalar
é necessário satisfazer suas dependências:

```
$ sudo aptitude update
$ sudo aptitude install build-essential \
    libfreetype6-dev python-dev python-imaging \
    cython python-pip libtiff5-dev libjpeg8-dev \
    zlib1g-dev libfreetype6-dev liblcms2-dev \
    libwebp-dev libharfbuzz-dev libfribidi-dev \
    tcl8.6-dev tk8.6-dev python-tk mysql-server
```

As bibliotecas necessárias estão disponíveis no serviço pip
```
$ sudo pip install peewee rsa qrcode reportlab PyMySQL
```

As dependências dos serviços devem ser instaladas no diretório 
[ZATO_INST_PATH]/2.0.8/zato_extra_paths. Em geral, ZATO_INST_PATH=/opt/zato.

```
$ sudo -u zato ln -s /usr/local/lib/python2.7/dist-packages/peewee-2.10.2.egg-info/ /home/zato/2.0.8/zato_extra_paths/
$ sudo -u zato ln -s /usr/local/lib/python2.7/dist-packages/peewee-2.10.2.egg-info/ /opt/zato/2.0.8/zato_extra_paths/
$ sudo -u zato ln -s /usr/local/lib/python2.7/dist-packages/peewee.py /opt/zato/2.0.8/zato_extra_paths/
$ sudo -u zato ln -s /usr/local/lib/python2.7/dist-packages/PIL/ /opt/zato/2.0.8/zato_extra_paths/
$ sudo -u zato ln -s /usr/local/lib/python2.7/dist-packages/Pillow-5.0.0.egg-info/ /opt/zato/2.0.8/zato_extra_paths/
$ sudo -u zato ln -s /usr/local/lib/python2.7/dist-packages/reportlab/ /opt/zato/2.0.8/zato_extra_paths/
$ sudo -u zato ln -s /usr/local/lib/python2.7/dist-packages/reportlab-3.4.0.egg-info/ /opt/zato/2.0.8/zato_extra_paths/
$ sudo -u zato ln -s /usr/local/lib/python2.7/dist-packages/rsa /opt/zato/2.0.8/zato_extra_paths/
$ sudo -u zato ln -s /usr/local/lib/python2.7/dist-packages/rsa-3.4.2.dist-info/ /opt/zato/2.0.8/zato_extra_paths/
$ sudo -u zato ln -s /usr/local/lib/python2.7/dist-packages/qrcode /opt/zato/2.0.8/zato_extra_paths/
$ sudo -u zato ln -s /usr/local/lib/python2.7/dist-packages/qrcode-5.3.dist-info/ /opt/zato/2.0.8/zato_extra_paths/
$ sudo -u zato ln -s /usr/lib/python2.7/dist-packages/six-1.5.2-dist-info/ /opt/zato/2.0.8/zato_extra_paths/
$ sudo -u zato ln -s /usr/local/lib/python2.7/dist-packages/six.py /opt/zato/2.0.8/zato_extra_paths/
```

# Como testar
## Cadastra curso:
Primeiro precisamos popular o banco com os professores: Adriano Nunez e Marcele Nunez
```
SQL> insert into professor (nome) values ("Marcele Nunez");
SQL> insert into professor (nome) values ("Adriano Nunez");
```

Será cadastrado o curso "Ensino Medio" e as disciplinas de Quimica e Matematica. Não será feita o envio para o MEC:
```
$ curl http://localhost:11223/curso/cadastra -d '{"nome":"Ensino Medio","envio_mec":"False","disciplinas":[{"nome":"Quimica", "carga_horaria":60, "creditos":10, "professor":"Marcele Nunez"},{"nome":"Matematica", "carga_horaria":45, "creditos":5, "professor":"Adriano Nunez"}]}' ; echo
```

## Gera histórico:
Deve-se popular a tabela aluno com o aluno "Ronaldo Nunez", matricula 12345:
```
SQL> insert into aluno (nome,curso_id,matricula) values ("Ronaldo Nunez",(select id from curso where id=1),12345);
```

Também deve-se gerar o par de chaves de criptografia (dentro do ambiente de desenvolvimento):
```
$ python /vagrant/files/cria_par_chaves.py
```

Popular a tabela historico com algumas notas:
```
SQL> insert into historico (disciplina_id, aluno_id, nota) values ((select id from disciplina where nome = "Matematica"),(select id from aluno where nome = "Ronaldo Nunez", 10.0);
SQL> insert into historico (disciplina_id, aluno_id, nota) values ((select id from disciplina where nome = "Quimica"),(select id from aluno where nome = "Ronaldo Nunez"), 9.7);
```

Em seguida, gerar o pdf
```
$ curl -v http://localhost:11223/historico/gera --data '{"matricula": 12345}' -H "Content-Type: application/json" | base64 -d - > teste.pdf
```
