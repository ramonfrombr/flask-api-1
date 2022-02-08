from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os


app = Flask(__name__)

diretoriobase = os.path.abspath(os.path.dirname(__file__))

# Banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(diretoriobase, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa banco de dados
db = SQLAlchemy(app)

# Inicializa serializador
ma = Marshmallow(app)


class Produto(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.String(200))
    preco = db.Column(db.Float)
    quantidade = db.Column(db.Integer)

    def __init__(self, nome, descricao, preco, quantidade):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.quantidade = quantidade

# Schema do Produto
class ProdutoSchema(ma.Schema):

    class Meta:

        fields = ('id', 'nome', 'descricao', 'preco', 'quantidade')

# Inicializa os schemas
produto_schema = ProdutoSchema()
produtos_schema = ProdutoSchema(many=True)




# Rota da API


@app.route('/produtos', methods=['GET'])
def produtos():

    produtos = Produto.query.all()

    return produtos_schema.jsonify(produtos)


@app.route('/produtos/<int:id>')
def produto(id):

    produto = Produto.query.get(id)

    return produto_schema.jsonify(produto)



@app.route('/produtos', methods=['POST'])
def adicionar_produto():

    produto = Produto(**request.json)

    db.session.add(produto)

    db.session.commit()

    return produto_schema.jsonify(produto)


@app.route('/produtos/<int:id>', methods=['PUT'])
def editar_produto(id):

    produto = Produto.query.get(id)

    produto.nome = request.json['nome']
    produto.descricao = request.json['descricao']
    produto.preco = request.json['preco']
    produto.quantidade = request.json['quantidade']

    db.session.add(produto)

    db.session.commit()

    return produto_schema.jsonify(produto)


@app.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):

    produto = Produto.query.get(id)

    db.session.delete(produto)

    db.session.commit()

    return produto_schema.jsonify(produto)




# Ativa o servidor
if __name__ == '__main__':
    app.run(debug=True)


