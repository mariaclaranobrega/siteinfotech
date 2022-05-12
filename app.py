from flask import Flask,render_template,url_for,redirect,request
import sqlite3

app = Flask(__name__)

#Todas as bases de dados foram criadas diretamente no DB Browser

#Referenciar 'fornecedores.db' no arquivo
db_fornecedores = 'database/fornecedores.db'
#Referenciar 'administracao.db' no arquivo
db_administracao = 'database/administracao.db'
#Referenciar 'administracao.db' no arquivo
db_clientes = 'database/clientes.db'
#Referenciar 'produtos.db' no arquivo
db_produtos = 'database/produtos.db'




# Criar uma conexão com 'fornecedores.db' e passar as interações como parâmetros
def interagir_db_fornecedores(query, parametros=()):
    with sqlite3.connect(db_fornecedores) as con:
        cursor = con.cursor()
        interacao = cursor.execute(query, parametros)
        con.commit()
    return interacao


#Criar uma conexão com 'administracao.db' e passar as interações como parâmetros
def interagir_db_administracao(query,parametros=()):
    with sqlite3.connect(db_administracao) as con:
        cursor = con.cursor()
        interacao = cursor.execute(query,parametros)
        con.commit()
    return interacao

#Criar uma conexão com 'clientes.db' e passar as interações como parâmetros
def interagir_db_clientes(query,parametros=()):
    with sqlite3.connect(db_clientes) as con:
        cursor = con.cursor()
        interacao = cursor.execute(query,parametros)
        con.commit()
    return interacao

#Criar uma conexão com 'produtos.db' e passar as interações como parâmetros
def interagir_db_produtos(query,parametros=()):
    with sqlite3.connect(db_produtos) as con:
        cursor = con.cursor()
        interacao = cursor.execute(query,parametros)
        con.commit()
    return interacao



#Renderizar página inicial
@app.route('/',methods=['GET','POST'])
def inicial():
    if request.method=='GET':
        return render_template("inicial.html")


#Renderizar página de clientes
@app.route('/clientes')
def clientes():
    return render_template("clientes.html")

#Renderizar página da admnistração
@app.route('/att-adm')
def refresh():
    return render_template("adm.html")


#Redirecionar para a página de fornecedores
@app.route('/fornecedores/<fornecedor_login><fornecedor_senha>', methods=['GET','POST'])
def fornecedores(fornecedor_login,fornecedor_senha):
        if request.method == 'POST':
            #Trazer dados de login dos fornecedores diretamente do banco de dados
            query = 'SELECT usuariofornecedor,senhafornecedor FROM fornecedor'
            consulta_f = interagir_db_fornecedores(query)
            database_f = consulta_f.fetchall()
            #Receber inputs de login e senha dados na página
            fornecedor_login=request.form['InputEmail1']
            fornecedor_senha=request.form['InputPassword1']
            #Percorrer a base de dados
            for i in database_f:
                #Se os inputs de email e senha estiverem no banco de dados
                if i.count(fornecedor_login) == 1 and i.count(fornecedor_senha) == 1:
                    #Renderizar página dos Fornecedores
                    return render_template("fornecedores.html",fornecedor_login=fornecedor_login,fornecedor_senha=fornecedor_senha)
                else:
                    pass
            #Caso não haja no banco de dados, o acesso é negado
            return "Página restrita a Fornecedores - Login ou senha incorretos"



#Redirecionar para a página da Administração
@app.route('/adm/<adm_login><adm_senha>', methods=['GET','POST'])
def administracao(adm_login,adm_senha):
        if request.method == 'POST':
            # Trazer dados de login da administração diretamente do banco de dados
            query = 'SELECT usuarioadm,senhaadm FROM administracao'
            consulta_adm = interagir_db_administracao(query)
            database_adm = consulta_adm.fetchall()
            # Receber inputs de login e senha dados na página
            adm_login = request.form['InputEmail2']
            adm_senha = request.form['InputPassword2']
            # Percorrer a base de dados
            for i in database_adm:
                # Se os inputs de email e senha estiverem no banco de dados
                if i.count(adm_login) == 1 and i.count(adm_senha) == 1:
                    # Renderizar página da Administração
                    return render_template("adm.html",adm_login=adm_login,adm_senha=adm_senha)
                else:
                    pass
            #Caso não haja no banco de dados, o acesso é negado
            return "Página restrita a Administração - Login ou senha incorretos"



