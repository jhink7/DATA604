from __future__ import print_function
import io

with io.open('../Raw Data/movies.dat', 'r', encoding='utf-8', errors='ignore') as infile, \
        io.open('outmovies.dat', 'w', encoding='ascii', errors='ignore') as outfile:
    for line in infile:
        print(*line.split(), file=outfile)