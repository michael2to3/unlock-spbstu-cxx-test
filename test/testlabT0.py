#!/usr/bin/env python3

from test.labtesting import Lab, Result, main
import sys
import os.path

class LabT0(Lab):
    def __init__(self, student):
        super(LabT0, self).__init__(student, 'T0')

    def testRun(self):
        result = self.execute()
        result.succeeded = (result.exitCode == 0) and (result.output == self.student + "\n")
        result.expected = self.student + "\n"
        return result

if __name__ == "__main__":
    main(LabT0(sys.argv[1]))
