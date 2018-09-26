# -*- coding: utf-8 -*-


import json
import freecad.asm3.assembly
import FreeCAD
import FreeCADGui
import sys
import fnmatch
import os
from structure import Structure


class Assembly(object):

    def __init__(self, groups, parts, basedir):
        super(Assembly, self).__init__()
        self._groups = groups
        self._parts = parts
        self._basedir = basedir

    @classmethod
    def from_json(cls, filename):
        with open(filename, 'r') as f:
            _dict = json.load(f)
        groups = _dict.get('groups', [])
        parts = _dict.get('parts', [])
        basedir = os.path.dirname(filename)
        return cls(groups, parts, basedir)

    def abspath(self, path):
        return os.path.join(self._basedir, path)


class FreeCADAssembly(Assembly):

    def __init__(self, groups, parts, basedir, *args, **kwargs):
        super(FreeCADAssembly, self).__init__(groups, parts, basedir, *args, **kwargs)

    @property
    def document_name(self):
        return "assembly"

    def start(self):
        self.create_document()
        self.create_groups()
        for p in self._parts:
            self.create_part(p)

        FreeCAD.setActiveDocument(self.document_name)

    def create_document(self):
        FreeCAD.newDocument(self.document_name)
        FreeCAD.setActiveDocument(self.document_name)
        FreeCAD.ActiveDocument=FreeCAD.getDocument(self.document_name)
        FreeCADGui.ActiveDocument=FreeCADGui.getDocument(self.document_name)

        doc = FreeCAD.getDocument(self.document_name)
        doc.saveAs(self.abspath('assembly.fcstd'))

    def create_groups(self):
        doc = FreeCAD.getDocument(self.document_name)

        for g in self._groups:
            obj = doc.addObject('App::Part', g['name'])
            obj.Label = g['label']

        for g in self._groups:
            if g['parent'] != '':
                obj = doc.getObject(g['name'])
                doc.getObject(g['parent']).addObject(obj)

    def create_part(self, part):
        doc = FreeCAD.getDocument(self.document_name)

        newdoc = FreeCAD.openDocument(self.abspath(part['filename']))

        FreeCAD.setActiveDocument(self.document_name)

        if len(newdoc.RootObjects) > 1:
            print("More than one root object!")

        obj = newdoc.RootObjects[0]
        label, name = obj.Label, obj.Name
        doc.addObject('App::Link', part['name']).setLink(obj)
        doc.getObject(part['name']).Label = part['label']
        doc.getObject(part['parent']).addObject(doc.getObject(part['name']))
