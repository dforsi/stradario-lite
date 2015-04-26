#!/usr/bin/env python3

# Author: Daniele Forsi
# License: CC0

import importlib

def import_module(name):
    module = importlib.import_module("reader.osm." + name)
    return module.osm
