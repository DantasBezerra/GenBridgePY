import flask
from flask import jsonify
import Bio
from Bio import Entrez
from Bio.Align.Applications import ClustalwCommandline
from Bio import AlignIO
from Bio import Phylo

arq = "chloroplast"


c_line = ClustalwCommandline("clustalw2", infile="%s.fasta" % arq)
print(c_line)


clustalw_exe =  "C: \ Arquivos de programas \ new clustal \ clustalw2.exe"
lustalw_cline = ClustalwCommandline (clustalw_exe, infile = "arq.fasta")
alinhamento = AlignIO.read("%s.aln" % arq, "clustal")
print(alinhamento)

arvore = Phylo.read("%s.dnd" % arq, "newick")
Phylo.draw_ascii(arvore)


