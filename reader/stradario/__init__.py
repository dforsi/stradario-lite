#!/usr/bin/env python3

# Author: Daniele Forsi
# License: CC0

class Stradario:
    def __init__(self, *args):
        pass

    def __iter__(self):
        return iter([])

    def transform_accents(self, name):
        return name \
            .replace("À", "A'") \
            .replace("È", "E'") \
            .replace("É", "E'") \
            .replace("Ì", "I'") \
            .replace("Ò", "O'") \
            .replace("Ù", "U'") \

    def transform_italian_numbers(self, name):
        return name \
            .replace(" 2 ", " DUE ") \
            .replace(" 4 ", " QUATTRO ") \
            .replace(" 5° ", " QUINTO ") \
            .replace(" 8 ", " OTTO ") \
            .replace(" 11 ", " UNDICI ") \
            .replace(" 12 ", " DODICI ") \
            .replace(" 24 ", " VENTIQUATTRO ") \
            .replace(" XXV ", " VENTICINQUE ") \

    def transform_osm_name(self, name):
        return self.transform_italian_numbers(self.transform_accents(name.upper()))

    def transform_ext_name(self, name):
        return name

import importlib

def import_module(name):
    python_name = name.replace(" ", "_").replace("'", "_")
    try:
        imp = importlib.import_module("reader.stradario." + python_name)
        return eval("imp." + python_name)
    except ImportError as e:
        print(e)
        return Stradario
