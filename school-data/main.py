#!/usr/bin/python3

from parser import parser

p = parser()
p.create_schema()
p.create_index()
p.add_dir_to_index("files")
p.search("test")