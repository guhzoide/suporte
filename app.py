import os
import threading
import pandas as pd
import pysftp as sf
import mysql.connector
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for

app = Flask(__name__)
data_hora = str((datetime.now().strftime("%Y-%m-%d_%H_%M_%S")))
data = str((datetime.now().strftime("%Y-%m-%d")))
hora = str((datetime.now().strftime("%H:%M:%S")))

# Funções
class funcoes():
    def verificaprog():
        dados = []
        loja = []
        with open('bin/listalojas', 'r') as file:
            for line in file:
                address = line.strip()
                loja.append(address)
                try:
                    try:
                        username = 'user'
                        password = 'pass'
                        hostkey_file = 'bin/known_hosts'
                        cnopts = sf.CnOpts()
                        cnopts.hostkeys.load(hostkey_file)

                        with sf.Connection(address, username=username, password=password, cnopts=cnopts) as sftp:
                            print(f"Verificando: {address}")
                            result = str((sftp.execute("sh /etc/shell/verificaprog1")))
                            chars = "''()[],"
                            result = result.translate(str.maketrans('', '', chars))
                            result = result.replace("b", "").replace("n", "")
                            dados.append(result)

                    except Exception:
                        username = 'user'
                        password = 'pass'
                        hostkey_file = 'bin/known_hosts'
                        cnopts = sf.CnOpts()
                        cnopts.hostkeys.load(hostkey_file)

                        with sf.Connection(address, username=username, password=password, cnopts=cnopts) as sftp:
                            print(f"Verificando: {address}")
                            result = str((sftp.execute("sh /etc/shell/verificaprog1")))
                            chars = "''()[],"
                            result = result.translate(str.maketrans('', '', chars))
                            result = result.replace("b", "").replace("n", "")
                            dados.append(result)
                except Exception as error:
                    error = str(error)
                    dados.append(f"Erro ao verificar {address}: {error}")
                                    
        combined_data = zip(loja, dados)
        return list(combined_data)
    
    def verificardisco():
        with open('tmp/relatorio', 'w') as file:
            file.write(f"Relatorio de uso de disco {data} {hora}\n\n--------------------------------\n")

        with open('bin/listalojas', 'r') as file:
            for line in file:
                address = line.strip()
                print(f"Gerando relatório da loja {address}")

                try:
                    username = 'user'
                    password = 'pass'
                    hostkey_file = 'bin/known_hosts'
                    cnopts = sf.CnOpts()
                    cnopts.hostkeys.load(hostkey_file)

                    with sf.Connection(address, username=username, password=password, cnopts=cnopts) as sftp:
                        size = str(sftp.execute("df -h | grep '/$' | awk '{print $2}'"))
                        used = str(sftp.execute("df -h | grep '/$' | awk '{print $3}'"))
                        avail = str(sftp.execute("df -h | grep '/$' | awk '{print $4}'"))
                        use = str(sftp.execute("df -h | grep '/$' | awk '{print $5}'"))
                        chars = "''\[]nb "
                        size_tratado = size.translate(str.maketrans('', '', chars))
                        used_tratado = used.translate(str.maketrans('', '', chars))
                        avail_tratado = avail.translate(str.maketrans('', '', chars))
                        use_tratado = use.translate(str.maketrans('', '', chars))

                        with open('tmp/relatorio', 'a') as file:
                            file.write(f"Relatorio da loja {address}\nEspaco total em disco: {size_tratado}\nEspaco utilizado: {used_tratado}\nEspaco disponivel: {avail_tratado}\nEspaco usado em %: {use_tratado}\n--------------------------------\n")
                except:
                    username = 'user'
                    password = 'pass'
                    hostkey_file = 'bin/known_hosts'
                    cnopts = sf.CnOpts()
                    cnopts.hostkeys.load(hostkey_file)

                    with sf.Connection(address, username=username, password=password, cnopts=cnopts) as sftp:
                        size = str(sftp.execute("df -h | grep '/$' | awk '{print $2}'"))
                        used = str(sftp.execute("df -h | grep '/$' | awk '{print $3}'"))
                        avail = str(sftp.execute("df -h | grep '/$' | awk '{print $4}'"))
                        use = str(sftp.execute("df -h | grep '/$' | awk '{print $5}'"))
                        chars = "''\[]nb "
                        size_tratado = size.translate(str.maketrans('', '', chars))
                        used_tratado = used.translate(str.maketrans('', '', chars))
                        avail_tratado = avail.translate(str.maketrans('', '', chars))
                        use_tratado = use.translate(str.maketrans('', '', chars))

                        with open('tmp/relatorio', 'a') as file:
                            file.write(f"Relatorio da loja {address}\nEspaco total em disco: {size_tratado}\nEspaco utilizado: {used_tratado}\nEspaco disponivel: {avail_tratado}\nEspaco usado em %: {use_tratado}\n--------------------------------\n") 
