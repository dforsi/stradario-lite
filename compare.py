#!/usr/bin/env python3

# Confronta i nomi delle strade in OpenStreetMap con gli stradari comunali

# Author: Daniele Forsi
# License: CC0

import argparse
import sqlite3
import csv

import reader

parser = argparse.ArgumentParser(description='Compare OpenStreetMap names with other sources.')
parser.add_argument('dbname', metavar='DBNAME', nargs='+',
                    help='Spatialite database with OpenStreetMap data')
parser.add_argument('--data-prefix', metavar='PREFIX', default='',
                    help='Base directory for data files')

args = parser.parse_args()

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

osm_reader = reader.import_module('osm', 'estratti_spatialite')
for filename in args.dbname:
    osm = osm_reader(filename)
    boundaries = osm.getBoundaries()
    for boundary in boundaries:
        boundary_name = boundary.GetFieldAsString('name')

        # Import from external source
        ext_reader = reader.import_module('stradario', boundary_name)
        ext_iterable = ext_reader(args.data_prefix)
        cursor.execute("DROP TABLE IF EXISTS ext")
        cursor.execute("CREATE TEMPORARY TABLE ext (id STRING PRIMARY KEY, name STRING, cmpname STRING)")
        cursor.executemany("INSERT INTO ext (id, name, cmpname) VALUES (:id, :name, :cmpname)", ext_iterable)
        cursor.execute("CREATE INDEX idx_ext_name ON ext (cmpname)")

        # Import from OpenStreetMap
        osm_iterable = osm.load(boundary_name, ext_iterable)
        cursor.execute("DROP TABLE IF EXISTS osm")
        cursor.execute("CREATE TEMPORARY TABLE osm (id STRING PRIMARY KEY, name STRING, cmpname STRING)")
        cursor.executemany("INSERT INTO osm (id, name, cmpname) VALUES (:id, :name, :cmpname)", osm_iterable)
        cursor.execute("CREATE INDEX idx_osm_name ON osm (cmpname)")

        # Extract data
        # Can't GROUP BY in the inner queries else all NULLs are grouped!
        # Use UNION because RIGHT and OUTER JOIN aren't supported by Sqlite3
        cursor.execute("""
WITH osm2 AS (SELECT group_concat(osm.id) AS ids, name, cmpname FROM osm GROUP BY name)
SELECT * FROM (
SELECT ext.id, ext.name, osm2.ids AS osm_ids, osm2.name AS osm_name FROM ext LEFT JOIN osm2 ON ext.cmpname=osm2.cmpname
UNION
SELECT ext.id, ext.name, osm2.ids AS osm_ids, osm2.name AS osm_name FROM osm2 LEFT JOIN ext ON ext.cmpname=osm2.cmpname
ORDER BY osm2.ids
) ORDER BY Coalesce(name, osm_name) COLLATE NOCASE
""")

        # Export data
        with open(boundary_name + ".tsv", "w", newline="") as csvfile:
            field_names = [i[0] for i in cursor.description]
            csvfile.write("\t".join(field_names))
            csvfile.write("\n")
            csvwriter = csv.writer(csvfile, delimiter="\t", quotechar="\"")
            csvwriter.writerows(cursor)

cursor.close()
conn.close()
