#!/usr/bin/env python3

from test.labtesting import Lab, Result, SingleIntegerParameterRangeValidation, IntegerSequenceMixin, main
from itertools import chain
import array
import os
import random
import re
import string
import tempfile

import sys


class VectorSorting(Lab, IntegerSequenceMixin):
    def __init__(self, student, lab, name = None):
        Lab.__init__(self, student, lab, name)
        IntegerSequenceMixin.__init__(self, ['1', 'ascending'])

    def _cleanupOutput(self, str):
        return re.sub(' \n', '\n', str)

    def _sortNumbers(self, numbers, reverse):
        if isinstance(numbers, str):
            input = numbers + '\n'
            if numbers[0] == '+':
                expected = numbers[1:]
            else:
                expected = numbers
            numbers = [int(numbers)]
        else:
            input = ' '.join(map(str, numbers)) + '\n'
            numbers.sort(reverse = reverse)
            expected = ' '.join(map(str, numbers))

        expected += '\n'
        expected += expected + expected

        args = ['1', 'descending' if reverse else 'ascending']

        result = self.execute(args = args, input = input)

        sortedNumbers = []
        if result.exitCode == 0:
            try:
                lines = result.output.splitlines()
                sortedNumbers = list(map(lambda str: list(map(int, str.split())), lines))
            except Exception as e:
                result.error += 'Exception: ' + str(e)

        result.succeeded = (result.exitCode == 0) and (len(sortedNumbers) == 3) \
                           and (sortedNumbers[0] == numbers) \
                           and (sortedNumbers[1] == numbers) \
                           and (sortedNumbers[2] == numbers) \
                           and (len(result.error) == 0)
        result.expected = expected

        return result

    def testParameterWithSpace(self):
        args = ['1 3', 'ascending']

        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testMissingSortOrder(self):
        args = ['1']

        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testInvalidSortOrder(self):
        args = ['1', 'kjhgkj']

        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testSortOrderWithSpace(self):
        args = ['1', 'ascending descending']

        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testEmptyInput(self):
        args = ['1', 'ascending']

        result = self.execute(args = args)
        result.succeeded = (result.exitCode == 0) and ((len(result.output) == 0) or (result.output == '\n') or (result.output == '\n\n\n')) and (len(result.error) == 0)
        result.expected = ['', '\n', '\n\n\n']

        return result

    # TODO:
    # Add fault injection

    def testSinglePositiveNumber(self):
        numbers = '+' + str(random.randint(1, 1000))

        return self._sortNumbers(numbers, False)

    def testSingleNegativeNumber(self):
        numbers = [random.randint(-1000, -1)]

        return self._sortNumbers(numbers, False)

    def testRandomNumbersAscending(self):
        length = self.randomObjectLimit(2, 100)
        numbers = list(map(lambda x: random.randint(-1000, 1000), range(0, length)))

        return self._sortNumbers(numbers, False)

    def testRandomNumbersDescending(self):
        length = self.randomObjectLimit(2, 100)
        numbers = list(map(lambda x: random.randint(-1000, 1000), range(0, length)))

        return self._sortNumbers(numbers, True)


class FileReading(Lab):
    def __init__(self, student, lab, name = None):
        super(FileReading, self).__init__(student, lab, name)

    def testParameterWithSpace(self):
        with tempfile.NamedTemporaryFile() as source:
            args = ['2 3', source.name]

            result = self.execute(args = args)
            result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
            result.expected = 'Non-zero exit code and error message in standard error'

            return result

    def testMissingFileName(self):
        args = ['2']

        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testMissingFile(self):
        source =  tempfile.NamedTemporaryFile()
        args = ['2', source.name]
        source.close()

        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    # TODO:
    # Add fault injection

    def testEmptyFile(self):
        expected = ''
        with tempfile.NamedTemporaryFile() as source:
            args = ['2', source.name]
            result = self.execute(args = args)
            result.succeeded = (result.exitCode == 0) and (expected == result.output) and (len(result.error) == 0)

            return result

    def testFileRead(self):
        length = self.randomObjectLimit(4096, 40960)
        expected = array.array('B')
        for i in range(0, length - 1):
            expected.append(ord(random.choice(string.ascii_letters)))
        expected.append(ord('\n'))
        expected = expected.tobytes().decode('UTF-8')

        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(expected, 'UTF-8'))
            source.flush()

            args = ['2', source.name]
            result = self.execute(args = args)
            result.succeeded = (result.exitCode == 0) and (expected == result.output) and (len(result.error) == 0)
            result.expected = expected

            return result

    def testPipeRead(self):
        length = self.randomObjectLimit(1024, 2048)
        expected = array.array('B')
        for i in range(0, length - 1):
            expected.append(ord(random.choice(string.ascii_letters)))
        expected.append(ord('\n'))
        expected = expected.tobytes().decode('UTF-8')

        handle, filename = tempfile.mkstemp()

        def _writeData():
            with open(filename, 'w') as source:
                source.write(expected)

        os.close(handle)
        os.unlink(filename)
        os.mkfifo(filename)

        try:
            args = ['2', filename]
            result = self.execute(args = args, input = _writeData)
        finally:
            os.unlink(filename)

        result.succeeded = (result.exitCode == 0) and (expected == result.output) and (len(result.error) == 0)
        result.expected = expected

        return result

    # Temporary disabled because of limitation of xsltproc
    def _testHugeFileRead(self):
        length = self.randomObjectLimit(8, 10) * 1024 * 1024
        expected = array.array('B')
        for i in range(0, length - 1):
            expected.append(ord(random.choice(string.ascii_letters)))
        expected.append(ord('\n'))
        expected = expected.tobytes().decode('UTF-8')

        with tempfile.NamedTemporaryFile() as source:
            source.write(bytes(expected, 'UTF-8'))
            source.flush()

            args = ['2', source.name]
            result = self.execute(args = args)
            result.succeeded = (result.exitCode == 0) and (expected == result.output) and (len(result.error) == 0)
            result.expected = expected

            return result

