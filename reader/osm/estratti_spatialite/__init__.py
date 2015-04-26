#!/usr/bin/env python3

# Author: Daniele Forsi
# License: CC0

import ogr

class osm:
    def __init__(self, filename):
        self.osm = ogr.Open(filename)

    def load(self, boundary_name, ext_iterable):
        escaped_name = boundary_name.replace("'", "''")
        self.ext_iterable = ext_iterable
        self.ways = self.osm.ExecuteSQL("""
SELECT 'w' || l.osm_id AS id, l.name AS name FROM lines AS l WHERE highway IS NOT NULL AND name IS NOT NULL AND ST_Within(l.GEOMETRY, (SELECT GEOMETRY FROM multipolygons AS m WHERE m.admin_level == '8' AND m.boundary == 'administrative' AND name = '{escaped_name}'))
UNION
SELECT CASE WHEN l.osm_id IS NOT NULL THEN 'r' || l.osm_id ELSE 'w' || l.osm_way_id END AS id, l.name FROM multipolygons AS l WHERE name IS NOT NULL AND other_tags LIKE '%highway=>%' AND ST_Within(l.GEOMETRY, (SELECT GEOMETRY FROM multipolygons AS m WHERE m.admin_level == '8' AND m.boundary == 'administrative' AND name = '{escaped_name}'))
""".format(**{'escaped_name':escaped_name}))
        return self

    def getBoundaries(self):
        return self.osm.ExecuteSQL("SELECT m.name FROM multipolygons AS m WHERE m.name IS NOT NULL AND m.admin_level == '8' AND m.boundary == 'administrative'")

    def __iter__(self):
        for row in self.ways:
            yield {'id':row['id'], 'name':row['name'], 'cmpname':self.ext_iterable.transform_osm_name(row['name'])}


