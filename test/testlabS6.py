#!/usr/bin/env python3

from test.labtesting import Lab, Result, main
import sys
import os.path
import random
import string
import tempfile

class LabS6(Lab):
    def __init__(self, student):
        super(LabS6, self).__init__(student, 'S6')

    def testNotEnoughArgs(self):
        result = self.execute()
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'
        return result

    def testStillNotEnoughArgs(self):
        args = ['one']
        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'
        return result

    def testYesStillNotEnoughArgs(self):
        args = ['one', 'two']
        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'
        return result

    def testUnexpectedArgs(self):
        args = ['bitonic', 'complex', 'FF']
        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'
        return result

    def testEmptySequence(self):
        args = ['ascending', 'ints', '0']
        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'
        return result

    def _convertableToInt(self, data):
        try:
            int(data)
            return True
        except ValueError:
            return False
    def _convertableToFloat(self, data):
        try:
            float(data)
            return not self._convertableToInt(data)
        except ValueError:
            return False

    def testUnaryIntSequence(self):
        args = ['ascending', 'ints', '1']
        result = self.execute(args = args)
        splitted = result.output.split('\n')
        if len(splitted) == 8:
            unsorted = splitted[0]
            convertable = all(j for j in [self._convertableToInt(i) for i in unsorted.split(' ')])
            if convertable:
                intsequence = [int(i) for i in unsorted.split(' ')]
                intsequence.sort()
                sortedstr = ' '.join([str(i) for i in intsequence])
                allsorted = all(data == sortedstr for data in splitted[1:6])
                result.succeeded = (result.exitCode == 0) and (len(result.error) == 0) and allsorted
                result.expected = sortedstr
                return result
            result.succeeded = False
            result.expected = 'Convertable to int value on each line\n'
        result.succeeded = False
        result.expected = 'Seven lines with int value on each line and newline after last one\n'
        return result

    def testUnaryFloatSequence(self):
        args = ['ascending', 'floats', '1']
        result = self.execute(args = args)
        splitted = result.output.split('\n')
        if len(splitted) == 8:
            unsorted = splitted[0]
            convertable = all(j for j in [self._convertableToFloat(i) for i in unsorted.split(' ')])
            if convertable:
                intsequence = [float(i) for i in unsorted.split(' ')]
                intsequence.sort()
                sortedstr = ' '.join([str(i) for i in intsequence])
                allsorted = all(data == sortedstr for data in splitted[1:6])
                result.succeeded = (result.exitCode == 0) and (len(result.error) == 0) and allsorted
                result.expected = sortedstr
                return result
            result.succeeded = False
            result.expected = 'Convertable to float only value on each line\n'
        result.succeeded = False
        result.expected = 'Seven lines with float value on each line and newline after last one\n'
        return result

    def testAscendingIntSequence(self):
        args = ['ascending', 'ints', '5']
        result = self.execute(args = args)
        splitted = result.output.split('\n')
        if len(splitted) == 8:
            unsorted = splitted[0]
            convertable = all(j for j in [self._convertableToInt(i) for i in unsorted.split(' ')])
            if convertable:
                intsequence = [int(i) for i in unsorted.split(' ')]
                intsequence.sort()
                sortedstr = ' '.join([str(i) for i in intsequence])
                allsorted = all(data == sortedstr for data in splitted[1:6])
                result.succeeded = (result.exitCode == 0) and (len(result.error) == 0) and allsorted
                result.expected = sortedstr
                return result
            result.succeeded = False
            result.expected = 'Convertable to int values on each line\n'
        result.succeeded = False
        result.expected = 'Seven lines with int values on each line and newline after last one\n'
        return result

    def testDescendingIntSequence(self):
        args = ['descending', 'ints', '5']
        result = self.execute(args = args)
        splitted = result.output.split('\n')
        if len(splitted) == 8:
            unsorted = splitted[0]
            convertable = all(j for j in [self._convertableToInt(i) for i in unsorted.split(' ')])
            if convertable:
                intsequence = [int(i) for i in unsorted.split(' ')]
                intsequence.sort(reverse = True)
                sortedstr = ' '.join([str(i) for i in intsequence])
                allsorted = all(data == sortedstr for data in splitted[1:6])
                result.succeeded = (result.exitCode == 0) and (len(result.error) == 0) and allsorted
                result.expected = sortedstr
                return result
            result.succeeded = False
            result.expected = 'Convertable to int values on each line\n'
        result.succeeded = False
        result.expected = 'Seven lines with int values on each line and newline after last one\n'
        return result

    def testAscendingFloatSequence(self):
        args = ['ascending', 'floats', '5']
        result = self.execute(args = args)
        splitted = result.output.split('\n')
        if len(splitted) == 8:
            unsorted = splitted[0]
            convertable = all(j for j in [self._convertableToFloat(i) for i in unsorted.split(' ')])
            if convertable:
                intsequence = [float(i) for i in unsorted.split(' ')]
                intsequence.sort()
                sortedstr = ' '.join([str(i) for i in intsequence])
                allsorted = all(data == sortedstr for data in splitted[1:6])
                result.succeeded = (result.exitCode == 0) and (len(result.error) == 0) and allsorted
                result.expected = sortedstr
                return result
            result.succeeded = False
            result.expected = 'Convertable to float only values on each line\n'
        result.succeeded = False
        result.expected = 'Seven lines with float values on each line and newline after last one\n'
        return result

    def testDescendingFloatSequence(self):
        args = ['descending', 'floats', '5']
        result = self.execute(args = args)
        splitted = result.output.split('\n')
        if len(splitted) == 8:
            unsorted = splitted[0]
            convertable = all(j for j in [self._convertableToFloat(i) for i in unsorted.split(' ')])
            if convertable:
                intsequence = [float(i) for i in unsorted.split(' ')]
                intsequence.sort(reverse = True)
                sortedstr = ' '.join([str(i) for i in intsequence])
                allsorted = all(data == sortedstr for data in splitted[1:6])
                result.succeeded = (result.exitCode == 0) and (len(result.error) == 0) and allsorted
                result.expected = sortedstr
                return result
            result.succeeded = False
            result.expected = 'Convertable to float only values on each line\n'
        result.succeeded = False
        result.expected = 'Seven lines with float values on each line and newline after last one\n'
        return result

if __name__ == "__main__":
    main(LabS6(sys.argv[1]))
