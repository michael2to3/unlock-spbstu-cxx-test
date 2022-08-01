#!/usr/bin/env python3

from test.labtesting import Lab, Result, SingleIntegerParameterRangeValidation, main
import random
import re
import string

import sys

class AddressBook(Lab):
    def __init__(self, student, lab, name = None):
        super(AddressBook, self).__init__(student, lab, name)

        self.ARGS = ['1']

        self.PHONE_LENGTH = 11
        self.LETTERS = string.ascii_letters + ' \",'
        self.MARK_CHARS = string.ascii_letters + string.digits + '-'

        self.EMPTY_BOOK = '<EMPTY>\n'
        self.INVALID_COMMAND = '<INVALID COMMAND>\n'
        self.INVALID_BOOKMARK = '<INVALID BOOKMARK>\n'
        self.INVALID_STEP = '<INVALID STEP>\n'

    def _generatePhone(self):
        return self.generateString(self.PHONE_LENGTH, self.PHONE_LENGTH, string.digits)

    def _generateName(self):
        return self.generateString(10, 30, self.LETTERS)

    def _generateMark(self):
        return self.generateString(10, 30, self.MARK_CHARS)

    def _escapeQuotes(self, str):
        result = ''
        for c in str:
            if c != '\"':
                result += c
            else:
                result += '\\\"'

        return result

    def testParameterWithSpace(self):
        args = ['1 2']

        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testEmptyInput(self):
        result = self.execute(args = self.ARGS)

        result.succeeded = (result.exitCode == 0) and (len(result.output) == 0) and (len(result.error) == 0)
        result.expected = ''

        return result

    def testEmptyBook(self):
        input = 'show current\n'
        expected = self.EMPTY_BOOK

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testUnknownBookmark(self):
        input = 'show test\n'
        expected = self.INVALID_BOOKMARK

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testInvalidCommandFormat(self):
        number = self._generatePhone()
        name = self._generateName()
        input = 'add ' + number + '\"' + self._escapeQuotes(name) + '\"\n'
        expected = self.INVALID_COMMAND

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testMissingQuotes(self):
        number = self._generatePhone()
        name = self._generateName()
        input = 'add ' + number + ' ' + self._escapeQuotes(name) + '\nshow current\n'
        expected = self.INVALID_COMMAND + self.EMPTY_BOOK

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testSingleEntryBook(self):
        number = self._generatePhone()
        name = self._generateName()
        input = 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\nshow current\n'
        expected = number + ' ' + name + '\n'

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testSingleEntryWithQuotesInside(self):
        number = self._generatePhone()
        name = 'test \"quote\" name'
        input = 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\nshow current\n'
        expected = number + ' ' + name + '\n'

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testMove1StepForward(self):
        number = self._generatePhone()
        name = self._generateName()

        input = 'add ' + self._generatePhone() + ' \"' + self._escapeQuotes(self._generateName()) + '\"\n' \
                + 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\nmove current 1\nshow current\n'
        expected = number + ' ' + name + '\n'

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testMoveSomeStepsForward(self):
        steps = random.randint(2, 10)
        number = self._generatePhone()
        name = self._generateName()

        input = ''
        for i in range(1, steps + 1):
            input += 'add ' + self._generatePhone() + ' \"' + self._escapeQuotes(self._generateName()) + '\"\n'

        input += 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\nmove current ' + str(steps) + '\nshow current\n'
        expected = number + ' ' + name + '\n'

        result = self.execute(args = self.ARGS, input = input)
        result.name = 'Move ' + str(steps) + ' step forward'
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testMoveToTheLast(self):
        steps = random.randint(2, 10)
        number = self._generatePhone()
        name = self._generateName()

        input = ''
        for i in range(1, steps + 1):
            input += 'add ' + self._generatePhone() + ' \"' + self._escapeQuotes(self._generateName()) + '\"\n'

        input += 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\nmove current last\nshow current\n'
        expected = number + ' ' + name + '\n'

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testMove1StepBackward(self):
        number = self._generatePhone()
        name = self._generateName()

        input = 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        input += 'add ' + self._generatePhone() + ' \"' + self._escapeQuotes(self._generateName()) + '\"\n'
        input += 'move current last\nmove current -1\nshow current\n'
        expected = number + ' ' + name + '\n'

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testMoveSomeStepsBackward(self):
        steps = random.randint(2, 10)
        number = self._generatePhone()
        name = self._generateName()

        input = 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        for i in range(1, steps + 1):
            input += 'add ' + self._generatePhone() + ' \"' + self._escapeQuotes(self._generateName()) + '\"\n'

        input += 'move current last\nmove current -' + str(steps) + '\nshow current\n'
        expected = number + ' ' + name + '\n'

        result = self.execute(args = self.ARGS, input = input)
        result.name = 'Move ' + str(steps) + ' step backward'
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testMoveToTheFirst(self):
        steps = random.randint(2, 10)
        number = self._generatePhone()
        name = self._generateName()

        input = 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        for i in range(1, steps + 1):
            input += 'add ' + self._generatePhone() + ' \"' + self._escapeQuotes(self._generateName()) + '\"\n'

        input += 'move current last\nmove current first\nshow current\n'
        expected = number + ' ' + name + '\n'

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testIterateOverEntries(self):
        entries = list(map(lambda x: (self._generatePhone(), self._generateName()), range(10, random.randint(10, 31))))
        input = ''.join(map(lambda value: 'add ' + value[0] + ' \"' + self._escapeQuotes(value[1]) + '\"\n', entries)) \
                + ''.join(map(lambda x: 'show current\nmove current 1\n', entries))
        expected = ''.join(map(lambda value: value[0] + ' ' + value[1] + '\n', entries))


        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testInvalidStepKeyword(self):
        steps = random.randint(2, 10)

        input = ''
        for i in range(1, steps + 1):
            input += 'add ' + self._generatePhone() + ' \"' + self._escapeQuotes(self._generateName()) + '\"\n'

        input += 'move current asfasdf\n'
        expected = '<INVALID STEP>\n'

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testInsertBeforeAMark(self):
        number = self._generatePhone()
        name = self._generateName()
        input = 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        expected = number + ' ' + name + '\n'

        insertNumber = self._generatePhone()
        insertName = self._generateName()
        expected += insertNumber + ' ' + insertName + '\n'

        number = self._generatePhone()
        name = self._generateName()
        input += 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        expected += number + ' ' + name + '\n'

        input += 'move current last\ninsert before current ' + insertNumber + ' \"' + self._escapeQuotes(insertName) + '\"\n'
        input += 'move current first\nshow current\nmove current +1\nshow current\nmove current +1\nshow current\n'


        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testInsertBeforeAMarkAtTheFirstEntry(self):
        insertNumber = self._generatePhone()
        insertName = self._generateName()
        expected = insertNumber + ' ' + insertName + '\n'

        number = self._generatePhone()
        name = self._generateName()
        input = 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        expected += number + ' ' + name + '\n'

        number = self._generatePhone()
        name = self._generateName()
        input += 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        expected += number + ' ' + name + '\n'

        input += 'move current first\ninsert before current ' + insertNumber + ' \"' + self._escapeQuotes(insertName) + '\"\n'
        input += 'move current first\nshow current\nmove current +1\nshow current\nmove current +1\nshow current\n'

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testInsertBeforeAMarkToAnEmptyBook(self):
        number = self._generatePhone()
        name = self._generateName()
        input = 'insert before current ' + number + ' \"' + self._escapeQuotes(name) + '\"\nshow current\n'
        expected = number + ' ' + name + '\n'

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testInsertBeforeAMArkWithAnInvalidFormat(self):
        number = self._generatePhone()
        name = self._generateName()
        input = 'insert before current ' + number + '\"' + self._escapeQuotes(name) + '\"\nshow current\n'
        expected = self.INVALID_COMMAND + self.EMPTY_BOOK

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testInsertBeforeAMarkWithoutQuotes(self):
        number = self._generatePhone()
        name = self._generateName()
        input = 'insert before current ' + number + ' ' + self._escapeQuotes(name) + '\n'
        expected = self.INVALID_COMMAND

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testInsertAfterAMark(self):
        number = self._generatePhone()
        name = self._generateName()
        input = 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        expected = number + ' ' + name + '\n'

        insertNumber = self._generatePhone()
        insertName = self._generateName()
        expected += insertNumber + ' ' + insertName + '\n'

        number = self._generatePhone()
        name = self._generateName()
        input += 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        expected += number + ' ' + name + '\n'

        input += 'move current first\ninsert after current ' + insertNumber + ' \"' + self._escapeQuotes(insertName) + '\"\n'
        input += 'move current first\nshow current\nmove current +1\nshow current\nmove current +1\nshow current\n'

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testInsertAfterAMarkAtTheLastEntry(self):
        number = self._generatePhone()
        name = self._generateName()
        input = 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        expected = number + ' ' + name + '\n'

        number = self._generatePhone()
        name = self._generateName()
        input += 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        expected += number + ' ' + name + '\n'

        insertNumber = self._generatePhone()
        insertName = self._generateName()
        expected += insertNumber + ' ' + insertName + '\n'

        input += 'move current last\ninsert after current ' + insertNumber + ' \"' + self._escapeQuotes(insertName) + '\"\n'
        input += 'move current first\nshow current\nmove current +1\nshow current\nmove current +1\nshow current\n'

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testInsertAfterAMarkToAnEmptyBook(self):
        number = self._generatePhone()
        name = self._generateName()
        input = 'insert after current ' + number + ' \"' + self._escapeQuotes(name) + '\"\nshow current\n'
        expected = number + ' ' + name + '\n'

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testInsertAfterAMarkWithAnInvalidFormat(self):
        number = self._generatePhone()
        name = self._generateName()
        input = 'insert after current ' + number + '\"' + self._escapeQuotes(name) + '\"\nshow current\n'
        expected = self.INVALID_COMMAND + self.EMPTY_BOOK

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testInsertAfterAMarkWithoutQuotes(self):
        number = self._generatePhone()
        name = self._generateName()
        input = 'insert after current ' + number + ' ' + self._escapeQuotes(name) + '\n'
        expected = self.INVALID_COMMAND

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testInsertAtInvalidLocation(self):
        number = self._generatePhone()
        name = self._generateName()
        input = 'insert jhfgh current ' + number + ' ' + self._escapeQuotes(name) + '\n'
        expected = self.INVALID_COMMAND

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testDelete(self):
        number = self._generatePhone()
        name = self._generateName()
        input = 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        expected = number + ' ' + name + '\n'

        number = self._generatePhone()
        name = self._generateName()
        input += 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'

        number = self._generatePhone()
        name = self._generateName()
        input += 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        expected += number + ' ' + name + '\n'

        # Check that after deletion mark points to the next element
        expected = number + ' ' + name + '\n' + expected

        input += 'move current first\nmove current 1\ndelete current\nshow current\nmove current first\nshow current\nmove current 1\nshow current\n'

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testDeleteTheFirstEntry(self):
        number = self._generatePhone()
        name = self._generateName()
        input = 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'

        number = self._generatePhone()
        name = self._generateName()
        input += 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        expected = number + ' ' + name + '\n'
        # Check that after deletion mark points to the next element
        expected += number + ' ' + name + '\n'

        number = self._generatePhone()
        name = self._generateName()
        input += 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        expected += number + ' ' + name + '\n'

        input += 'move current first\ndelete current\nshow current\nmove current first\nshow current\nmove current 1\nshow current\n'

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testDeleteTheLastEntry(self):
        number = self._generatePhone()
        name = self._generateName()
        input = 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        expected = number + ' ' + name + '\n'

        number = self._generatePhone()
        name = self._generateName()
        input += 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        expected += number + ' ' + name + '\n'

        number = self._generatePhone()
        name = self._generateName()
        input += 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'

        input += 'move current last\ndelete current\nmove current first\nshow current\nmove current 1\nshow current\n'

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testDeleteAllEntries(self):
        number = self._generatePhone()
        name = self._generateName()
        input = 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'

        number = self._generatePhone()
        name = self._generateName()
        input += 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'

        input += 'move current first\ndelete current\ndelete current\nshow current\n'
        expected = self.EMPTY_BOOK

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testAMarkRemainsValidAfterDeletion(self):
        number = self._generatePhone()
        name = self._generateName()
        input = 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        expected1 = number + ' ' + name + '\n'

        number = self._generatePhone()
        name = self._generateName()
        input += 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        expected2 = number + ' ' + name + '\n'

        input += 'move current last\ndelete current\nshow current\n'

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and ((result.output == expected1) or (result.output == expected2)) and (len(result.error) == 0)
        result.expected = [expected1, expected2]

        return result

    def testAdditionalBookmark(self):
        number = self._generatePhone()
        name = self._generateName()
        input = 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'

        number = self._generatePhone()
        name = self._generateName()
        input += 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        expected = number + ' ' + name + '\n'

        number = self._generatePhone()
        name = self._generateName()
        input += 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        expected += number + ' ' + name + '\n'

        number = self._generatePhone()
        name = self._generateName()
        input += 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'

        markName = self._generateMark()
        input += 'move current first\nmove current 1\nstore current ' + markName + '\nmove current 1\nshow ' + markName + '\nshow current\n'

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testAdditionalBookmarkAfterInsertion(self):
        number = self._generatePhone()
        name = self._generateName()
        input = 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'

        number = self._generatePhone()
        name = self._generateName()
        input += 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        expected = number + ' ' + name + '\n'

        markName = self._generateMark()
        input += 'move current first\nmove current 1\nstore current ' + markName + '\n'

        number = self._generatePhone()
        name = self._generateName()
        input += 'insert before current ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'

        input += 'show ' + markName + '\n'

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testAdditionalBookmarkAfterDeletion(self):
        number = self._generatePhone()
        name = self._generateName()
        input = 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'

        number = self._generatePhone()
        name = self._generateName()
        input += 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'

        markName = self._generateMark()
        input += 'move current first\nmove current 1\nstore current ' + markName + '\n'

        number = self._generatePhone()
        name = self._generateName()
        input += 'add ' + number + ' \"' + self._escapeQuotes(name) + '\"\n'
        expected = number + ' ' + name + '\n'

        input += 'delete current\nshow ' + markName + '\n'

        result = self.execute(args = self.ARGS, input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

class FactorialContainer(Lab):
    def __init__(self, student, lab, name = None):
        super(FactorialContainer, self).__init__(student, lab, name)

        self.ARGS = ['2']

        self.MAX_NUMBER = 10
        self.FACTORIALS = [1]

        for i in range(2, self.MAX_NUMBER + 1):
            self.FACTORIALS.append(self.FACTORIALS[-1] * i)

    def _cleanupOutput(self, output):
        # It is officially allowed to have 1 space at the end of line.
        # The expected value doesn't contain it so it can be cleared.
        return re.sub(' \n', '\n', output)

    def testParameterWithSpace(self):
        args = ['2 1']

        result = self.execute(args = args)
        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testFactorialContent(self):
        expected = ' '.join(map(str, self.FACTORIALS)) + '\n' \
                   + ' '.join(map(str, reversed(self.FACTORIALS))) + '\n'

        result = self.execute(args = self.ARGS)
        cleanedOut = self._cleanupOutput(result.output)
        result.succeeded = (result.exitCode == 0) and (cleanedOut == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

class LabB3(Lab):
    def __init__(self, student):
        super(LabB3, self).__init__(student, 'B3')

        self.testBase = SingleIntegerParameterRangeValidation(student, self.lab, 1, 2, 'Overall program parameter check')
        self.testSection1 = AddressBook(student, self.lab, 'Lab ' + self.lab + '.1: address book')
        self.testSection2 = FactorialContainer(student, self.lab, 'Lab ' + self.lab + '.2: container of factorials')

if __name__ == "__main__":
    main(LabB3(sys.argv[1]))
