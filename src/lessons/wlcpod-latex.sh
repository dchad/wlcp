#!/bin/sh
xsltproc wlcpod-latex.xsl $1.xml > $1.tex
pdflatex $1.tex

