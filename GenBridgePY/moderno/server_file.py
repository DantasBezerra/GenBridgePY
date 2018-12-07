import flask
from flask import jsonify
import Bio
from Bio import Entrez
from Bio.Align.Applications import ClustalwCommandline
from Bio import AlignIO
from Bio import Phylo


Entrez.email = "email@gmail.com"
extracao = Entrez.einfo()
extracao_lida = Entrez.read(extracao)
bancos = extracao_lida["DbList"]


# para cada elemento da lista de bancos,
# mostra um ID, para cada.

bcs = ""

for b in range(1, len(bancos)+1):
    print(b, bancos[b-1])
    bcs += str(b)
    bcs += " - "
    bcs += bancos[b-1]
    bcs += "  |  "

# iniciar a aplicação
app = flask.Flask("GenBridgePY")
app.config["JSON_AS_ASCII"] = False


# gerar url
@app.route("/")
def pag_inicial():
    resposta = {
        "Ansewer":
            "Pagina em branco",
        "url/OP1":
            "/ncbi/find - Para buscar publicações no NCBI",
        "url/OP2":
            "/Clustalw/align - Para realizar um alihamento pelo ClustalW"
    }
    return flask.jsonify(resposta)


# 1ª opção adicionar uma palavra em português (com teste de existência) OK
@app.route("/ncbi/find")
def ncbi_inicial():
    resposta = {
        "url/OP1": "/ncbi/find/ID-BANCO/TERMO - Para buscar publicações no NCBI, no banco e termo escolhido",
        "BANCOS":"%s" % bcs,
        " ":" "
    }
    return flask.jsonify(resposta)


@app.route("/ncbi/find/<string:banco>/<string:termo>")
def ncbi_buscar(banco, termo):

    b_escolhido = int(banco)
    pubs_encontrados = []
    bd = ''

    for d in bancos:
        if d == bancos[b_escolhido - 1]:
            bd += d
            print(b_escolhido, bancos[b_escolhido - 1])
            termo = termo
            busca = Entrez.esearch(db=bancos[b_escolhido], term=termo)
            encontrado = Entrez.read(busca)
            print('buscando termo')
            # print(encontrado["IdList"])
            for i in encontrado["IdList"]:
                pubs_encontrados.append(i)

    dados = []
    for e in pubs_encontrados:
        handle = Entrez.efetch(db=bd, id=e, rettype="fasta")  # deixar uma opcao da pessoa escolher o formato
        teste = handle.read()
        dados.append(teste)
        print(teste)

    # escrever em um arquivo, para entao o html ler e mostrar OK
    arquivo = open('ncbi-seqs.txt', 'w')

    dd = ""
    for d in dados:
        arquivo.write(d)
        dd+=d+'\n'
    arquivo.close()

    # para alinhamento
    arquivo = open("%s.fasta" % termo, 'w')
    for l in dados:
        arquivo.write(l)
    arquivo.close()

    # mostrar as possibilidades de bancos de dados a serem acessados.
    print(dados)
    resultado = dd.split('\n')

    resposta = {
        "Dados":"%s" % resultado
    }

    return flask.jsonify(resposta)

@app.route("/clustalw/align")
def clustal_iniciar():
    print()
    resposta = {
        "OP1":"URL/NOME-DO-ARQUIVO-FASTA - Para realizar o alinhamento"
    }
    return flask.jsonify(resposta)

@app.route("/clustalw/align/<string:arq>")
def clustal_alinhar(arq):
    print()
    c_line = ClustalwCommandline("clustalw2", infile="%s.fasta" % arq)
    print(c_line)

    alinhamento = AlignIO.read("%s.aln" % arq, "clustal")
    print(alinhamento)

    arvore = Phylo.read("%s.dnd" % arq, "newick")
    Phylo.draw_ascii(arvore)

    resposta = {
        "Alinhamento":"%s" % alinhamento,
        "":"",
        "Arvore":"%s" % arvore
    }
    return flask.jsonify(resposta)

# rodar a aplicaçao web
app.run("0.0.0.0", 3030)