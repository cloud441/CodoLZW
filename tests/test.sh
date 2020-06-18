#!/bin/sh

echo -e "Begin of test suite:\n\n"

diff -qs toto.lzw ../toto.lzw

echo -e "\n"

diff -qs toto_dico.csv ../toto_dico.csv

echo -e "\n"

diff -qs toto_LZWtable.csv ../toto_LZWtable.csv

echo -e "\n\nEnd of test suite.\n"
