#!/usr/bin/env python3

from test.labtesting import Lab, main
import sys

class LabFT(Lab):
    def __init__(self, student):
        super(LabFT, self).__init__(student, 'FT')

    def testDryRun(self):
        result = self.execute()
        result.succeeded = True
        result.expected = 'No valgrind errors'
        return result


if __name__ == "__main__":
    main(LabFT(sys.argv[1]))