# janelas
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/consulta_cupom')
def consulta_cupom():
    dados = [(0,0,0)]
    count = 0
    return render_template('/consulta_cupom.html', dados=dados, count=count)

@app.route('/links')
def links():
    links = []
    nome_link = []
    with open('links.txt', 'r') as file:
        for line in file:
            line = line.strip()
            links.append(line)
    
    with open('nome_link.txt', 'r') as file:
        for line in file:
            line = line.strip()
            nome_link.append(line)
    combined_data = zip(links, nome_link)
    return render_template('/links.html', links=combined_data)

@app.route('/verificar_lojas')
def desativa_programas():
    return render_template('desativa_programas.html')

@app.route('/lista_loja')
def lista_loja():
    arquivo_excel = 'download/Lista_lojas.xlsx'

    dados_excel = pd.read_excel(arquivo_excel)
    dados_excel = dados_excel.dropna()

    numero_loja = dados_excel['numero_loja']
    loja = dados_excel['loja']
    regiao = dados_excel['regiao']
    localizacao = dados_excel['localizacao']
    tronco = dados_excel['tronco']

    combined_data = zip(numero_loja, loja, regiao, localizacao, tronco)

    return render_template('lista_loja.html', combined_data=combined_data, arquivo_excel=arquivo_excel)

@app.route('/verificar_disco')
def verificarDisco():
    funcoes.verificardisco()
    file = open('tmp/relatorio')
    file = file.readlines()
    return render_template('/desativa_programas.html', disco=file)

@app.route('/verificaprog')
def verificaprograma():
    combined_data = funcoes.verificaprog()
    return render_template('/desativa_programas.html', dados=combined_data)

@app.route('/tutorial')
def tutorial():
    tutorial_directory = 'tutoriais/'
    lista_arquivos = os.listdir(tutorial_directory)
    return render_template('lista_tutoriais.html', lista=lista_arquivos)

@app.route('/abrir_tutorial/<filename>')
def abrir_tutorial(filename):
    tutorial_directory = 'tutoriais/'
    caminho_arquivo = os.path.join(tutorial_directory, filename)
    return send_file(caminho_arquivo, as_attachment=False)

@app.route('/baixar_lista/<filename>')
def baixar_lista(filename):
    lista_directory = 'download'
    caminho_arquivo = os.path.join(lista_directory, filename)
    return send_file(caminho_arquivo)

@app.route('/atualiza')
def atualiza():
    dados = []  
    quantidade = 0 
    try:
        con = mysql.connector.connect(host="host", user="user", password="pass", database="database")
        cursor = con.cursor()
        cursor.execute(f"select numero_cupom, numero_loja, data_movimento from exp_imp_movimento where situacao_movimento=1;")
        dados = cursor.fetchall()
        cursor.close()
        con.close()
        quantidade = len(dados)
        if dados == []:
            dados = [(0,0,0)]
            quantidade = 0
        
        return render_template('consulta_cupom.html', dados=dados, quantidade=quantidade)
    
    except Exception as error:
        quantidade = 0
        return render_template('consulta_cupom.html', dados=dados)

@app.route('/desativa_tudo')
def desativa_tudo():
    dados = []
    def desativatudo(address):
        try:
            username = 'user'
            password = 'pass'
            hostkey_file = 'bin/known_hosts'
            cnopts = sf.CnOpts()
            cnopts.hostkeys.load(hostkey_file)

            with sf.Connection(address, username=username, password=password, cnopts=cnopts) as sftp:
                    print(f"Fazendo loja: {address}")
                    result = sftp.execute("sh /etc/shell/desativatudo && sh /etc/shell/ativtudo")
                    dados.append(result)
        except Exception:
            username = 'user'
            password = 'pass'
            hostkey_file = 'bin/known_hosts'
            cnopts = sf.CnOpts()
            cnopts.hostkeys.load(hostkey_file)

            with sf.Connection(address, username=username, password=password, cnopts=cnopts) as sftp:
                    print(f"Fazendo loja: {address}")
                    result = sftp.execute("sh /etc/shell/desativatudo && sh /etc/shell/ativtudo")
                    dados.append(result)

    def verifica_tempo_limite(address):
        tempo_limite = 15
        thread = threading.Thread(target=desativatudo, args=(address,))
        thread.start()
        thread.join(tempo_limite)
        if thread.is_alive():
            raise TimeoutError(f"Loja {address} finalizada\n")

    with open('bin/listalojas', 'r') as file:
        lojas = []
        for line in file:
            address = line.strip()
            lojas.append(address)
            try:
                verifica_tempo_limite(address)
            except TimeoutError as e:
                print(e)
    combined_data = funcoes.verificaprog()
    combined_dados = zip(lojas, dados)
    return render_template('desativa_programas.html', linhas=combined_dados, dados=combined_data)

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
