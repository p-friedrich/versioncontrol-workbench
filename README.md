# VersionControl Workbench

The purpose of this workbench is, to explore the possibilities of using FreeCAD
in conjunction with different version control software.

Currently, two systems will be used:
- [Git](https://git-scm.com/) (free and open source)
- [LoCo](https://www.scale.eu/en/products/loco) (proprietary Simulation Data Management software by [SCALE GmbH](https://www.scale.eu/en))


# Features

## Opening JSON files

This workbench implements a new FreeCAD file importer. It can open special JSON
files, that represent the hierarchy of different CAD parts.


# Installation

Copy or link this folder to `~/.FreeCAD/Mod`.


# Additional Scripts

Easy to use helpers in the `scripts` folder.

## `open_from_folder`

Takes path to a folder as argument and creates the neccessary JSON file to be
openend with FreeCAD. Nested directories will be interpreted as a part
hierarchy.

## `open_from_loco`

Wrapper to open FreeCAD directly from the LoCo application. To be configured as
external application.
