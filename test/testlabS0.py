#!/usr/bin/env python3

from test.labtesting import Lab, Result, main
import sys
import os.path

class LabS0(Lab):
    def __init__(self, student):
        super(LabS0, self).__init__(student, 'S0')

    def testRun(self):
        result = self.execute()
        result.succeeded = (result.exitCode == 0) and (result.output == self.student + "\n")
        result.expected = self.student + "\n"
        return result

if __name__ == "__main__":
    main(LabS0(sys.argv[1]))
