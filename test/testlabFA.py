#!/usr/bin/env python3

from test.labtesting import Lab, main
import sys

class LabFA(Lab):
    def __init__(self, student):
        super(LabFA, self).__init__(student, 'FA')

    def testDryRun(self):
        result = self.execute()
        result.succeeded = True
        result.expected = 'No valgrind errors'
        return result


if __name__ == "__main__":
    main(LabFA(sys.argv[1]))