#Renderizar página de Login de Clientes
@app.route('/login-clientes')
def login():
    return render_template("login-cliente.html")

#Confirmar login
@app.route('/entrar/<cliente_login><cliente_senha>', methods=['GET','POST'])
def entrar(cliente_login,cliente_senha):
    if request.method == 'POST':
        # Trazer todos os dados dos clientes diretamente do banco de dados
        query = 'SELECT * FROM cliente'
        consulta_cliente = interagir_db_clientes(query)
        database_cliente = consulta_cliente.fetchall()
        # Receber inputs de login e senha dados na página
        cliente_login = request.form['InputEmail3']
        cliente_senha = request.form['InputPassword3']
        # Percorrer a base de dados
        for i in database_cliente:
            # Se os inputs de email e senha estiverem no banco de dados
            if i[5] == cliente_login and i[6] == cliente_senha:
                # Renderizar página de Compras
                return render_template("compras.html",cliente_login=cliente_login,cliente_senha=cliente_senha)
            else:
                pass
        # Caso não haja no banco de dados, o acesso é negado
        return "Página restrita a Clientes - Faça seu Login ou Registre-se"


#Renderizar página de Registro de Clientes
@app.route('/registre-se')
def registre_se():
    return render_template("registro-cliente.html")

#Registrar cliente no banco de dados
@app.route('/registrar', methods=['GET','POST'])
def registrar():
    if request.method == 'POST':
        # Receber inputs da página
        nome_cliente = request.form['InputNameClient']
        nif_cliente = request.form['InputNIFClient']
        telefone_cliente = request.form['InputTlmClient']
        morada_cliente = request.form['InputAddressClient']
        email_cliente = request.form['InputEmail4']
        senha_cliente = request.form['InputPassword4']
        #Passar a instrução de introduzir na tabela
        query = 'INSERT INTO cliente VALUES(NULL,?,?,?,?,?,?)'
        #Passar os inputs como parâmetros do que deve ser introduzido
        parametros = (nome_cliente,nif_cliente,telefone_cliente,morada_cliente,email_cliente,senha_cliente)
        #Chamar o método de interação com a base de dados 'clientes.db'
        consulta_cliente = interagir_db_clientes(query,parametros)
        #Redirecionar para o cliente fazer login, uma vez que está cadastrado
        return render_template("login-cliente.html")


#Criar interações entre as compras e o banco de dados
#Cada artigo tem sua rota, que irá individualmente interagir com o banco de dados, quando chamado na página
#A explicação da rota/método estará no primeiro artigo e o restante segue a mesma lógica

#Ao clicar em comprar o RATO01
@app.route('/comprar-RATO01',methods=['GET','POST'])
def comprar_RATO01():
    if request.method == 'POST':
        # Trazer todos os dados dos produtos diretamente do banco de dados
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        #Percorrer a base de dados
        for i in db_produtos:
            #Quando neste artigo:
            if "RATO01" in i:
                #Retirar 1 artigo do stock
                update_quantidadestock=i[5]-1
                #Adicionar 1 venda
                update_vendascliente=i[7]+1
                query = '''UPDATE produto SET quantidadestock=?,vendascliente=? WHERE codigoproduto="RATO01"'''
                parametros = (update_quantidadestock,update_vendascliente)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    #Voltar a renderizar a mesma página
    return render_template('compras.html')

#Segue a lógica do '/comprar-RATO01'
@app.route('/comprar-NOTEBOOK01',methods=['GET','POST'])
def comprar_NOTEBOOK01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        for i in db_produtos:
            if "NOTEBOOK01" in i:
                update_quantidadestock=i[5]-1
                update_vendascliente=i[7]+1
                query = '''UPDATE produto SET quantidadestock=?,vendascliente=? WHERE codigoproduto="NOTEBOOK01"'''
                parametros = (update_quantidadestock,update_vendascliente)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return render_template('compras.html')

#Segue a lógica do '/comprar-RATO01'
@app.route('/comprar-ROUTER01',methods=['GET','POST'])
def comprar_ROUTER01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        for i in db_produtos:
            if "ROUTER01" in i:
                update_quantidadestock=i[5]-1
                update_vendascliente=i[7]+1
                query = '''UPDATE produto SET quantidadestock=?,vendascliente=? WHERE codigoproduto="ROUTER01"'''
                parametros = (update_quantidadestock,update_vendascliente)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return render_template('compras.html')

