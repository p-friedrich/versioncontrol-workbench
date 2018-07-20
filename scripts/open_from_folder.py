#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.split(os.path.split(__file__)[0])[0])

import structure
import subprocess


def main():
    basepath = os.path.abspath(os.path.dirname(sys.argv[1]))
    s = structure.Structure.from_folders(basepath)
    jsonpath = os.path.join(basepath, "structure.json")
    s.export_to_json(jsonpath)
    p = subprocess.Popen(["freecad", jsonpath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    for filename in ['assembly.fcstd']:
        path = os.path.join(basepath, filename)
        if os.path.exists(path):
            os.remove(path)


if __name__ == '__main__':
    main()
