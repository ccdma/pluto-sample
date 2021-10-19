#!/usr/bin/perl

# %O: option
# %S: source file

# -halt-on-errorは引数の順番に注意
$latex     = 'platex -halt-on-error -interaction=nonstopmode %O %S';
$dvipdf    = 'dvipdfmx %O -o %D %S';
$pdf_mode  = '3'; # .tex -> .dvi -> .pdf

# viewerを起動しない
$pdf_previewer = ''