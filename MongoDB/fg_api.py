from flask import Flask, request, redirect, url_for, render_template
from pymongo import MongoClient

app = Flask(__name__)

conn = MongoClient(    #Conectar num db seu, Fernando, pois eu não tenho certeza sobre a minha senha... haha
    # 'mongodb+srv://@cluster0.m52rote.mongodb.net/organicos',
    # username='dellamaf',
    # password='33762636'
)
conn = MongoClient('mongodb+srv://ficastro:jornaldb132@cluster0.dyf7dpm.mongodb.net/test')
db = conn['Organicos']

# Create
@app.route('/')
def home():
    return redirect(url_for('static', filename='index.html'))

@app.route('/cadastrar/', methods=['GET'])
# ?nome=tomate&preco=10
def cadastrar():
    produto = request.args.to_dict()
    print(produto)
    if not produto: #{}
        return redirect(url_for('static', filename='cadastrar.html'))
    else:
        query = db.produtos.find_one({'nome': produto['nome']})
        if query: #tomate está no banco
            return {'error': 'Produto já cadastrado!'}
        else: # tomate não está no banco
            db.produtos.insert_one(produto)
            del produto['_id']
            return produto

# # Read
# @app.route('/consultar/')
# def consultar():
#     produto = request.args.to_dict()
#     print(produto)
#     if not produto:
#         return redirect(url_for('static', filename='consultar.html'))
#     else: #{'nome': 'tomate', 'preco':10}
#         cursor = db.produtos.find({'nome': produto['nome']}, {'_id':False})
#         produtos = list(cursor)
#         return produtos

@app.route('/consultar/') #?
def consultar_nome():
    produto = request.args.to_dict()
    print(produto)
    if not produto:
        return redirect(url_for('static', filename='consultar.html'))
    else:
        produto = db.produtos.find_one({'nome': produto['nome']}, {'_id':False})
        print(produto)
        if produto: #tomate está no banco
            return produto
        else: # tomate não está no banco
            return {'error': 'Produto não encontrado!'}


# Delete
@app.route('/deletar/') #?
def deletar_nome():
    produto = request.args.to_dict()
    if not produto:
        return redirect(url_for('static', filename='deletar.html'))
    else:
        produto = db.produtos.find_one({'nome': produto['nome']}, {'_id':False})
        print(produto)
        if produto:
            db.produtos.delete_one({'nome': produto['nome']})
            return {'message': 'Produto deletado com sucesso!'}
        else:
            return {'error': 'Produto não encontrado!'}


# #Alterar
# @app.route('/alterar/<>')
# def alterar_nome(nome,chave,valor): #?
#     db.produtos.updateOne(
#     <condição>,
#     {$set:
#         {'chave':'valor'}
#     }
# )


# @app.route('/deletar/')
# def deletar():
#     db.produtos.drop()
#     return {'message': 'Banco de dados apagado!'}

if __name__ == '__main__':
    app.run(debug=True)