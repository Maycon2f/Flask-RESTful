from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usuarios
from flask_httpauth import HTTPBasicAuth


#definindo a autenticação
auth = HTTPBasicAuth()

#definindo o flask
app = Flask(__name__)
api = Api(app)

#def de verificação em hardcode
'''USUARIOS = {
    'maycon': '123',
    'lukas': '123'
}'''

'''@auth.verify_password
def verificacao(login, senha):
    print('Validando usuario')
    print(USUARIOS.get(login) == senha)

    if not (login, senha):
        return False
    
    return USUARIOS.get(login) == senha'''


#def de verificação utilizando a tabela do banco de dados Usuario
@auth.verify_password
def verificação(login, senha):
    if not (login, senha):
        return False
    return Usuarios.query.filter_by(login=login, senha=senha).first()


class Pessoa(Resource):
    @auth.login_required
    #Get para localizar uma unica pessoa
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        try:
            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }
        except AttributeError:
            response = {
                'status':'erro',
                'mensagem':'Pessoa não encontrada'
            }
        return response

    #put para alterar apenas 2 linhas sendo nome e idade
    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.json
        if 'nome' in dados:
            pessoa.nome = dados['nome']


        if 'idade' in dados:
            pessoa.idade = dados['idade']

        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }
        return response


    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        pessoa.delete()
        mensagem = f"{pessoa.nome} foi excluido com sucesso"
        return{'status':'sucesso ', 'mensagem':mensagem}

class ListaPessoas(Resource):
    @auth.login_required
    #get para localizar a lista inteira de pessoas
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id':i.id, 'nome':i.nome, 'idade':i.idade} for i in pessoas]
        return response
    #post para adicionar mais uma pessoa na lista com nome e idade
    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        response = {
            'id':pessoa.id,
            'nome':pessoa.nome,
            'idade':pessoa.idade
        }
        return response


class ListaAtividades(Resource):
    #Get para verificar todas as atividades existentes
    def get(self):
        atividades = Atividades.query.all()
        response = [{'id':i.id, 'nome':i.nome, 'pessoa':i.pessoa.nome} for i in atividades]
        return response
    #Post para atribuir uma atividade a uma pessoa
    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], pessoa=pessoa)
        atividade.save()
        response = {
            'pessoa': atividade.pessoa.nome,
            'nome': atividade.nome,
            'id': atividade.id
        }
        return response

#conexão da api com as urls
api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoas')
api.add_resource(ListaAtividades, '/atividades')


if __name__ == '__main__':
    app.run(debug=True)
