#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.split(os.path.split(__file__)[0])[0])

import structure
import subprocess


def main():
    basepath = os.path.dirname(sys.argv[1])
    files = [os.path.join(basepath, f.replace("fcstd", "fatxml"))
             for f in os.listdir(basepath)
             if f.endswith(".fcstd")]
    s = structure.Structure.from_fatxmls(basepath, filenames=files)
    jsonpath = os.path.join(basepath, "structure.json")
    s.export_to_json(jsonpath)
    p = subprocess.Popen(["freecad", jsonpath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    for filename in ['structure.json', 'assembly.fcstd']:
        path = os.path.join(basepath, filename)
        if os.path.exists(path):
            os.remove(path)


if __name__ == '__main__':
    main()
