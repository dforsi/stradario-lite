#!/usr/bin/env python3

# Author: Daniele Forsi
# License: CC0

# Data
# Source: http://opendata.comune.siena.it/?q=metarepo/datasetinfo&id=Toponimo_Stradale
# License: Italian Open Data Licence v2
# Shapefile: http://sienaopen.ldpgis.it/metarepo/download.php?id=43&type=1&format=shp

from ... import stradario
import shapefile

class Siena(stradario.Stradario, shapefile.Reader):
    def __init__(self, datadir=""):
        filename = datadir + "Siena/toponimo_stradale.dbf"
        dbf = open(filename, "rb")
        shapefile.Reader.__init__(self, dbf=dbf)

    def __iter__(self):
        for row in self.iterRecords():
            yield {'id':row[0], 'name':row[1], 'cmpname':self.transform_ext_name(row[1])}
