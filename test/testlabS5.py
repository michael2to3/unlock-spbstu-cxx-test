#!/usr/bin/env python3

from test.labtesting import Lab, Result, main
import sys
import os.path
import random
import string
import tempfile

class LabS5(Lab):
    def __init__(self, student):
        super(LabS5, self).__init__(student, 'S5')

    def testNotEnoughArgs(self):
        result = self.execute()
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'
        return result

    def testStillNotEnough(self):
        args = ['one']
        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'
        return result

    def testTooManyArgs(self):
        args = ['one', 'two', 'three']
        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'
        return result

    def testUnexpectedArgs(self):
        data1 = '2 first 1 name 3 surname\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1, 'utf-8'))
            source.flush()
            args = ['random', source.name]
            result = self.execute(args = args)
            result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
            result.expected = 'Non-zero exit code and error message in standard error'
            return result

    def testAscending(self):
        data1 = '2 first 1 name 3 surname\n'
        expected = '6 name first surname\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1, 'utf-8'))
            source.flush()
            args = ['ascending', source.name]
            result = self.execute(args = args)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\nexpected result is:\n\t' + expected
            return result

    def testDescending(self):
        data1 = '2 first 1 name 3 surname\n'
        expected = '6 surname first name\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1, 'utf-8'))
            source.flush()
            args = ['descending', source.name]
            result = self.execute(args = args)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\nexpected result is:\n\t' + expected
            return result

    def testBreadth(self):
        data1 = '2 first 1 name 3 surname\n'
        expected = '6 first name surname\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1, 'utf-8'))
            source.flush()
            args = ['breadth', source.name]
            result = self.execute(args = args)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = 'With data:\n\t' + data1 + '\nexpected result is:\n\t' + expected
            return result

    def testEmpty(self):
        data1 = '\n'
        expected = '<EMPTY>\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1, 'utf-8'))
            source.flush()
            args = ['breadth', source.name]
            result = self.execute(args = args)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = expected
            return result

    def testOverflow(self):
        data1 = '1 first 9223372036854775807 second\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1, 'utf-8'))
            source.flush()
            args = ['breadth', source.name]
            result = self.execute(args = args)
            result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
            result.expected = 'Non-zero exit code and error message in standard error'
            return result

    def testUnderflow(self):
        data1 = '-1 first -9223372036854775808 second\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(data1, 'utf-8'))
            source.flush()
            args = ['breadth', source.name]
            result = self.execute(args = args)
            result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
            result.expected = 'Non-zero exit code and error message in standard error'
            return result

if __name__ == "__main__":
    main(LabS5(sys.argv[1]))
