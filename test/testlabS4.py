#!/usr/bin/env python3

from test.labtesting import Lab, Result, main
import sys
import os.path
import random
import string
import tempfile

class LabS4(Lab):
    def __init__(self, student):
        super(LabS4, self).__init__(student, 'S4')

    def testNotEnoughArgs(self):
        result = self.execute()
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'
        return result

    def testTooManyArgs(self):
        args = ['one', 'two']
        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'
        return result

    def testUnexpectedCommand(self):
        data1 = 'first 1 name 2 surname\n'
        data2 = 'second 4 mouse 1 name 2 keyboard\n'
        input = 'unexpected second\n'
        expected = '<INVALID COMMAND>\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1 + data2, 'utf-8'))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\t' + data2 + '\nexpected result is:\n\t' + expected
            return result

    def testSeveralCommands(self):
        data1 = 'first 1 name 2 surname\n'
        data2 = 'second 4 mouse 1 name 2 keyboard\n'
        input = 'union third first second\ncomplement fourth first first\nintersect first third fourth\nprint first\n'
        expected = '<EMPTY>\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1 + data2, 'utf-8'))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\t' + data2 + '\nexpected result is:\n\t' + expected
            return result

    def testPrintNonEmptyDictionary(self):
        data1 = 'first 1 name 2 surname\n'
        data2 = 'second 4 mouse 1 name 2 keyboard\n'
        input = 'print second\n'
        expected = 'second 1 name 2 keyboard 4 mouse\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1 + data2, 'utf-8'))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\t' + data2 + '\nexpected result is:\n\t' + expected
            return result

    def testPrintEmptyDictionary(self):
        data1 = 'first\n'
        data2 = 'second 4 mouse 1 name 2 keyboard\n'
        input = 'print first\n'
        expected = '<EMPTY>\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1 + data2, 'utf-8'))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\t' + data2 + '\nexpected result is:\n\t' + expected
            return result

    def testPrintNonExistentDictionary(self):
        data1 = 'first\n'
        data2 = 'second 4 mouse 1 name 2 keyboard\n'
        input = 'print third\n'
        expected = '<INVALID COMMAND>\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1 + data2, 'utf-8'))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\t' + data2 + '\nexpected result is:\n\t' + expected
            return result

    def testComplementDictionaries(self):
        data1 = 'first 1 name 2 surname\n'
        data2 = 'second 4 mouse 1 name 2 keyboard\n'
        input = 'complement third second first\nprint third\n'
        expected = 'third 4 mouse\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1 + data2, 'utf-8'))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\t' + data2 + '\nexpected result is:\n\t' + expected
            return result

    def testComplementDictionariesToExistentDictionary(self):
        data1 = 'first 1 name 2 surname\n'
        data2 = 'second 4 mouse 1 name 2 keyboard\n'
        input = 'complement second second first\nprint second\n'
        expected = 'second 4 mouse\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1 + data2, 'utf-8'))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\t' + data2 + '\nexpected result is:\n\t' + expected
            return result

    def testComplementSameDictionaries(self):
        data1 = 'first 1 name 2 surname\n'
        data2 = 'second 4 mouse 1 name 2 keyboard\n'
        input = 'complement third second second\nprint third\n'
        expected = '<EMPTY>\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1 + data2, 'utf-8'))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\t' + data2 + '\nexpected result is:\n\t' + expected
            return result

    def testComplementNonExistentDictionaries(self):
        data1 = 'first 1 name 2 surname\n'
        data2 = 'second 4 mouse 1 name 2 keyboard\n'
        input = 'complement third third second\n'
        expected = '<INVALID COMMAND>\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1 + data2, 'utf-8'))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\t' + data2 + '\nexpected result is:\n\t' + expected
            return result

    def testIntersectDictionaries(self):
        data1 = 'first 1 name 2 surname\n'
        data2 = 'second 4 mouse 1 name 2 keyboard\n'
        input = 'intersect third second first\nprint third\n'
        expected = 'third 1 name 2 keyboard\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1 + data2, 'utf-8'))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\t' + data2 + '\nexpected result is:\n\t' + expected
            return result

    def testIntersectDictionariesToExistentDictionary(self):
        data1 = 'first 1 name 2 surname\n'
        data2 = 'second 4 mouse 1 name 2 keyboard\n'
        input = 'intersect second second first\nprint second\n'
        expected = 'second 1 name 2 keyboard\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1 + data2, 'utf-8'))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\t' + data2 + '\nexpected result is:\n\t' + expected
            return result

    def testIntersectSameDictionaries(self):
        data1 = 'first 1 name 2 surname\n'
        data2 = 'second 4 mouse 1 name 2 keyboard\n'
        input = 'intersect third second second\nprint third\n'
        expected = 'third 1 name 2 keyboard 4 mouse\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1 + data2, 'utf-8'))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\t' + data2 + '\nexpected result is:\n\t' + expected
            return result

    def testIntersectDictionariesWithoutIntersection(self):
        data1 = 'first 3 name 5 surname\n'
        data2 = 'second 4 mouse 1 name 2 keyboard\n'
        input = 'intersect third first second\nprint third\n'
        expected = '<EMPTY>\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1 + data2, 'utf-8'))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\t' + data2 + '\nexpected result is:\n\t' + expected
            return result

    def testIntersectWithEmptyDictionary(self):
        data1 = 'first\n'
        data2 = 'second 4 mouse 1 name 2 keyboard\n'
        input = 'intersect third first second\nprint third\n'
        expected = '<EMPTY>\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1 + data2, 'utf-8'))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\t' + data2 + '\nexpected result is:\n\t' + expected
            return result

    def testIntersectNonExistentDictionaries(self):
        data1 = 'first 3 name 5 surname\n'
        data2 = 'second 4 mouse 1 name 2 keyboard\n'
        input = 'intersect third third second\n'
        expected = '<INVALID COMMAND>\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1 + data2, 'utf-8'))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\t' + data2 + '\nexpected result is:\n\t' + expected
            return result

    def testUnionDictionaries(self):
        data1 = 'first 1 name 3 machine 2 surname\n'
        data2 = 'second 4 mouse 1 name 2 keyboard\n'
        input = 'union third second first\nprint third\n'
        expected = 'third 1 name 2 keyboard 3 machine 4 mouse\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1 + data2, 'utf-8'))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\t' + data2 + '\nexpected result is:\n\t' + expected
            return result

    def testUnionDictionariesToExistentDictionary(self):
        data1 = 'first 1 name 3 machine 2 surname\n'
        data2 = 'second 4 mouse 1 name 2 keyboard\n'
        input = 'union first second first\nprint first\n'
        expected = 'first 1 name 2 keyboard 3 machine 4 mouse\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1 + data2, 'utf-8'))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\t' + data2 + '\nexpected result is:\n\t' + expected
            return result

    def testUnionSameDictionaries(self):
        data1 = 'first 1 name 3 machine 2 surname\n'
        data2 = 'second 4 mouse 1 name 2 keyboard\n'
        input = 'union third first first\nprint third\n'
        expected = 'third 1 name 2 surname 3 machine\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1 + data2, 'utf-8'))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\t' + data2 + '\nexpected result is:\n\t' + expected
            return result

    def testUnionEmptyDictionaries(self):
        data1 = 'first\n'
        data2 = 'second\n'
        input = 'union third first second\nprint third\n'
        expected = '<EMPTY>\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1 + data2, 'utf-8'))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\t' + data2 + '\nexpected result is:\n\t' + expected
            return result

    def testUnionWithEmptyDictionary(self):
        data1 = 'first 1 name 3 machine 2 surname\n'
        data2 = 'second\n'
        input = 'union third first second\nprint third\n'
        expected = 'third 1 name 2 surname 3 machine\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1 + data2, 'utf-8'))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\t' + data2 + '\nexpected result is:\n\t' + expected
            return result

    def testUnionWithNonExistentDictionary(self):
        data1 = 'first 1 name 3 machine 2 surname\n'
        data2 = 'second\n'
        input = 'union third third second\n'
        expected = '<INVALID COMMAND>\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1 + data2, 'utf-8'))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = input)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\t' + data2 + '\nexpected result is:\n\t' + expected
            return result

if __name__ == "__main__":
    main(LabS4(sys.argv[1]))
