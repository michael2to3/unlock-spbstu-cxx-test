#!/usr/bin/env python3

import os
import sys
import collections
from test.labtesting import main

filepath = os.path.realpath(__file__)
for entry in os.scandir(filepath[:filepath.rfind('/')] + '/test/'):
    if entry.is_file() and entry.name[-3:] == '.py':
        string = f'from test.{entry.name[:-3]} import *'
        exec (string)

def strToClass(classname):
    return getattr(sys.modules[__name__], classname)

if len(sys.argv) < 2:
    print('Give me your code!')
    exit(1)

namelab = sys.argv[1]
if namelab[-1] == '/':
    namelab = namelab[:-1]
student = namelab.split('/')[-2]
namelab = namelab.split('/')[-1]

pathtolab = sys.argv[1][:sys.argv[1].rfind('/')]
os.chdir(pathtolab + '/..')
print('cd', os.getcwd())

target = student + '/' + namelab

sys.argv.pop()
sys.argv.append(target)

print('Check lab -', student, '-', namelab)
lab = strToClass('Lab' + namelab)
if len(sys.argv) < 3:
    try:
        os.mkdir('dist')
    except FileExistsError:
        pass

    defaultpathfile = 'dist/acceptance.xml'
    fxml = open(defaultpathfile, 'w')
    fxml.close()

    sys.argv.append(defaultpathfile)

collections.Sequence = collections.abc.Sequence

print(main(lab(student)))
