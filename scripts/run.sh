#!/bin/zsh

INFILE=b40.7.pdf
# Extract pages from PDF file and convert to text
pdftk b40.7.pdf cat 7-21 output - | pdftotext -layout - output.txt

# Extract columns 1, 2, 6, 7 from table and reformat to 2 columns
cat output.txt | sed -e '/^[^[:alpha:]]/d' -e '/^[[:space:]]*$/d' | awk -F' ' '{print $1, $2; print $6, $7}' | sed '/^[[:space:]]*$/d' > keywords.txt