class VectorProcessing(Lab, IntegerSequenceMixin):
    def __init__(self, student, lab, name = None):
        Lab.__init__(self, student, lab, name)
        IntegerSequenceMixin.__init__(self, ['3'])

        self.ARGS = ['3']

    def _randomInt(self, begin, end):
        result = random.randint(begin, end)

        while result == 0:
            result = random.randint(begin, end)

        return result

    def testParameterWithSpace(self):
        args = ['3 1']

        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testEmptyInput(self):
        result = self.execute(args = self.ARGS)
        result.succeeded = (result.exitCode == 0) and ((len(result.output) == 0) or (result.output == '\n') or (result.output == '\n\n\n')) and (len(result.error) == 0)
        result.expected = ['', '\n']

        return result

    # TODO:
    # Add fault injection
    def testSinglePositiveNumber(self):
        numbers = [random.randint(1, 1000) * 3, 1, 0]

        input = '+' + ' '.join(map(str, numbers)) + '\n'
        expected = list(filter(lambda x: x % 2 != 0, numbers[:-1]))

        result = self.execute(args = self.ARGS, input = input)

        processed = []
        if result.exitCode == 0:
            try:
                processed = list(map(int, result.output.split()))
                result.succeeded = (result.exitCode == 0) and (processed == expected) and (len(result.error) == 0)
            except Exception as e:
                result.succeeded = False
                result.error += 'Exception: ' + str(e)

        result.expected = ' '.join(map(str, expected)) + '\n'

        return result

    def testCorrectDataWith1Before0(self):
        numbers = list(chain(map(lambda x: self._randomInt(-1000, 1000) * 2, range(0, 2)),
                             map(lambda x: self._randomInt(-1000, 1000) * 3, range(0, 2)),
                             map(lambda x: self._randomInt(-1000, 1000), range(0, self.randomObjectLimit(10, 50))),
                             map(lambda x: self._randomInt(-1000, 1000) * 2, range(0, 2)),
                             map(lambda x: self._randomInt(-1000, 1000) * 3, range(0, 2)),
                             [1, 0]))

        input = ' '.join(map(str, numbers)) + '\n'
        expected = list(filter(lambda x: x % 2 != 0, numbers[:-1]))

        result = self.execute(args = self.ARGS, input = input)

        processed = []
        if result.exitCode == 0:
            try:
                processed = list(map(int, result.output.split()))
                result.succeeded = (result.exitCode == 0) and (processed == expected) and (len(result.error) == 0)
            except Exception as e:
                result.succeeded = False
                result.error += 'Exception: ' + str(e)

        result.expected = ' '.join(map(str, expected)) + '\n'

        return result

    def testCorrectDataWith2Before0(self):
        numbers = list(chain(map(lambda x: self._randomInt(-1000, 1000) * 2, range(0, 2)),
                             map(lambda x: self._randomInt(-1000, 1000) * 3, range(0, 2)),
                             map(lambda x: self._randomInt(-1000, 1000), range(0, self.randomObjectLimit(10, 50))),
                             map(lambda x: self._randomInt(-1000, 1000) * 2, range(0, 2)),
                             map(lambda x: self._randomInt(-1000, 1000) * 3, range(0, 2)),
                             [2, 0]))

        input = ' '.join(map(str, numbers)) + '\n'
        expected = []
        for i in numbers[:-1]:
            if i % 3 == 0:
                expected += [i, 1, 1, 1]
            else:
                expected.append(i)

        result = self.execute(args = self.ARGS, input = input)

        processed = []
        if result.exitCode == 0:
            try:
                processed = list(map(int, result.output.split()))
                result.succeeded = (result.exitCode == 0) and (processed == expected) and (len(result.error) == 0)
            except Exception as e:
                result.succeeded = False
                result.error += 'Exception: ' + str(e)

        result.expected = ' '.join(map(str, expected)) + '\n'

        return result

    def testCorrectDataWithArbitraryNumberBefore0(self):
        numbers = list(chain(map(lambda x: self._randomInt(-1000, 1000) * 2, range(0, 2)),
                             map(lambda x: self._randomInt(-1000, 1000) * 3, range(0, 2)),
                             map(lambda x: self._randomInt(-1000, 1000), range(0, self.randomObjectLimit(10, 50))),
                             map(lambda x: self._randomInt(-1000, 1000) * 2, range(0, 2)),
                             map(lambda x: self._randomInt(-1000, 1000) * 3, range(0, 2)),
                             [self._randomInt(-1000, 1000) * 3 + 3, 0]))

        input = ' '.join(map(str, numbers)) + '\n'
        expected = numbers[:-1]

        result = self.execute(args = self.ARGS, input = input)

        processed = []
        if result.exitCode == 0:
            try:
                processed = list(map(int, result.output.split()))
                result.succeeded = (result.exitCode == 0) and (processed == expected) and (len(result.error) == 0)
            except Exception as e:
                result.succeeded = False
                result.error += 'Exception: ' + str(e)

        result.expected = ' '.join(map(str, expected)) + '\n'

        return result

    def testMissingZero(self):
        numbers = list(chain(map(lambda x: self._randomInt(-1000, 1000) * 2, range(0, 2)),
                             map(lambda x: self._randomInt(-1000, 1000) * 3, range(0, 2)),
                             map(lambda x: self._randomInt(-1000, 1000), range(0, self.randomObjectLimit(10, 50))),
                             map(lambda x: self._randomInt(-1000, 1000) * 2, range(0, 2)),
                             map(lambda x: self._randomInt(-1000, 1000) * 3, range(0, 2)),
                             [5]))

        input = ' '.join(map(str, numbers)) + '\n'

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result


