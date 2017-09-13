from peewee import *

mysql_db = MySQLDatabase('controle_academico', user='root', password='zato')

class BaseModel(Model):
	class Meta:
		database = mysql_db

class Curso(BaseModel):
	nome = CharField()
	envio_mec = BooleanField()

class Professor(BaseModel):
	nome = CharField()

class Disciplina(BaseModel):
	nome = CharField()
	carga_horaria = IntegerField()
	creditos = IntegerField()
	professor = ForeignKeyField(Professor)
	curso = ForeignKeyField(Curso)

class Aluno(BaseModel):
	nome = CharField()
	curso = ForeignKeyField(Curso)
	matricula = IntegerField()

class Historico(BaseModel):
	disciplina = ForeignKeyField(Disciplina)
	aluno = ForeignKeyField(Aluno)
	nota = FloatField()

if __name__ == '__main__':
	try:
		Historico.create_table()
		Aluno.create_table()
		Curso.create_table()
		Disciplina.create_table()
	except:
		pass