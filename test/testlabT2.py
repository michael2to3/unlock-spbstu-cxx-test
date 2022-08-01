#!/usr/bin/env python3

from test.labtesting import Lab, Result, main
import sys
import os.path

class LabT2(Lab):
    def __init__(self, student):
        super(LabT2, self).__init__(student, 'T2')

    def _mkKey(self, num, value):
        return ':key' + str(num) + ' ' + value

    def _mkShuffledRecord(self, table, key1, f1, key2, f2, key3, f3):
        result = '('
        result = result + self._mkKey(f1, table[key1][0])
        result = result + self._mkKey(f2, table[key2][0])
        result = result + self._mkKey(f3, table[key3][0])
        result = result + ':)'
        return result

    def _mkRecord(self, table, key1, num1, key2, num2, key3, num3):
        result = '('
        result = result + self._mkKey(1, table[key1][num1])
        result = result + self._mkKey(2, table[key2][num2])
        result = result + self._mkKey(3, table[key3][num3])
        result = result + ':)'
        return result

    def _mkNumRecord(self, table, key1, num1, key2, num2, num3):
        return self._mkRecord(table, key1, num1, key2, num2, "STR LIT", num3)

    def _mkVarRecord(self, table, key1, key2):
        return self._mkNumRecord(table, key1, 0, key2, 0, 0)

    def _mkTable(self):
        table = {
          "STR LIT": ['\"Data\"', '\"Data with :\"'],
          "DBL LIT": ['0.0d', '1.0d'],
          "DBL SCI": ['1.0e-1', '1.0e+2'],
          "SLL LIT": ['-89ll', '0ll'],
          "ULL LIT": ['0ull', '89ull'],
          "ULL OCT": ['00', '076'],
          "ULL BIN": ['0b0', '0b01'],
          "ULL HEX": ['0x0', '0xAF'],
          "CHR LIT": ['\'a\'', '\'z\''],
          "CMP LSP": ['#c(0.5 -0.5)', '#c(-1.0 1.0)'],
          "RAT LSP": ['(:N -3:D 2:)', '(:N -1:D 2:)']
        }
        return table

    def _isImplemented(self, key1, key2):
        table = self._mkTable()
        input = self._mkVarRecord(table, key1, key2) + '\n'
        result = self.execute(input = input)
        return (result.output == input) and (result.exitCode == 0)

    def _supported(self):
        table = self._mkTable()
        keys = list(table.keys())
        for key1 in keys[:-1]:
            for key2 in keys[1:]:
                if self._isImplemented(key1, key2):
                    return [key1, key2]
        return []

    def _formSortedRecords(self, key1, key2):
        table = self._mkTable()
        returnable = [
          self._mkNumRecord(table, key1, 0, key2, 0, 0),
          self._mkNumRecord(table, key1, 1, key2, 0, 0),
          self._mkNumRecord(table, key1, 1, key2, 1, 0),
          self._mkNumRecord(table, key1, 1, key2, 1, 1)
        ]
        return returnable

    def _formShuffledFieldsRecords(self, key1, key2):
        table = self._mkTable()
        returnable = [
          self._mkShuffledRecord(table, key1, 1, key2, 2, "STR LIT", 3),
          self._mkShuffledRecord(table, key1, 1, "STR LIT", 3, key2, 2),
          self._mkShuffledRecord(table, key2, 2, key1, 1, "STR LIT", 3),
          self._mkShuffledRecord(table, key2, 2, "STR LIT", 3, key1, 1),
          self._mkShuffledRecord(table, "STR LIT", 3, key1, 1, key2, 2),
          self._mkShuffledRecord(table, "STR LIT", 3, key2, 2, key1, 1),
        ]
        return returnable

    def testAtleastOneRecordSupproted(self):
        keys = self._supported()
        input = '\n'
        if keys:
            input = self._mkVarRecord(self._mkTable(), keys[0], keys[1]) + '\n'

        anySupported = len(input) != 0

        input = ''
        table = self._mkTable()
        keys = list(table.keys())
        for key1 in keys[:-1]:
            for key2 in keys[1:]:
                input = input + self._mkVarRecord(table, key1, key2) + '\n'

        result = self.execute(input = input)
        result.succeeded = anySupported
        result.expected = 'Atleast one supported record type\n'
        return result

    def testEcho(self):
        keys = self._supported()
        input = '\n'
        expected = 'Looks like there is no supported record. Cannot determine input. Test skipped\n'
        if keys:
            sorted = self._formSortedRecords(keys[0], keys[1])
            expected = '\n'.join(sorted) + '\n'
            input = expected
        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (len(input) != 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected
        return result

    def testSorting(self):
        keys = self._supported()
        input = '\n'
        expected = 'Looks like there is no supported record. Cannot determine input. Test skipped\n'
        if keys:
            sorted = self._formSortedRecords(keys[0], keys[1])
            expected = '\n'.join(sorted) + '\n'
            shuffled = sorted
            shuffled[:] = shuffled[2:] + shuffled[:2]
            input = '\n'.join(shuffled) + '\n'
        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (len(input) != 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected
        return result

    def testShuffledFields(self):
        keys = self._supported()
        input = '\n'
        expected = 'Looks like there is no supported record. Cannot determine input. Test skipped\n'
        if keys:
            shuffled = self._formShuffledFieldsRecords(keys[0], keys[1])
            repeated = [shuffled[0]] * len(shuffled)
            input = '\n'.join(shuffled) + '\n'
            expected = '\n'.join(repeated) + '\n'
        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (len(input) != 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected
        return result

    def testInputRecovery(self):
        keys = self._supported()
        input = '\n'
        expected = 'Looks like there is no supported record. Cannot determine input. Test skipped\n'
        if keys:
            sorted = self._formSortedRecords(keys[0], keys[1])
            expected = '\n'.join(sorted) + '\n'
            unsupported = self._mkRecord(self._mkTable(), "STR LIT", 0, "STR LIT", 0, "STR LIT", 0)
            failed = sorted
            failed.insert(2, unsupported)
            input = '\n'.join(failed) + '\n'
        result = self.execute(input = input)
        result.succeeded = (result.exitCode == 0) and (len(input) != 0) and (result.output == expected) and (len(result.error) == 0)
        result.expected = expected
        return result

if __name__ == "__main__":
    main(LabT2(sys.argv[1]))
