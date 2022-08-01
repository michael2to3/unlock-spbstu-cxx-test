#!/usr/bin/env python3

import os
import sys
import collections
from test.labtesting import main

filepath = os.path.realpath(__file__)
for entry in os.scandir(filepath[:filepath.rfind('/')] + '/test/'):
    if entry.is_file():
        string = f'from test.{entry.name[:-3]} import *'
        exec (string)

def strToClass(classname):
    return getattr(sys.modules[__name__], classname)


# python ./test-lab-T0 podshivalov.georgiy out/podshivalov.georgiy/T0/acceptance.xml
if len(sys.argv) < 2:
    print('Give me your code!')
    exit(1)

namelab = sys.argv[1].split('/')[-1]
print('Check lab -', namelab)
lab = strToClass('Lab' + namelab)
if len(sys.argv) < 3:
    try:
        os.mkdir('dist')
    except FileExistsError:
        pass

    sys.argv.append('dist/acceptance.xml')

collections.Sequence = collections.abc.Sequence

pathtolab = sys.argv[1][:sys.argv[1].rfind('/')]
print(main(lab(pathtolab)))
