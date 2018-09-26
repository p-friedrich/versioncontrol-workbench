# -*- coding: utf-8 -*-

import re
import glob
import fnmatch
import os
import json


class Structure(object):

    def __init__(self, groups=[], parts=[]):
        self._groups = groups
        self._parts = parts

    @classmethod
    def from_folders(cls, basedir):
        matches = []
        for root, dirnames, filenames in os.walk(basedir):
            for filename in fnmatch.filter(filenames, '*.fcstd'):
                matches.append(os.path.join(root, filename))
        parts = []
        groups = []
        for m in matches:
            # m = os.path.relpath(m, os.path.split(basedir)[0])
            m = os.path.relpath(m, basedir)
            p, g = cls.extract_path(m)
            parts.append(p)
            groups += g
        groupdict = {g['name']: g for g in groups}
        groups = [v for _, v in groupdict.items()]
        return cls(groups, parts)

    @classmethod
    def from_fatxmls(cls, basedir, filenames=[]):
        """Search for all fatxml files and create structure from Loco path"""
        groups = []
        parts = []
        if len(filenames) > 0:
            source = [f for f in filenames if os.path.splitext(f)[1] == '.xml']
        else:
            source = glob.glob("{0}/*.fatxml".format(basedir))
        for fn in source:
            raw_path = cls.extract_tree_path_from_fatxml(fn)
            path = [cls.parse_name_without_underscore(r) for r in raw_path]
            parent = ''
            for g in path:
                groups.append({'name': g[0], 'label': g[1], 'parent': parent})
                parent = g[0]
            name, label = cls.parse_name_without_underscore(os.path.splitext(os.path.basename(fn))[0])
            parts.append({'name': name, 'label': label, 'parent': parent, 'filename': os.path.splitext(fn)[0]})
        groupdict = {g['name']: g for g in groups}
        groups = [v for _, v in groupdict.items()]
        return cls(groups, parts)

    @staticmethod
    def extract_tree_path_from_fatxml(filename):
        def find_tree_path_string(fatxml_content):
            pattern = r"<loco_tree_path>.*?<value>(?P<tree_path_string>.*?)</value>.*?</loco_tree_path>"
            m = re.search(pattern, fatxml_content, re.DOTALL)
            if m is not None:
                return m.group(1)
            else:
                raise ValueError("<loco_tree_path> not found in fatxml.")

        def parse_tree_path(tps):
            return tps.split('/')

        path = filename
        with open(path, "r") as f:
            content = f.read()
        tps = find_tree_path_string(content)
        return parse_tree_path(tps)[1:]

    @staticmethod
    def parse_name_without_underscore(name):
        """Parse name like 'body_in_white___________________________PID1' into name and label"""
        split = name.split('_')
        pid = ''.join(split[-2:])
        label = '_'.join(s for s in split[:-2] if s)
        if name.endswith('.fcstd'):
            pid = pid[:-6]
        return pid, label

    @staticmethod
    def parse_name(name):
        """Parse name like 'body_in_white___________________________PID_1' into name and label"""
        split = name.split('_')
        pid = name[name.find('PID'):]
        label = '_'.join(s for s in split[:-1] if s)
        if name.endswith('.fcstd'):
            pid = pid[:-6]
        return pid, label

    @staticmethod
    def extract_path(filename):
        """Extract Group Path from"""
        groups = []
        parent = ''
        for element in filename.split(os.path.sep)[:-1]:
            if element == '.':
                continue
            name, label = Structure.parse_name(element)
            groups.append({'name': name, 'label': label, 'parent': parent})
            parent = name

        p = os.path.split(filename)[1]
        name, label = Structure.parse_name(p)
        part = {'name': name, 'label': label, 'parent': parent, 'filename': filename}
        return part, groups

    def export_to_json(self, filename):
        _dict = {}
        _dict['parts'] = self._parts
        _dict['groups'] = self._groups

        with open(filename, 'w') as f:
            json.dump(_dict, f, indent=4)

