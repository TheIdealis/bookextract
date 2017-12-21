#!/usr/bin/python2
# -*- coding: utf-8 -*-

import argparse
import subprocess

parser = argparse.ArgumentParser(description = 'Extract pages from pdf' )
parser.add_argument('-p','--pages', help='Pages to print; Format: 1-4,6,8,9  etc. default=all', default='-')
parser.add_argument('-i','--infile', required=True, help='Name of the pdf')
parser.add_argument('-o','--outfile',help='Name of the created pdf', default='book')
parser.add_argument('-b','--booklet', help='Return the Document for bookletprint', action='store_true', default=False)
parser.add_argument('-c','--cropped', help='Return the Document for cropped bookletprint', action='store_true', default=False)
args = parser.parse_args()

def encode(raw):
    keys = {'\\ ': ' '
    }
    for key in keys:
        raw = raw.replace(key,keys.get(key))
    return raw

infiles = [encode(book) for book in args.infile.split(';')]

if args.pages is '-':
    pages = ['-' for _ in range(len(infiles))]
else:
    pages = [book.split(',') for book in args.pages.split(';')]
    print(pages)
    for i, page in enumerate(pages):
        if page[0] is 'a':
            pages[i] = ['-']

form = ['','']
if args.booklet or args.cropped is True:
    form[0]=',landscape'
    form[1]=',booklet'


f = open('/home/thomas/.local/build/tex/'+args.outfile+'.tex','w')
header = '\documentclass[paper=A4 %s, pagesize]{scrartcl}' %form[0]
header +='''
\usepackage{grffile}
\usepackage{pdfpages}
\\begin{document}
'''
middle=''

for i, book in enumerate(infiles):
    for page in pages[i]:
        middle +='\includepdf[pages=%s%s]{%s}\n'%(page, form[1], book)
footer='''
\end{document}
'''
f.write(header+middle+footer)
f.close()


latex = subprocess.Popen(['pdflatex', '--output-directory=/home/thomas/.local/build/tex/',
                          '-halt-on-error',
                          '-interaction',
                          'nonstopmode',
                          '/home/thomas/.local/build/tex/'+args.outfile+'.tex'], 
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr=latex.communicate()
if latex.returncode:
    print 'Error ---------------------------------- last 700 characters of pdflatex\'s output'
    print stdout[-700:] 
else: subprocess.call(['cp', '/home/thomas/.local/build/tex/'+args.outfile+'.pdf', './'])



####Crop the file ###############################
if args.cropped is True:
    f = open('/home/thomas/.local/build/tex/'+args.outfile+'.crop'+'.tex','w')
    header ='''\documentclass[paper=24.7cm:17.5cm]{scrartcl}
\usepackage{pdfpages}
\usepackage[
    a4,         % die Papiergröße im Drucker
    cross,      % Beschnittmarken hinzufügen
    landscape,
    center,     % zentriere auf dem größeren Druckbogen
]{crop}
\\begin{document}
'''
    footer='    \includepdf[pages=-]{%s}'%(args.outfile)
    footer +='''
    \end{document}
    '''
    f.write(header+footer)
    f.close()

    latex = subprocess.Popen(['pdflatex', '--output-directory=/home/thomas/.local/build/tex/',
                              '-halt-on-error',
                              '-interaction',
                              'nonstopmode',
                              '/home/thomas/.local/build/tex/'+args.outfile+'.crop'+'.tex'], 
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr=latex.communicate()
    if latex.returncode:
        print 'Error ---------------------------------- last 700 characters of pdflatex\'s output'
        print stdout[-700:] 
    else: subprocess.call(['cp', '/home/thomas/.local/build/tex/'+args.outfile+'.crop'+'.pdf', './'])
     
