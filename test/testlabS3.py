#!/usr/bin/env python3

from test.labtesting import Lab, Result, main
import sys
import os.path
import random
import string
import tempfile

class LabS3(Lab):
    def __init__(self, student):
        super(LabS3, self).__init__(student, 'S3')

    def _formDatasetForFile(self, dataset):
        returnable = bytes('', 'utf-8')
        for data in dataset:
            returnable = returnable + bytes(data + '\n', 'utf-8')
        return returnable

    def _formDatasetForExpected(self, dataset, expected):
        returnable = 'With data:\n'
        for data in dataset:
            returnable = returnable + '\t' + data + '\n'
        returnable = returnable + 'Expected result is:\n'
        for data in expected:
            returnable = returnable + '\t' + data + '\n'
        return returnable

    def _formInputCommands(self, commands):
        returnable = ''
        for data in commands:
            returnable = returnable + data + '\n'
        return returnable

    def _formExpected(self, expected):
        return self._formInputCommands(expected)

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
        dataset = [
          'first 1 3 2 1',
          'second 6 0 -1 1',
          'third'
        ]
        commands = [
          'unexpected command'
        ]
        expected = [
          '<INVALID COMMAND>'
        ]
        with tempfile.NamedTemporaryFile() as source:
            source.write(self._formDatasetForFile(dataset))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = self._formInputCommands(commands))
            result.succeeded = (result.exitCode == 0) and (result.output == self._formExpected(expected)) and (len(result.error) == 0)
            result.expected = self._formDatasetForExpected(dataset, expected)
            return result


    def testSkipEmptyLinesInDataset(self):
        dataset = [
          '',
          'first 1 3 2 1',
          '',
          'third',
          ''
        ]
        commands = [
          'print first'
        ]
        expected = [
          'first 1 3 2 1'
        ]
        with tempfile.NamedTemporaryFile() as source:
            source.write(self._formDatasetForFile(dataset))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = self._formInputCommands(commands))
            result.succeeded = (result.exitCode == 0) and (result.output == self._formExpected(expected)) and (len(result.error) == 0)
            result.expected = self._formDatasetForExpected(dataset, expected)
            return result

    def testPrintCommandWithEmptyList(self):
        dataset = [
          'first 1 3 2 1',
          'second 6 0 -1 1',
          'third'
        ]
        commands = [
          'print third'
        ]
        expected = [
          '<EMPTY>'
        ]
        with tempfile.NamedTemporaryFile() as source:
            source.write(self._formDatasetForFile(dataset))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = self._formInputCommands(commands))
            result.succeeded = (result.exitCode == 0) and (result.output == self._formExpected(expected)) and (len(result.error) == 0)
            result.expected = self._formDatasetForExpected(dataset, expected)
            return result

    def testPrintCommandWithNotEnoughParams(self):
        dataset = [
          'first 1 3 2 1',
          'second 6 0 -1 1',
          'third'
        ]
        commands = [
          'print'
        ]
        expected = [
          '<INVALID COMMAND>'
        ]
        with tempfile.NamedTemporaryFile() as source:
            source.write(self._formDatasetForFile(dataset))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = self._formInputCommands(commands))
            result.succeeded = (result.exitCode == 0) and (result.output == self._formExpected(expected)) and (len(result.error) == 0)
            result.expected = self._formDatasetForExpected(dataset, expected)
            return result

    def testReplaceCommandWithValueArgs(self):
        dataset = [
          'first 1 3 2 1',
          'second 6 0 -1 1',
          'third'
        ]
        commands = [
          'replace first 1 2',
          'print first'
        ]
        expected = [
          'first 2 3 2 2'
        ]
        with tempfile.NamedTemporaryFile() as source:
            source.write(self._formDatasetForFile(dataset))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = self._formInputCommands(commands))
            result.succeeded = (result.exitCode == 0) and (result.output == self._formExpected(expected)) and (len(result.error) == 0)
            result.expected = self._formDatasetForExpected(dataset, expected)
            return result

    def testReplaceCommandWithAnotherListArg(self):
        dataset = [
          'first 1 3 2 1',
          'second 6 0 -1 1',
          'third'
        ]
        commands = [
          'replace first 2 second',
          'print first'
        ]
        expected = [
          'first 1 3 6 0 -1 1 1'
        ]
        with tempfile.NamedTemporaryFile() as source:
            source.write(self._formDatasetForFile(dataset))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = self._formInputCommands(commands))
            result.succeeded = (result.exitCode == 0) and (result.output == self._formExpected(expected)) and (len(result.error) == 0)
            result.expected = self._formDatasetForExpected(dataset, expected)
            return result

    def testReplaceCommandWithNotEnoughArgs(self):
        dataset = [
          'first 1 3 2 1',
          'second 6 0 -1 1',
          'third'
        ]
        commands = [
          'replace',
          'replace first',
          'replace first 2',
          'print first'
        ]
        expected = [
          '<INVALID COMMAND>',
          '<INVALID COMMAND>',
          '<INVALID COMMAND>',
          'first 1 3 2 1'
        ]
        with tempfile.NamedTemporaryFile() as source:
            source.write(self._formDatasetForFile(dataset))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = self._formInputCommands(commands))
            result.succeeded = (result.exitCode == 0) and (result.output == self._formExpected(expected)) and (len(result.error) == 0)
            result.expected = self._formDatasetForExpected(dataset, expected)
            return result

    def testRemoveWithValueArg(self):
        dataset = [
          'first 1 3 2 1',
          'second 6 0 -1 1',
          'third'
        ]
        commands = [
          'remove first 1',
          'print first'
        ]
        expected = [
          'first 3 2'
        ]
        with tempfile.NamedTemporaryFile() as source:
            source.write(self._formDatasetForFile(dataset))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = self._formInputCommands(commands))
            result.succeeded = (result.exitCode == 0) and (result.output == self._formExpected(expected)) and (len(result.error) == 0)
            result.expected = self._formDatasetForExpected(dataset, expected)
            return result

    def testRemoveWithListArg(self):
        dataset = [
          'first 1 3 2 1',
          'second 6 3 -1 1',
          'third'
        ]
        commands = [
          'remove first second',
          'print first'
        ]
        expected = [
          'first 2'
        ]
        with tempfile.NamedTemporaryFile() as source:
            source.write(self._formDatasetForFile(dataset))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = self._formInputCommands(commands))
            result.succeeded = (result.exitCode == 0) and (result.output == self._formExpected(expected)) and (len(result.error) == 0)
            result.expected = self._formDatasetForExpected(dataset, expected)
            return result

    def testRemoveCommandWithNotEnoughArgs(self):
        dataset = [
          'first 1 3 2 1',
          'second 6 0 -1 1',
          'third'
        ]
        commands = [
          'remove',
          'remove first',
          'print first'
        ]
        expected = [
          '<INVALID COMMAND>',
          '<INVALID COMMAND>',
          'first 1 3 2 1'
        ]
        with tempfile.NamedTemporaryFile() as source:
            source.write(self._formDatasetForFile(dataset))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = self._formInputCommands(commands))
            result.succeeded = (result.exitCode == 0) and (result.output == self._formExpected(expected)) and (len(result.error) == 0)
            result.expected = self._formDatasetForExpected(dataset, expected)
            return result

    def testConcatCommandWithEmptyLists(self):
        dataset = [
          'first 1 3 2 1',
          'second 6 0 -1 1',
          'third'
        ]
        commands = [
          'concat fourth third third',
          'print fourth'
        ]
        expected = [
          '<EMPTY>'
        ]
        with tempfile.NamedTemporaryFile() as source:
            source.write(self._formDatasetForFile(dataset))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = self._formInputCommands(commands))
            result.succeeded = (result.exitCode == 0) and (result.output == self._formExpected(expected)) and (len(result.error) == 0)
            result.expected = self._formDatasetForExpected(dataset, expected)
            return result

    def testConcatCommandWithLists(self):
        dataset = [
          'first 1 3 2 1',
          'second 6 0 -1 1',
          'third'
        ]
        commands = [
          'concat fourth second third first second',
          'print fourth'
        ]
        expected = [
          'fourth 6 0 -1 1 1 3 2 1 6 0 -1 1'
        ]
        with tempfile.NamedTemporaryFile() as source:
            source.write(self._formDatasetForFile(dataset))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = self._formInputCommands(commands))
            result.succeeded = (result.exitCode == 0) and (result.output == self._formExpected(expected)) and (len(result.error) == 0)
            result.expected = self._formDatasetForExpected(dataset, expected)
            return result

    def testConcatCommandWithNotEnoughArgs(self):
        dataset = [
          'first 1 3 2 1',
          'second 6 0 -1 1',
          'third'
        ]
        commands = [
          'concat',
          'concat fourth',
          'concat fourth third',
          'print first'
        ]
        expected = [
          '<INVALID COMMAND>',
          '<INVALID COMMAND>',
          '<INVALID COMMAND>',
          'first 1 3 2 1'
        ]
        with tempfile.NamedTemporaryFile() as source:
            source.write(self._formDatasetForFile(dataset))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = self._formInputCommands(commands))
            result.succeeded = (result.exitCode == 0) and (result.output == self._formExpected(expected)) and (len(result.error) == 0)
            result.expected = self._formDatasetForExpected(dataset, expected)
            return result

    def testEqualCommandWithSameNamedList(self):
        dataset = [
          'first 1 3 2 1',
          'second 6 0 -1 1',
          'third'
        ]
        commands = [
          'equal first first first first first first first first first first',
        ]
        expected = [
          '<TRUE>'
        ]
        with tempfile.NamedTemporaryFile() as source:
            source.write(self._formDatasetForFile(dataset))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = self._formInputCommands(commands))
            result.succeeded = (result.exitCode == 0) and (result.output == self._formExpected(expected)) and (len(result.error) == 0)
            result.expected = self._formDatasetForExpected(dataset, expected)
            return result

    def testEqualCommandWithDifferentListsButContentIsSame(self):
        dataset = [
          'first 1 3 2 1',
          'second 1 3 2 1',
          'third'
        ]
        commands = [
          'equal first second first second first second first second first second',
        ]
        expected = [
          '<TRUE>'
        ]
        with tempfile.NamedTemporaryFile() as source:
            source.write(self._formDatasetForFile(dataset))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = self._formInputCommands(commands))
            result.succeeded = (result.exitCode == 0) and (result.output == self._formExpected(expected)) and (len(result.error) == 0)
            result.expected = self._formDatasetForExpected(dataset, expected)
            return result

    def testEqualCommandWithDifferentLists(self):
        dataset = [
          'first 1 3 2 1',
          'second 6 0 -1 1',
          'third'
        ]
        commands = [
          'equal first second',
        ]
        expected = [
          '<FALSE>'
        ]
        with tempfile.NamedTemporaryFile() as source:
            source.write(self._formDatasetForFile(dataset))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = self._formInputCommands(commands))
            result.succeeded = (result.exitCode == 0) and (result.output == self._formExpected(expected)) and (len(result.error) == 0)
            result.expected = self._formDatasetForExpected(dataset, expected)
            return result

    def testEqualCommandWithNotEnoughArgs(self):
        dataset = [
          'first 1 3 2 1',
          'second 6 0 -1 1',
          'third'
        ]
        commands = [
          'equal',
          'equal first',
          'print first'
        ]
        expected = [
          '<INVALID COMMAND>',
          '<INVALID COMMAND>',
          'first 1 3 2 1'
        ]
        with tempfile.NamedTemporaryFile() as source:
            source.write(self._formDatasetForFile(dataset))
            source.flush()
            args = [source.name]
            result = self.execute(args = args, input = self._formInputCommands(commands))
            result.succeeded = (result.exitCode == 0) and (result.output == self._formExpected(expected)) and (len(result.error) == 0)
            result.expected = self._formDatasetForExpected(dataset, expected)
            return result

if __name__ == "__main__":
    main(LabS3(sys.argv[1]))