#Segue a lógica do '/comprar-RATO01'
@app.route('/comprar-MONITOR01',methods=['GET','POST'])
def comprar_MONITOR01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        for i in db_produtos:
            if "MONITOR01" in i:
                update_quantidadestock=i[5]-1
                update_vendascliente=i[7]+1
                query = '''UPDATE produto SET quantidadestock=?,vendascliente=? WHERE codigoproduto="MONITOR01"'''
                parametros = (update_quantidadestock,update_vendascliente)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return render_template('compras.html')

#Segue a lógica do '/comprar-RATO01'
@app.route('/comprar-PROCESSADOR01',methods=['GET','POST'])
def comprar_PROCESSADOR01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        for i in db_produtos:
            if "PROCESSADOR01" in i:
                update_quantidadestock=i[5]-1
                update_vendascliente=i[7]+1
                query = '''UPDATE produto SET quantidadestock=?,vendascliente=? WHERE codigoproduto="PROCESSADOR01"'''
                parametros = (update_quantidadestock,update_vendascliente)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return render_template('compras.html')

#Segue a lógica do '/comprar-RATO01'
@app.route('/comprar-DOCA01',methods=['GET','POST'])
def comprar_DOCA01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        for i in db_produtos:
            if "DOCA01" in i:
                update_quantidadestock=i[5]-1
                update_vendascliente=i[7]+1
                query = '''UPDATE produto SET quantidadestock=?,vendascliente=? WHERE codigoproduto="DOCA01"'''
                parametros = (update_quantidadestock,update_vendascliente)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return render_template('compras.html')

#Segue a lógica do '/comprar-RATO01'
@app.route('/comprar-CARREGADOR01',methods=['GET','POST'])
def comprar_CARREGADOR01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        for i in db_produtos:
            if "CARREGADOR01" in i:
                update_quantidadestock=i[5]-1
                update_vendascliente=i[7]+1
                query = '''UPDATE produto SET quantidadestock=?,vendascliente=? WHERE codigoproduto="CARREGADOR01"'''
                parametros = (update_quantidadestock,update_vendascliente)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return render_template('compras.html')

#Segue a lógica do '/comprar-RATO01'
@app.route('/comprar-IPHONE01',methods=['GET','POST'])
def comprar_IPHONE01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        for i in db_produtos:
            if "IPHONE01" in i:
                update_quantidadestock=i[5]-1
                update_vendascliente=i[7]+1
                query = '''UPDATE produto SET quantidadestock=?,vendascliente=? WHERE codigoproduto="IPHONE01"'''
                parametros = (update_quantidadestock,update_vendascliente)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return render_template('compras.html')

#Segue a lógica do '/comprar-RATO01'
@app.route('/comprar-HEADSET01',methods=['GET','POST'])
def comprar_HEADSET01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        for i in db_produtos:
            if "HEADSET01" in i:
                update_quantidadestock=i[5]-1
                update_vendascliente=i[7]+1
                query = '''UPDATE produto SET quantidadestock=?,vendascliente=? WHERE codigoproduto="HEADSET01"'''
                parametros = (update_quantidadestock,update_vendascliente)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return render_template('compras.html')



#Solicitar reposição ao fornecedor
#Cada artigo tem sua rota, que irá individualmente interagir com o banco de dados, quando chamado na página
#A explicação da rota/método estará no primeiro artigo e o restante segue a mesma lógica

#Quando (na página da Administração), o solicitar reposição do RATO01:
@app.route('/solicitar-RATO01',methods=['GET','POST'])
def solicitar_RATO01():
    if request.method == 'POST':
        # Trazer todos os dados dos produtos diretamente do banco de dados
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        #Trazer input de quantidade dado pelo usuário (adm)
        quantidade = int(request.form['quantidade_RATO01'])
        #Percorrer banco de dados
        for i in db_produtos:
            #Quando neste artigo:
            if "RATO01" in i:
                #Adicionar esta informação a coluna de quantidade a ser solicitada ao fornecedor
                update_quantidarepor=(i[8])+quantidade
                query = '''UPDATE produto SET quantidaderepor=? WHERE codigoproduto="RATO01"'''
                parametros = (update_quantidarepor,)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    #Renderizar página administração
    return redirect(url_for('refresh'))