class FPSorting(Lab):
    def __init__(self, student, lab, name = None):
        super(FPSorting, self).__init__(student, lab, name)

    def testParameterWithSpace(self):
        args = ['4 3', 'ascending', '10']

        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testSortOrderWithSpace(self):
        args = ['4', 'ascending descending', '10']

        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testNumberCountWithSpace(self):
        args = ['4', 'ascending', str(self.randomObjectLimit(10, 1000)) + ' ' + str(self.randomObjectLimit(10, 1000))]

        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testSortAscending(self):
        length = self.randomObjectLimit(10, 1000)

        args = ['4', 'ascending', str(length)]

        result = self.execute(args = args)

        data = [[]]
        if result.exitCode == 0:
            try:
                lines = result.output.splitlines()
                data = list(map(lambda str: list(map(float, str.split())), lines))
            except Exception as e:
                result.error += 'Exception: ' + str(e)

        if len(data) > 0:
            data[0].sort()

        result.succeeded = (result.exitCode == 0) and (len(data) == 2) and (len(data[0]) == length) \
                           and (len(data[1]) == length) and (data[0] == data[1]) and (len(result.error) == 0)
        result.expected = 'Generated and sorted data'

        return result

    def testSortDescending(self):
        length = self.randomObjectLimit(10, 1000)

        args = ['4', 'descending', str(length)]

        result = self.execute(args = args)

        data = [[]]
        if result.exitCode == 0:
            try:
                lines = result.output.splitlines()
                data = list(map(lambda str: list(map(float, str.split())), lines))
            except Exception as e:
                result.error += 'Exception: ' + str(e)

        if len(data) > 0:
            data[0].sort(reverse = True)

        result.succeeded = (result.exitCode == 0) and (len(data) == 2) and (len(data[0]) == length) \
                           and (len(data[1]) == length) and (data[0] == data[1]) and (len(result.error) == 0)
        result.expected = 'Generated and sorted data'

        return result

    def testMissingLength(self):
        args = ['4', 'ascending']

        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testInvalidLength(self):
        args = ['4', 'ascending', 'garbage']

        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testMissingSortOrder(self):
        args = ['4']

        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testInvalidSortOrder(self):
        args = ['4', 'kjhgkj', str(random.randint(10, 1000))]

        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result


class LabB1(Lab):
    def __init__(self, student):
        super(LabB1, self).__init__(student, 'B1')

        self.testBase = SingleIntegerParameterRangeValidation(student, self.lab, 1, 4, 'Overall program parameter check')
        self.testSection1 = VectorSorting(student, self.lab, 'Lab ' + self.lab + '.1: vector of integers sorting')
        self.testSection2 = FileReading(student, self.lab, 'Lab ' + self.lab + '.2: file reading')
        self.testSection3 = VectorProcessing(student, self.lab, 'Lab ' + self.lab + '.3: vector processing')
        self.testSection4 = FPSorting(student, self.lab, 'Lab ' + self.lab + '.4: vector of doubles sorting')


if __name__ == "__main__":
    main(LabB1(sys.argv[1]))
