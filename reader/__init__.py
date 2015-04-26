#!/usr/bin/env python3

# Author: Daniele Forsi
# License: CC0

def import_module(type, name):
    if type == 'stradario':
        from . import stradario
        return stradario.import_module(name)
    elif type == 'osm':
        from . import osm
        return osm.import_module(name)
    else:
        raise Exception('Unknown type "%s"' % (type, ))