#Segue a lógica do '/solicitar-RATO01'
@app.route('/solicitar-NOTEBOOK01',methods=['GET','POST'])
def solicitar_NOTEBOOK01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        quantidade = int(request.form['quantidade_NOTEBOOK01'])
        for i in db_produtos:
            if "NOTEBOOK01" in i:
                update_quantidarepor=(i[8])+quantidade
                query = '''UPDATE produto SET quantidaderepor=? WHERE codigoproduto="NOTEBOOK01"'''
                parametros = (update_quantidarepor,)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return redirect(url_for('refresh'))

#Segue a lógica do '/solicitar-RATO01'
@app.route('/solicitar-ROUTER01',methods=['GET','POST'])
def solicitar_ROUTER01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        quantidade = int(request.form['quantidade_ROUTER01'])
        for i in db_produtos:
            if "ROUTER01" in i:
                update_quantidarepor=(i[8])+quantidade
                query = '''UPDATE produto SET quantidaderepor=? WHERE codigoproduto="ROUTER01"'''
                parametros = (update_quantidarepor,)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return redirect(url_for('refresh'))

#Segue a lógica do '/solicitar-RATO01'
@app.route('/solicitar-MONITOR01',methods=['GET','POST'])
def solicitar_MONITOR01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        quantidade = int(request.form['quantidade_MONITOR01'])
        for i in db_produtos:
            if "MONITOR01" in i:
                update_quantidarepor=(i[8])+quantidade
                query = '''UPDATE produto SET quantidaderepor=? WHERE codigoproduto="MONITOR01"'''
                parametros = (update_quantidarepor,)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return redirect(url_for('refresh'))

#Segue a lógica do '/solicitar-RATO01'
@app.route('/solicitar-PROCESSADOR01',methods=['GET','POST'])
def solicitar_PROCESSADOR01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        quantidade = int(request.form['quantidade_PROCESSADOR01'])
        for i in db_produtos:
            if "PROCESSADOR01" in i:
                update_quantidarepor=(i[8])+quantidade
                query = '''UPDATE produto SET quantidaderepor=? WHERE codigoproduto="PROCESSADOR01"'''
                parametros = (update_quantidarepor,)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return redirect(url_for('refresh'))

#Segue a lógica do '/solicitar-RATO01'
@app.route('/solicitar-DOCA01',methods=['GET','POST'])
def solicitar_DOCA01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        quantidade = int(request.form['quantidade_DOCA01'])
        for i in db_produtos:
            if "DOCA01" in i:
                update_quantidarepor=(i[8])+quantidade
                query = '''UPDATE produto SET quantidaderepor=? WHERE codigoproduto="DOCA01"'''
                parametros = (update_quantidarepor,)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return redirect(url_for('refresh'))

#Segue a lógica do '/solicitar-RATO01'
@app.route('/solicitar-CARREGADOR01',methods=['GET','POST'])
def solicitar_CARREGADOR01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        quantidade = int(request.form['quantidade_CARREGADOR01'])
        for i in db_produtos:
            if "CARREGADOR01" in i:
                update_quantidarepor=(i[8])+quantidade
                query = '''UPDATE produto SET quantidaderepor=? WHERE codigoproduto="CARREGADOR01"'''
                parametros = (update_quantidarepor,)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return redirect(url_for('refresh'))

#Segue a lógica do '/solicitar-RATO01'
@app.route('/solicitar-IPHONE01',methods=['GET','POST'])
def solicitar_IPHONE01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        quantidade = int(request.form['quantidade_IPHONE01'])
        for i in db_produtos:
            if "IPHONE01" in i:
                update_quantidarepor=(i[8])+quantidade
                query = '''UPDATE produto SET quantidaderepor=? WHERE codigoproduto="IPHONE01"'''
                parametros = (update_quantidarepor,)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return redirect(url_for('refresh'))

#Segue a lógica do '/solicitar-RATO01'
@app.route('/solicitar-HEADSET01',methods=['GET','POST'])
def solicitar_HEADSET01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        quantidade = int(request.form['quantidade_HEADSET01'])
        for i in db_produtos:
            if "HEADSET01" in i:
                update_quantidarepor=(i[8])+quantidade
                query = '''UPDATE produto SET quantidaderepor=? WHERE codigoproduto="HEADSET01"'''
                parametros = (update_quantidarepor,)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return redirect(url_for('refresh'))


#Fornecer reposição ao administrador
#Cada artigo tem sua rota, que irá individualmente interagir com o banco de dados, quando chamado na página
#A explicação da rota/método estará no primeiro artigo e o restante segue a mesma lógica

