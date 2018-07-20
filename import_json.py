# -*- coding: utf-8 -*-

import assembly

def open(filename):
    asm = assembly.FreeCADAssembly.from_json(filename)
    asm.start()
