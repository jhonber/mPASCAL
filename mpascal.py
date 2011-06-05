import sys
import os.path
import mpasparse


filename = sys.argv[1]
outfile = os.path.splitext(filename)[0] + ".s"

f = open(filename)
data = f.read()
f.close()
import mpasparse

top = mpasparse.parser.parse(data)

if top:
	import mpasgen
	outf = open(outfile,"w")
	mpasgen.generate(outf,top)
	mpasgen.emit_program(outf,top)
	outf.close()