#Quando o fornecedor clicar em fornecer o artigo RATO01:
@app.route('/fornecer-RATO01',methods=['GET','POST'])
def fornecer_RATO01():
    if request.method == 'POST':
        # Trazer todos os dados dos produtos diretamente do banco de dados
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        #Percorrer a base de dados
        for i in db_produtos:
            #Quando neste produto:
            if "RATO01" in i:
                #Zerar a necessidade de reposição, uma vez que o fornecimento está a ser realizado
                repor = 0
                #Incluir ao stock a quantidade que foi solicitada pelo administrador
                stock = i[5] + i[8]
                #Adicionar esta quantidade as compras que o administrador faz ao fornecedor deste produto
                comprasfornecedor = i[6] + i[8]
                query = '''UPDATE produto SET quantidadestock=?,quantidaderepor=?,comprasfornecedor=? WHERE codigoproduto="RATO01"'''
                parametros = (stock,repor,comprasfornecedor)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    #Renderizar página de confirmação de reposição
    return render_template("reposicaofeita.html")

#Segue a lógica do '/fornecer-RATO01'
@app.route('/fornecer-NOTEBOOK01',methods=['GET','POST'])
def fornecer_NOTEBOOK01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        for i in db_produtos:
            if "NOTEBOOK01" in i:
                repor = 0
                stock = i[5] + i[8]
                comprasfornecedor = i[6] + i[8]
                query = '''UPDATE produto SET quantidadestock=?,quantidaderepor=?,comprasfornecedor=? WHERE codigoproduto="NOTEBOOK01"'''
                parametros = (stock,repor,comprasfornecedor)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return render_template("reposicaofeita.html")

#Segue a lógica do '/fornecer-RATO01'
@app.route('/fornecer-ROUTER01',methods=['GET','POST'])
def fornecer_ROUTER01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        for i in db_produtos:
            if "ROUTER01" in i:
                repor = 0
                stock = i[5] + i[8]
                comprasfornecedor = i[6] + i[8]
                query = '''UPDATE produto SET quantidadestock=?,quantidaderepor=?,comprasfornecedor=? WHERE codigoproduto="ROUTER01"'''
                parametros = (stock,repor,comprasfornecedor)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return render_template("reposicaofeita.html")

#Segue a lógica do '/fornecer-RATO01'
@app.route('/fornecer-MONITOR01',methods=['GET','POST'])
def fornecer_MONITOR01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        for i in db_produtos:
            if "MONITOR01" in i:
                repor = 0
                stock = i[5] + i[8]
                comprasfornecedor = i[6] + i[8]
                query = '''UPDATE produto SET quantidadestock=?,quantidaderepor=?,comprasfornecedor=? WHERE codigoproduto="MONITOR01"'''
                parametros = (stock,repor,comprasfornecedor)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return render_template("reposicaofeita.html")

#Segue a lógica do '/fornecer-RATO01'
@app.route('/fornecer-PROCESSADOR01',methods=['GET','POST'])
def fornecer_PROCESSADOR01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        for i in db_produtos:
            if "PROCESSADOR01" in i:
                repor = 0
                stock = i[5] + i[8]
                comprasfornecedor = i[6] + i[8]
                query = '''UPDATE produto SET quantidadestock=?,quantidaderepor=?,comprasfornecedor=? WHERE codigoproduto="PROCESSADOR01"'''
                parametros = (stock,repor,comprasfornecedor)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return render_template("reposicaofeita.html")

#Segue a lógica do '/fornecer-RATO01'
@app.route('/fornecer-DOCA01',methods=['GET','POST'])
def fornecer_DOCA01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        for i in db_produtos:
            if "DOCA01" in i:
                repor = 0
                stock = i[5] + i[8]
                comprasfornecedor = i[6] + i[8]
                query = '''UPDATE produto SET quantidadestock=?,quantidaderepor=?,comprasfornecedor=? WHERE codigoproduto="DOCA01"'''
                parametros = (stock,repor,comprasfornecedor)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return render_template("reposicaofeita.html")

