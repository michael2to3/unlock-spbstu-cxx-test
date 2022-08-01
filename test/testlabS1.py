#!/usr/bin/env python3

from test.labtesting import Lab, Result, main
import sys
import os.path
import random
import string
import tempfile

class LabS1(Lab):
    def __init__(self, student):
        super(LabS1, self).__init__(student, 'S1')

    def testIncorrectExpression(self):
        input = '( 1 - 2 ) + ('
        result = self.execute(input = input)

        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testAdditionAlmostOverflow(self):
        expected = '9223372036854775807\n'
        input = '9223372036854775806 + 1'

        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testAdditionOverflow(self):
        input = '9223372036854775807 + 1'
        result = self.execute(input = input)

        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testSubtractionAlmostUnderflow(self):
        expected = '-9223372036854775808\n'
        input = '0 - 9223372036854775807 - 1'

        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testSubtractionUnderflow(self):
        input = '0 - 9223372036854775808 - 1'
        result = self.execute(input = input)

        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testMultiplicationOverflow(self):
        input = '9223372036854775807 * 2'
        result = self.execute(input = input)

        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testMultiplicationUnderflow(self):
        input = '( 0 - 9223372036854775807 ) * 2'
        result = self.execute(input = input)

        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testDivisionOverflow(self):
        input = '( 0 - 9223372036854775808 ) / ( 0 - 1 )'
        result = self.execute(input = input)

        result.succeeded = (result.exitCode != 0) and (len(result.error) != 0)
        result.expected = 'Non-zero exit code and error message in standard error'

        return result

    def testConstantPolynom(self):
        lhs = random.randint(0, 1000)
        input = str(lhs)
        expected = str(lhs) + '\n'

        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testConstantPolynomInParentheses(self):
        lhs = random.randint(0, 1000)
        input = '( ' + str(lhs) + ' )'
        expected = str(lhs) + '\n'

        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testAddition(self):
        lhs = random.randint(0, 1000)
        rhs = random.randint(0, 1000)
        input = str(lhs) + ' + ' + str(rhs)
        expected = str(lhs + rhs) + '\n'

        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testSubtraction(self):
        lhs = random.randint(0, 1000)
        rhs = random.randint(1001, 2000)
        input = str(lhs) + ' - ' + str(rhs)
        expected = str(lhs - rhs) + '\n'

        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testMultiplication(self):
        lhs = random.randint(0, 1000)
        rhs = random.randint(0, 1000)
        input = str(lhs) + ' * ' + str(rhs)
        expected = str(lhs * rhs) + '\n'

        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testDivision(self):
        divider = random.randint(2, 1000)
        result = random.randint(2, 1000)
        lhs = divider * result
        input = str(lhs) + ' / ' + str(divider)
        expected = str(result) + '\n'

        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testNonZeroModulation(self):
        divider = random.randint(2, 1000)
        result = random.randint(2, 1000)
        reminder = random.randint(0, divider - 1)
        lhs = divider * result + reminder
        input = str(lhs) + ' % ' + str(divider)
        expected = str(reminder) + '\n'

        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testZeroModulation(self):
        divider = random.randint(1, 1000)
        result = random.randint(1, 1000)
        lhs = divider * result
        input = str(lhs) + ' % ' + str(divider)
        expected = '0\n'

        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testPositiveModOnDivisionWithNegativeNumbers(self):
        divider = random.randint(2, 1000)
        result = random.randint(2, 1000)
        reminder = random.randint(0, divider - 1)
        lhs = divider * result + reminder
        input = '( 0 - ' + str(lhs) + ' )' + ' % ' + str(divider)
        expected = str(divider - reminder) + '\n'

        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testDivisionCorrectnessWithNegativeNumbers(self):
        divider = random.randint(2, 1000)
        result = random.randint(2, 1000)
        reminder = random.randint(0, divider - 1)
        lhs = divider * result + reminder
        input = '( 0 - ' + str(lhs) + ' )' + ' / ' + str(divider)
        expected = str(-result) + '\n'

        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testReverseOrderOutput(self):
        input = '1 + ( 2 - 1 )\n( 3 * 2 ) / ( 3 - 1 )'
        expected = '3 2\n'

        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testSkipEmptyLines(self):
        input = '\n1 + ( 2 - 1 )\n\n( 3 * 2 ) / ( 3 - 1 )'
        expected = '3 2\n'

        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testComplexExpression(self):
        v1 = random.randint(5, 15)
        v2 = random.randint(5, 15)
        v3 = random.randint(5, 15)
        v4 = random.randint(5, 15)

        input = '( ' + str(v1) + ' * ' + str(v3) + ' )' + ' - ' + '( ' + str(v2) + ' + ' + str(v4) + ' )'
        expected = str(v1 * v3 - (v2 + v4)) + '\n'

        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected

        return result

    def testEmptyFile(self):
        expected = '\n'
        with tempfile.NamedTemporaryFile() as source:
            args = [source.name]
            result = self.execute(args = args)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = expected
            return result

    def testFileRead(self):
        expected = '45 2\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(b'( 1 + 3 ) / 2\n( 4 - 1 ) * 15')
            source.flush()
            args = [source.name]
            result = self.execute(args = args)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = expected
            return result


    def testSkipEmptyLinesInFile(self):
        expected = '45 2\n'
        with tempfile.NamedTemporaryFile() as source:
            source.write(b'\n( 1 + 3 ) / 2\n\n( 4 - 1 ) * 15')
            source.flush()
            args = [source.name]
            result = self.execute(args = args)
            result.succeeded = (result.exitCode == 0) and (result.output == expected) and (len(result.error) == 0)
            result.expected = expected
            return result

if __name__ == "__main__":
    main(LabS1(sys.argv[1]))
