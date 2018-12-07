"""
nome: ncbiaccess.py
funçao: acessar as informações do banco de dados NCBI e
mostrar para o usuário, assim como, encaminhar tais informações
para outros bancos importantes na área de bioinformática, como
PDB e PSPRED.
objetivos: Acessar o banco OK
           Listar os bancos OK
           Buscar termo OK
           Listar as publicações OK
           Acessar uma publicação escolhida ok - modo genbank
           Extrair os dados desta publicação e armazená-los ok
data: 18/11/2018
versao: 0.0.1 - acesso ao banco, lista dos bancos,
busca e escolha da publicação pelo termo

"""
#from Bio import PDB
# Importar as bibliotecas nescessárias
import Bio
from Bio import Entrez

# acessar o banco, informando um email


Entrez.email = "email@gmail.com"

extracao = Entrez.einfo()
extracao_lida = Entrez.read(extracao)
bancos = extracao_lida["DbList"]
#print(bancos) OK

# para cada elemento da lista de bancos,
# mostra um ID, para cada.

for b in range(1, len(bancos)+1):
    print(b, bancos[b-1])

# escolher um banco obs: fazer teste de validação
b_escolhido = int(input("Escolha um banco de dados, 0 para buscar em todos: "))


pubs_encontrados = []

bd = ''

for d in bancos:
    if d == bancos[b_escolhido - 1]:
        bd += d
        print(b_escolhido, bancos[b_escolhido-1])
        termo = input("Digite o que deseja encontrar: ")
        busca = Entrez.esearch(db=bancos[b_escolhido], term=termo)
        encontrado = Entrez.read(busca)
        print()
        #print(encontrado["IdList"])
        for id in encontrado["IdList"]:
            pubs_encontrados.append(id)

dados = []
for e in pubs_encontrados:
    handle = Entrez.efetch(db=bd, id=e, rettype="gb") # deixar uma opcao da pessoa escolher o formato
    teste = handle.read()
    dados.append(teste)
    print(teste)


# escrever em um arquivo, para entao o html ler e mostrar OK
arquivo = open('ola.txt', 'w')

for d in dados:
    arquivo.write(d)
arquivo.close()
# mostrar as possibilidades de bancos de dados a serem acessados.
print(dados)