#Segue a lógica do '/fornecer-RATO01'
@app.route('/fornecer-CARREGADOR01',methods=['GET','POST'])
def fornecer_CARREGADOR01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        for i in db_produtos:
            if "CARREGADOR01" in i:
                repor = 0
                stock = i[5] + i[8]
                comprasfornecedor = i[6] + i[8]
                query = '''UPDATE produto SET quantidadestock=?,quantidaderepor=?,comprasfornecedor=? WHERE codigoproduto="CARREGADOR01"'''
                parametros = (stock,repor,comprasfornecedor)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return render_template("reposicaofeita.html")

#Segue a lógica do '/fornecer-RATO01'
@app.route('/fornecer-IPHONE01',methods=['GET','POST'])
def fornecer_IPHONE01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        for i in db_produtos:
            if "IPHONE01" in i:
                repor = 0
                stock = i[5] + i[8]
                comprasfornecedor = i[6] + i[8]
                query = '''UPDATE produto SET quantidadestock=?,quantidaderepor=?,comprasfornecedor=? WHERE codigoproduto="IPHONE01"'''
                parametros = (stock,repor,comprasfornecedor)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return render_template("reposicaofeita.html")

#Segue a lógica do '/fornecer-RATO01'
@app.route('/fornecer-HEADSET01',methods=['GET','POST'])
def fornecer_HEADSET01():
    if request.method == 'POST':
        query = 'SELECT * FROM produto'
        consulta_produtos = interagir_db_produtos(query)
        db_produtos = consulta_produtos.fetchall()
        for i in db_produtos:
            if "HEADSET01" in i:
                repor = 0
                stock = i[5] + i[8]
                comprasfornecedor = i[6] + i[8]
                query = '''UPDATE produto SET quantidadestock=?,quantidaderepor=?,comprasfornecedor=? WHERE codigoproduto="HEADSET01"'''
                parametros = (stock,repor,comprasfornecedor)
                consulta = interagir_db_produtos(query,parametros)
            else:
                pass
    return render_template("reposicaofeita.html")


#Página de gestão de produtos - Administração
@app.route('/tabela-adm',methods=['GET','POST'])
def tabela_adm():
    #Para garantir que o banco de dados será atualizado, será aberta uma conexão sempre que a página for chamada
    with sqlite3.connect(db_produtos) as con:
        cursor = con.cursor()
        #Trazer os dados do banco de dados 'produtos.db' (tabela:produto)
        interacao = cursor.execute('SELECT * from produto').fetchall()
        con.commit()
        #Criar uma lista, que armazenará estes dados
        tabelaadm=[]
        #Percorrer banco de dados
        for i in interacao:
            #E armazenar a informação em na lista
            tabelaadm.append(i)
    #Renderizar página de Gestão de Produtos - Administração
    return render_template("adm-tabela.html",tabelaadm=tabelaadm)

#Página de gestão de produtos - Fornecedores
#Cada fornecedor terá uma página específica
#Fornecedor 01
@app.route('/tabela-fornecedor1',methods=['GET','POST'])
def tabela_fornecedor1():
    with sqlite3.connect(db_produtos) as con:
        cursor = con.cursor()
        interacao = cursor.execute('SELECT * from produto').fetchall()
        con.commit()
        tabelafornecedor=[]
        for i in interacao:
            tabelafornecedor.append(i)
    # Renderizar página do fornecedor 01
    return render_template("fornecedor-tabela1.html",tabelafornecedor=tabelafornecedor)
#Fornecedor 02
@app.route('/tabela-fornecedor2',methods=['GET','POST'])
def tabela_fornecedor2():
    with sqlite3.connect(db_produtos) as con:
        cursor = con.cursor()
        interacao = cursor.execute('SELECT * from produto').fetchall()
        con.commit()
        tabelafornecedor=[]
        for i in interacao:
            tabelafornecedor.append(i)
    # Renderizar página do fornecedor 01
    return render_template("fornecedor-tabela2.html",tabelafornecedor=tabelafornecedor)

#Página que mostra aos clientes quais são os artigos mais vendidos
@app.route('/tabela-clientes',methods=['GET','POST'])
def tabela_clientes():
    with sqlite3.connect(db_produtos) as con:
        cursor = con.cursor()
        interacao = cursor.execute('SELECT * from produto ORDER BY vendascliente DESC').fetchall()
        con.commit()
        tabelaclientes=[]
        for i in interacao:
            tabelaclientes.append(i)
    #Renderiza página de ranking de vendas - Clientes
    return render_template("clientes-tabela.html",tabelaclientes=tabelaclientes)



if __name__ == "__main__":
    app.run(debug=True)


