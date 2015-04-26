#!/usr/bin/env python3

# Author: Daniele Forsi
# License: CC0

# Data
# Source: http://opendata.comune.re.it/?dataset=civici-del-comune-di-reggio-emilia
# License: CC-BY
# Format: csv

from ... import stradario
import csv

class Reggio_nell_Emilia(stradario.Stradario, csv.DictReader):
    def __init__(self, datadir=""):
        filename = datadir + "Reggio_nell_Emilia/stradario.csv"
        csvfile = open(filename)
        temp = csvfile.read(1024)
        csvfile.seek(0)
        dialect = csv.Sniffer().sniff(temp)
        csv.DictReader.__init__(self, csvfile, dialect=dialect)

    def __next__(self):
        row = super().__next__()
        return {'id':row['ID_VIA'], 'name':row['TOPONIMO'], 'cmpname':self.transform_ext_name(row['TOPONIMO'])}
