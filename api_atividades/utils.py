from models import Pessoas, Usuarios, db_session

#insere dados na tabela pessoas
def insere_pessoas():
    pessoa = Pessoas(nome='arruda', idade=22)
    print(pessoa)
    pessoa.save()

#Realiza consulta na tabela pessoa
def consulta():
    pessoa = Pessoas.query.all()
    print(pessoa)
    #pessoa = Pessoas.query.filter_by(nome='Arruda').first()
    #print(pessoa.nome)

#Altera dados na tabela pessoa
def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='arruda').first()
    pessoa.idade = 23
    pessoa.save()

#Exclui dados na tabela pessoas
def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Arruda').first()
    pessoa.delete()


def insere_usuario(login, senha):
    usuario = Usuarios(login=login, senha=senha)
    usuario.save()


def consulta_todos_usuarios():
    usuarios = Usuarios.query.all()
    print(usuarios)





#teste das def criadas acima
if __name__ == '__main__':
    #insere_usuario('robertinho', '123')
    #insere_usuario('arruda', '123')
    #consulta_todos_usuarios()
    #insere_pessoas()
    #consulta()
    #exclui_pessoa()
    #altera_pessoa()