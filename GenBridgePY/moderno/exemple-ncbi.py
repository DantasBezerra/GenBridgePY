import Bio
import flask
from Bio import Entrez
Entrez.email = "A.N.Other@example.com" # Always tell NCBI who you are
handle = Entrez.efetch(db="nucleotide", id="186972394", rettype="gb")
teste = handle.read()
print(teste)
# exemplo de busca